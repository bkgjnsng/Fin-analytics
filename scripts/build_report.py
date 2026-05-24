from __future__ import annotations

import ast
import calendar
import html
import json
import math
import statistics
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from case_config import Asset, CASES, EventCase, EVENT_WINDOWS, is_korean_asset


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def naver_price_url(code: str, start: datetime, end: datetime) -> str:
    params = {
        "symbol": code,
        "requestType": "1",
        "startTime": start.strftime("%Y%m%d"),
        "endTime": end.strftime("%Y%m%d"),
        "timeframe": "day",
    }
    return "https://api.finance.naver.com/siseJson.naver?" + urllib.parse.urlencode(params)


def fetch_naver_prices(asset: Asset, start: datetime, end: datetime) -> pd.DataFrame:
    url = naver_price_url(asset.code, start, end)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    payload = ast.literal_eval(raw.strip())
    if len(payload) <= 1:
        raise ValueError(f"No price data returned for {asset.code} {asset.name}")

    columns = ["date", "open", "high", "low", "close", "volume", "foreign_ownership"]
    rows = payload[1:]
    frame = pd.DataFrame(rows, columns=columns)
    frame["date"] = pd.to_datetime(frame["date"], format="%Y%m%d")
    for column in columns[1:]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["code"] = asset.code
    frame["name"] = asset.name
    frame["source"] = "naver-finance"
    return frame.dropna(subset=["close"]).sort_values("date").reset_index(drop=True)


def yahoo_symbol(code: str) -> str:
    return code.replace(".US", "").replace(".us", "").strip().upper()


def yahoo_price_url(code: str, start: datetime, end: datetime) -> str:
    period1 = calendar.timegm(start.timetuple())
    period2 = calendar.timegm((end + timedelta(days=1)).timetuple())
    params = {
        "period1": str(period1),
        "period2": str(period2),
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(yahoo_symbol(code))}?" + urllib.parse.urlencode(params)


def fetch_yahoo_prices(asset: Asset, start: datetime, end: datetime) -> pd.DataFrame:
    url = yahoo_price_url(asset.code, start, end)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    payload = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))
    result = payload.get("chart", {}).get("result") or []
    if not result:
        error = payload.get("chart", {}).get("error")
        raise ValueError(f"No Yahoo price data returned for {asset.code} {asset.name}: {error}")

    block = result[0]
    timestamps = block.get("timestamp") or []
    quote = (block.get("indicators", {}).get("quote") or [{}])[0]
    adj = (block.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose", [])
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(timestamps, unit="s").normalize(),
            "open": quote.get("open", []),
            "high": quote.get("high", []),
            "low": quote.get("low", []),
            "close": quote.get("close", []),
            "adj_close": adj if adj else quote.get("close", []),
            "volume": quote.get("volume", []),
        }
    )
    for column in ["open", "high", "low", "close", "volume"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["adj_close"] = pd.to_numeric(frame["adj_close"], errors="coerce")
    frame["foreign_ownership"] = float("nan")
    frame["code"] = asset.code
    frame["name"] = asset.name
    frame["source"] = "yahoo-finance-chart"
    return frame.dropna(subset=["close"]).sort_values("date").reset_index(drop=True)


def fetch_prices(asset: Asset, start: datetime, end: datetime) -> pd.DataFrame:
    if is_korean_asset(asset):
        return fetch_naver_prices(asset, start, end)
    return fetch_yahoo_prices(asset, start, end)


def add_event_metrics(frame: pd.DataFrame, event_date: datetime) -> pd.DataFrame:
    frame = frame.copy()
    frame["daily_return"] = frame["close"].pct_change()
    frame["event_day"] = range(-sum(frame["date"] < event_date), len(frame) - sum(frame["date"] < event_date))
    base_rows = frame.loc[frame["date"] <= event_date]
    if base_rows.empty:
        base_price = frame.iloc[0]["close"]
    else:
        base_price = base_rows.iloc[-1]["close"]
    frame["cumulative_return"] = frame["close"] / base_price - 1
    return frame


def event_window_dates(event_date: datetime) -> tuple[datetime, datetime]:
    return event_date - timedelta(days=430), event_date + timedelta(days=190)


def pct(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value * 100:,.2f}%"


def number(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value:,.0f}"


def svg_line_chart(
    title: str,
    series: dict[str, pd.DataFrame],
    y_column: str,
    colors: dict[str, str],
    x_window: tuple[int, int] = (-20, 60),
    width: int = 880,
    height: int = 360,
) -> str:
    margin = {"left": 64, "right": 28, "top": 46, "bottom": 54}
    points_by_name: dict[str, list[tuple[float, float]]] = {}
    y_values: list[float] = []
    x_values: list[float] = []

    for name, frame in series.items():
        trimmed = frame[(frame["event_day"] >= x_window[0]) & (frame["event_day"] <= x_window[1])].dropna(subset=[y_column])
        points = [(float(row.event_day), float(getattr(row, y_column))) for row in trimmed.itertuples()]
        points_by_name[name] = points
        x_values.extend([point[0] for point in points])
        y_values.extend([point[1] for point in points])

    if not y_values:
        return f"<p>No data available for {html.escape(title)}</p>"

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    if math.isclose(y_min, y_max):
        y_min -= 0.01
        y_max += 0.01
    y_padding = (y_max - y_min) * 0.12
    y_min -= y_padding
    y_max += y_padding

    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]

    def sx(x: float) -> float:
        return margin["left"] + (x - x_min) / (x_max - x_min) * plot_w

    def sy(y: float) -> float:
        return margin["top"] + (y_max - y) / (y_max - y_min) * plot_h

    elements = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">',
        f'<text x="{margin["left"]}" y="28" class="chart-title">{html.escape(title)}</text>',
        f'<line x1="{margin["left"]}" y1="{margin["top"] + plot_h}" x2="{margin["left"] + plot_w}" y2="{margin["top"] + plot_h}" class="axis"/>',
        f'<line x1="{margin["left"]}" y1="{margin["top"]}" x2="{margin["left"]}" y2="{margin["top"] + plot_h}" class="axis"/>',
    ]

    tick_candidates = [x_window[0], -10, 0, 10, 20, 60, x_window[1]]
    ticks = []
    for tick in tick_candidates:
        if x_window[0] <= tick <= x_window[1] and tick not in ticks:
            ticks.append(tick)
    for tick in ticks:
        if x_min <= tick <= x_max:
            x = sx(tick)
            elements.append(f'<line x1="{x:.1f}" y1="{margin["top"]}" x2="{x:.1f}" y2="{margin["top"] + plot_h}" class="grid"/>')
            elements.append(f'<text x="{x:.1f}" y="{height - 22}" text-anchor="middle" class="tick">{tick:+d}</text>')

    for frac in [0, 0.25, 0.5, 0.75, 1]:
        y_value = y_min + (y_max - y_min) * frac
        y = sy(y_value)
        elements.append(f'<line x1="{margin["left"]}" y1="{y:.1f}" x2="{margin["left"] + plot_w}" y2="{y:.1f}" class="grid"/>')
        elements.append(f'<text x="{margin["left"] - 10}" y="{y + 4:.1f}" text-anchor="end" class="tick">{y_value * 100:.0f}%</text>')

    x0 = sx(0)
    elements.append(f'<line x1="{x0:.1f}" y1="{margin["top"]}" x2="{x0:.1f}" y2="{margin["top"] + plot_h}" class="event-line"/>')
    elements.append(f'<text x="{x0 + 6:.1f}" y="{margin["top"] + 14}" class="event-label">IPO day</text>')

    for name, points in points_by_name.items():
        if len(points) < 2:
            continue
        path = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in points)
        color = colors.get(name, "#334155")
        elements.append(f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')

    legend_x = margin["left"]
    legend_y = height - 8
    offset = 0
    for name in series:
        color = colors.get(name, "#334155")
        label_w = max(90, len(name) * 8)
        elements.append(f'<line x1="{legend_x + offset}" y1="{legend_y - 5}" x2="{legend_x + offset + 20}" y2="{legend_y - 5}" stroke="{color}" stroke-width="3"/>')
        elements.append(f'<text x="{legend_x + offset + 26}" y="{legend_y}" class="legend">{html.escape(name)}</text>')
        offset += label_w

    elements.append("</svg>")
    return "\n".join(elements)


def table(headers: list[str], rows: list[list[str]]) -> str:
    header_html = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    row_html = []
    for row in rows:
        row_html.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    return f"<table><thead><tr>{header_html}</tr></thead><tbody>{''.join(row_html)}</tbody></table>"


def summarize_case(case: EventCase, frames: dict[str, pd.DataFrame]) -> dict[str, float | str]:
    event_date = pd.to_datetime(case.listing_date)
    ipo = frames[case.ipo.name]
    benchmark = frames[case.benchmark.name]
    peers = [frames[asset.name] for asset in case.peers]

    def cumulative(frame: pd.DataFrame, start_day: int, end_day: int) -> float:
        target = frame[(frame["event_day"] >= start_day) & (frame["event_day"] <= end_day)]
        if target.empty:
            return float("nan")
        return float((target.iloc[-1]["close"] / target.iloc[0]["close"]) - 1)

    peer_returns = [cumulative(peer, -20, -1) for peer in peers]
    peer_post = [cumulative(peer, 0, 20) for peer in peers]
    peer_post_long = [cumulative(peer, 0, 60) for peer in peers]
    benchmark_pre = cumulative(benchmark, -20, -1)
    benchmark_post = cumulative(benchmark, 0, 20)
    benchmark_post_long = cumulative(benchmark, 0, 60)

    return {
        "case": case.name,
        "listing_date": event_date.strftime("%Y-%m-%d"),
        "ipo_day_return": float(ipo.loc[ipo["date"] == event_date, "daily_return"].iloc[0]) if (ipo["date"] == event_date).any() else float("nan"),
        "ipo_t20_return": cumulative(ipo, 0, 20),
        "peer_pre_avg": statistics.fmean([x for x in peer_returns if not pd.isna(x)]),
        "peer_post_avg": statistics.fmean([x for x in peer_post if not pd.isna(x)]),
        "peer_post_avg_60": statistics.fmean([x for x in peer_post_long if not pd.isna(x)]),
        "benchmark_pre": benchmark_pre,
        "benchmark_post": benchmark_post,
        "benchmark_post_60": benchmark_post_long,
        "peer_abnormal_post": statistics.fmean([x for x in peer_post if not pd.isna(x)]) - benchmark_post,
        "peer_abnormal_post_60": statistics.fmean([x for x in peer_post_long if not pd.isna(x)]) - benchmark_post_long,
    }


def build_case(case: EventCase) -> tuple[str, dict[str, float | str], pd.DataFrame]:
    event_date = datetime.strptime(case.listing_date, "%Y-%m-%d")
    start, end = event_window_dates(event_date)
    assets = [case.ipo, case.benchmark, *case.peers]
    frames: dict[str, pd.DataFrame] = {}

    for asset in assets:
        frame = fetch_prices(asset, start, end)
        frames[asset.name] = add_event_metrics(frame, event_date)
        out = DATA_DIR / f"{case.key}_{asset.code}.csv"
        frame.to_csv(out, index=False, encoding="utf-8-sig")

    benchmark = frames[case.benchmark.name][["date", "daily_return"]].rename(columns={"daily_return": "benchmark_return"})
    for name, frame in frames.items():
        frames[name] = frame.merge(benchmark, on="date", how="left")
        frames[name]["abnormal_return"] = frames[name]["daily_return"] - frames[name]["benchmark_return"]
        frames[name]["cumulative_abnormal_return"] = frames[name]["abnormal_return"].fillna(0).cumsum()

    peer_avg = pd.concat(
        [
            frames[asset.name][["event_day", "cumulative_return", "cumulative_abnormal_return"]].assign(peer=asset.name)
            for asset in case.peers
        ],
        ignore_index=True,
    )
    peer_group = peer_avg.groupby("event_day", as_index=False)[["cumulative_return", "cumulative_abnormal_return"]].mean()
    peer_group["date"] = pd.NaT
    peer_group["close"] = float("nan")
    peer_group["daily_return"] = float("nan")
    peer_group["benchmark_return"] = float("nan")
    peer_group["abnormal_return"] = float("nan")
    frames["Peer average"] = peer_group

    colors = {
        case.ipo.name: "#2563eb",
        case.benchmark.name: "#64748b",
        "Peer average": "#dc2626",
    }
    return_chart = svg_line_chart(
        f"{case.name}: cumulative return around IPO",
        {
            case.ipo.name: frames[case.ipo.name],
            "Peer average": frames["Peer average"],
            case.benchmark.name: frames[case.benchmark.name],
        },
        "cumulative_return",
        colors,
    )
    abnormal_chart = svg_line_chart(
        f"{case.name}: cumulative abnormal return vs {case.benchmark.name}",
        {
            case.ipo.name: frames[case.ipo.name],
            "Peer average": frames["Peer average"],
        },
        "cumulative_abnormal_return",
        colors,
    )

    peer_rows = []
    for asset in case.peers:
        frame = frames[asset.name]
        t0 = frame.loc[frame["event_day"] == 0]
        t20 = frame[(frame["event_day"] >= 0) & (frame["event_day"] <= 20)]
        t60 = frame[(frame["event_day"] >= 0) & (frame["event_day"] <= 60)]
        peer_rows.append(
            [
                html.escape(asset.name),
                pct(float(t0.iloc[0]["daily_return"])) if not t0.empty else "-",
                pct(float(t20.iloc[-1]["cumulative_return"])) if not t20.empty else "-",
                pct(float(t20.iloc[-1]["cumulative_abnormal_return"])) if not t20.empty else "-",
                pct(float(t60.iloc[-1]["cumulative_abnormal_return"])) if not t60.empty else "-",
                number(float(t0.iloc[0]["volume"])) if not t0.empty else "-",
            ]
        )

    valuation_note = table(
        ["Valuation output", "Current status"],
        [
            ["PER/PBR/EV-EBITDA change", "Price-based report created; fundamental multiples require FnGuide/KRX/fundamental data input."],
            ["Practical proxy in this report", "Cumulative return, abnormal return, and trading-volume reaction around IPO date."],
            ["Next data to add", "Daily market cap, PER, PBR, and EV/EBITDA for peer companies."],
        ],
    )

    html_section = f"""
    <section>
      <h2>{html.escape(case.name)}</h2>
      <p class="meta">{case.listing_date} · {html.escape(case.industry)}</p>
      <div class="chart">{return_chart}</div>
      <div class="chart">{abnormal_chart}</div>
      <h3>Peer Group Snapshot</h3>
      {table(["Peer", "IPO-day return", "T+20 cumulative return", "T+20 CAR", "T+60 CAR", "IPO-day volume"], peer_rows)}
      <h3>Valuation Multiple Output</h3>
      {valuation_note}
    </section>
    """

    all_frames = pd.concat(
        [frame.assign(asset=name, case=case.name) for name, frame in frames.items()],
        ignore_index=True,
    )
    return html_section, summarize_case(case, frames), all_frames


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    sections = []
    summaries = []
    all_data = []
    for case in CASES:
        section, summary, case_data = build_case(case)
        sections.append(section)
        summaries.append(summary)
        all_data.append(case_data)

    summary_frame = pd.DataFrame(summaries)
    summary_frame.to_csv(DATA_DIR / "event_summary.csv", index=False, encoding="utf-8-sig")
    pd.concat(all_data, ignore_index=True).to_csv(DATA_DIR / "event_window_prices.csv", index=False, encoding="utf-8-sig")

    summary_rows = [
        [
            html.escape(str(row["case"])),
            html.escape(str(row["listing_date"])),
            pct(row["peer_pre_avg"]),
            pct(row["peer_post_avg"]),
            pct(row["peer_post_avg_60"]),
            pct(row["benchmark_post"]),
            pct(row["benchmark_post_60"]),
            pct(row["peer_abnormal_post"]),
            pct(row["peer_abnormal_post_60"]),
        ]
        for row in summaries
    ]

    report = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IPO Event Study Expected Output</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #111827;
      --muted: #5b6472;
      --line: #d7dde6;
      --soft: #f7f8fb;
      --accent: #2563eb;
    }}
    body {{
      margin: 0;
      font-family: Arial, "Malgun Gothic", sans-serif;
      color: var(--ink);
      background: white;
      line-height: 1.55;
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 40px 28px 64px;
    }}
    h1 {{
      font-size: 32px;
      margin: 0 0 8px;
      letter-spacing: 0;
    }}
    h2 {{
      margin-top: 42px;
      padding-top: 28px;
      border-top: 1px solid var(--line);
      font-size: 24px;
    }}
    h3 {{
      margin-top: 26px;
      font-size: 18px;
    }}
    .lead {{
      max-width: 780px;
      color: var(--muted);
      font-size: 16px;
    }}
    .meta {{
      color: var(--muted);
      margin-top: -8px;
    }}
    .chart {{
      margin: 22px 0;
      border: 1px solid var(--line);
      background: var(--soft);
      overflow-x: auto;
    }}
    svg {{
      display: block;
      width: 100%;
      min-width: 720px;
      height: auto;
      background: #fff;
    }}
    .chart-title {{
      font-size: 18px;
      font-weight: 700;
      fill: var(--ink);
    }}
    .axis {{
      stroke: #687386;
      stroke-width: 1;
    }}
    .grid {{
      stroke: #e7ebf1;
      stroke-width: 1;
    }}
    .event-line {{
      stroke: #111827;
      stroke-width: 1.2;
      stroke-dasharray: 4 4;
    }}
    .event-label, .tick, .legend {{
      font-size: 12px;
      fill: var(--muted);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0 22px;
      font-size: 14px;
    }}
    th, td {{
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: var(--soft);
      font-weight: 700;
    }}
    .note {{
      color: var(--muted);
      font-size: 13px;
    }}
  </style>
</head>
<body>
  <main>
    <h1>IPO Event Study Expected Output</h1>
    <p class="lead">대형 IPO 전후로 관련 상장기업과 시장지수가 어떻게 움직였는지 확인하기 위한 산출물입니다. 모든 수익률은 상장일을 t=0으로 놓고 비교했으며, 단기와 중기 반응을 함께 봅니다.</p>
    <h2>Cross-Case Summary</h2>
    {table(["Case", "Listing date", "Peer pre-IPO return", "Peer post-IPO T+20", "Peer post-IPO T+60", "Benchmark T+20", "Benchmark T+60", "Peer abnormal T+20", "Peer abnormal T+60"], summary_rows)}
    {"".join(sections)}
    <p class="note">Data source: Naver Finance daily price endpoint for Korean assets and Yahoo Finance chart API for US assets. Fundamental valuation multiples are marked as a next-step data requirement because daily PER/PBR/EV-EBITDA history is not included in these free price feeds.</p>
  </main>
</body>
</html>
"""
    report = "\n".join(line.rstrip() for line in report.splitlines()) + "\n"
    (REPORT_DIR / "ipo_event_study_report.html").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
