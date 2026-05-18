from __future__ import annotations

import html
import math
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from build_report import Asset, CASES, fetch_prices as fetch_naver_prices
from public_data_api import fetch_prices as fetch_public_prices


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"

ESTIMATION_START = -250
ESTIMATION_END = -20
EVENT_WINDOWS = [(-1, 1), (0, 5), (0, 20)]


@dataclass(frozen=True)
class RegressionResult:
    case: str
    listing_date: str
    asset: str
    code: str
    market: str
    alpha: float
    beta_market: float
    beta_industry: float
    r_squared: float
    n_estimation: int
    sigma: float
    car_m1_p1: float
    t_m1_p1: float
    p_m1_p1: float
    car_0_p5: float
    t_0_p5: float
    p_0_p5: float
    car_0_p20: float
    t_0_p20: float
    p_0_p20: float


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def two_sided_p_from_t(t_stat: float) -> float:
    if pd.isna(t_stat):
        return float("nan")
    return 2.0 * (1.0 - norm_cdf(abs(t_stat)))


def add_returns(frame: pd.DataFrame, event_date: datetime) -> pd.DataFrame:
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame["date"])
    frame = frame.sort_values("date").reset_index(drop=True)
    frame["return"] = frame["close"].pct_change()
    event_position = int(frame.index[frame["date"] <= event_date].max())
    frame["event_day"] = frame.index - event_position
    return frame


def cumulative_return(frame: pd.DataFrame, start_day: int, end_day: int) -> float:
    window = frame[(frame["event_day"] >= start_day) & (frame["event_day"] <= end_day)]
    if len(window) < 2:
        return float("nan")
    return float((1.0 + window["return"].fillna(0.0)).prod() - 1.0)


def ols(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, float, float]:
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    fitted = x @ beta
    residuals = y - fitted
    ss_resid = float(np.sum(residuals**2))
    ss_total = float(np.sum((y - np.mean(y)) ** 2))
    r_squared = 1.0 - ss_resid / ss_total if ss_total else float("nan")
    dof = max(len(y) - x.shape[1], 1)
    sigma = math.sqrt(ss_resid / dof)
    return beta, r_squared, sigma


def get_history(asset: Asset, event_date: datetime) -> pd.DataFrame:
    start = event_date - timedelta(days=430)
    end = event_date + timedelta(days=45)
    fetcher = fetch_public_prices if os.environ.get("DATA_SOURCE") == "public" else fetch_naver_prices
    return add_returns(fetcher(asset, start, end), event_date)


def build_case_dataset(case) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    event_date = datetime.strptime(case.listing_date, "%Y-%m-%d")
    assets = list(case.peers)
    indexes = {
        "KOSPI": Asset("KOSPI", "KOSPI", "Index"),
        "KOSDAQ": Asset("KOSDAQ", "KOSDAQ", "Index"),
    }

    frames: dict[str, pd.DataFrame] = {}
    for asset in [*assets, *indexes.values()]:
        frames[asset.name] = get_history(asset, event_date)

    peer_returns = []
    for asset in assets:
        frame = frames[asset.name][["date", "return"]].rename(columns={"return": asset.name})
        peer_returns.append(frame)

    peer_panel = peer_returns[0]
    for frame in peer_returns[1:]:
        peer_panel = peer_panel.merge(frame, on="date", how="outer")
    peer_panel = peer_panel.sort_values("date")
    peer_panel["peer_average"] = peer_panel[[asset.name for asset in assets]].mean(axis=1)
    return frames, peer_panel


def run_asset_regression(case, asset: Asset, frames: dict[str, pd.DataFrame], peer_panel: pd.DataFrame) -> RegressionResult:
    asset_frame = frames[asset.name].copy()
    market_name = "KOSDAQ" if asset.market.upper() == "KOSDAQ" else "KOSPI"
    market_frame = frames[market_name][["date", "return"]].rename(columns={"return": "market_return"})

    peer_columns = [peer.name for peer in case.peers if peer.name != asset.name]
    industry_frame = peer_panel[["date", *peer_columns]].copy()
    industry_frame["industry_return"] = industry_frame[peer_columns].mean(axis=1)
    industry_frame = industry_frame[["date", "industry_return"]]

    panel = (
        asset_frame[["date", "event_day", "return"]]
        .merge(market_frame, on="date", how="inner")
        .merge(industry_frame, on="date", how="inner")
        .dropna(subset=["return", "market_return", "industry_return"])
        .sort_values("date")
    )

    estimation = panel[(panel["event_day"] >= ESTIMATION_START) & (panel["event_day"] <= ESTIMATION_END)]
    if len(estimation) < 40:
        raise ValueError(f"Not enough estimation data for {asset.name}: {len(estimation)} rows")

    x = np.column_stack(
        [
            np.ones(len(estimation)),
            estimation["market_return"].to_numpy(dtype=float),
            estimation["industry_return"].to_numpy(dtype=float),
        ]
    )
    y = estimation["return"].to_numpy(dtype=float)
    beta, r_squared, sigma = ols(y, x)

    event_panel = panel[(panel["event_day"] >= -5) & (panel["event_day"] <= 20)].copy()
    expected = beta[0] + beta[1] * event_panel["market_return"] + beta[2] * event_panel["industry_return"]
    event_panel["abnormal_return"] = event_panel["return"] - expected
    event_panel["asset"] = asset.name
    event_panel["case"] = case.name
    event_panel["expected_return"] = expected
    event_panel["cumulative_abnormal_return"] = event_panel["abnormal_return"].cumsum()

    out_path = DATA_DIR / f"regression_event_ar_{case.key}_{asset.code}.csv"
    event_panel.to_csv(out_path, index=False, encoding="utf-8-sig")

    window_values = {}
    for start_day, end_day in EVENT_WINDOWS:
        window = event_panel[(event_panel["event_day"] >= start_day) & (event_panel["event_day"] <= end_day)]
        car = float(window["abnormal_return"].sum()) if not window.empty else float("nan")
        t_stat = car / (sigma * math.sqrt(len(window))) if len(window) and sigma else float("nan")
        window_values[(start_day, end_day)] = (car, t_stat, two_sided_p_from_t(t_stat))

    return RegressionResult(
        case=case.name,
        listing_date=case.listing_date,
        asset=asset.name,
        code=asset.code,
        market=market_name,
        alpha=float(beta[0]),
        beta_market=float(beta[1]),
        beta_industry=float(beta[2]),
        r_squared=float(r_squared),
        n_estimation=int(len(estimation)),
        sigma=float(sigma),
        car_m1_p1=window_values[(-1, 1)][0],
        t_m1_p1=window_values[(-1, 1)][1],
        p_m1_p1=window_values[(-1, 1)][2],
        car_0_p5=window_values[(0, 5)][0],
        t_0_p5=window_values[(0, 5)][1],
        p_0_p5=window_values[(0, 5)][2],
        car_0_p20=window_values[(0, 20)][0],
        t_0_p20=window_values[(0, 20)][1],
        p_0_p20=window_values[(0, 20)][2],
    )


def fmt_pct(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"{value * 100:,.2f}%"


def fmt_num(value: float, digits: int = 3) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:,.{digits}f}"


def html_table(headers: list[str], rows: list[list[str]]) -> str:
    thead = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    tbody = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>"


def conclusion_label(market_return: float, peer_car_values: list[float]) -> tuple[str, str]:
    peer_all_down = all(value < 0 for value in peer_car_values)
    peer_all_up = all(value > 0 for value in peer_car_values)
    market_down = market_return < 0
    market_up = market_return > 0
    if market_down and peer_all_down:
        return "H0 supported", "시장지수와 모든 peer의 이벤트 반응이 음(-)으로 나타났다."
    if market_up and peer_all_up:
        return "H1 supported", "시장지수와 모든 peer의 이벤트 반응이 양(+)으로 나타났다."
    return "Mixed / inconclusive", "시장지수와 peer 기업의 방향이 모두 일치하지 않아 H0/H1 중 하나를 엄격히 지지하기 어렵다."


def build_report(results: pd.DataFrame, hypothesis: pd.DataFrame) -> None:
    regression_rows = []
    for row in results.itertuples():
        regression_rows.append(
            [
                html.escape(row.case),
                html.escape(row.asset),
                html.escape(row.market),
                fmt_num(row.alpha, 5),
                fmt_num(row.beta_market),
                fmt_num(row.beta_industry),
                fmt_num(row.r_squared),
                str(row.n_estimation),
                fmt_pct(row.car_m1_p1),
                fmt_num(row.t_m1_p1),
                fmt_pct(row.car_0_p5),
                fmt_num(row.t_0_p5),
                fmt_pct(row.car_0_p20),
                fmt_num(row.t_0_p20),
            ]
        )

    hypothesis_rows = []
    for row in hypothesis.itertuples():
        hypothesis_rows.append(
            [
                html.escape(row.case),
                html.escape(row.listing_date),
                fmt_pct(row.market_return_0_20),
                fmt_pct(row.peer_avg_car_0_20),
                html.escape(row.peer_car_signs),
                html.escape(row.result),
                html.escape(row.interpretation),
            ]
        )

    report = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IPO Regression Analysis</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, "Malgun Gothic", sans-serif;
      color: #111827;
      background: #ffffff;
      line-height: 1.55;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 40px 28px 72px;
    }}
    h1 {{ margin: 0 0 10px; font-size: 32px; }}
    h2 {{ margin-top: 38px; padding-top: 24px; border-top: 1px solid #d8dee8; font-size: 22px; }}
    p, li {{ color: #374151; }}
    .formula {{
      background: #f8fafc;
      border: 1px solid #d8dee8;
      padding: 16px 18px;
      margin: 18px 0;
      font-family: "Times New Roman", serif;
      font-size: 18px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0 26px;
      font-size: 13px;
    }}
    th, td {{
      border-bottom: 1px solid #d8dee8;
      padding: 9px 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #f3f6fa;
      font-weight: 700;
      color: #111827;
    }}
    .note {{
      font-size: 13px;
      color: #5b6472;
    }}
  </style>
</head>
<body>
  <main>
    <h1>IPO Event Regression Analysis</h1>
    <p>첨부한 이벤트 스터디 식을 기준으로 각 IPO 사례의 관련 상장 peer 기업에 대해 정상수익률을 추정하고, 이벤트 기간의 AR과 CAR을 산출했다.</p>

    <h2>Regression Model</h2>
    <div class="formula">r<sub>i,t</sub> = α<sub>i</sub> + β<sub>1,i</sub> r<sub>mkt,t</sub> + β<sub>2,i</sub> r<sub>ind,t</sub> + ε<sub>i,t</sub></div>
    <div class="formula">AR<sub>i,t</sub> = r<sub>i,t</sub> - (α̂<sub>i</sub> + β̂<sub>1,i</sub> r<sub>mkt,t</sub> + β̂<sub>2,i</sub> r<sub>ind,t</sub>)</div>
    <div class="formula">CAR<sub>i,[a,b]</sub> = Σ AR<sub>i,t</sub>, t ∈ [a,b]</div>
    <p class="note">추정기간은 IPO일 기준 -250거래일부터 -20거래일까지다. r_mkt는 KOSPI/KOSDAQ 수익률, r_ind는 같은 IPO 사례의 peer 평균 수익률을 사용했다. 개별 peer 분석 시 r_ind에는 해당 종목을 제외했다.</p>

    <h2>Hypothesis Test Summary</h2>
    <p>H0: 대형 IPO 이벤트시 주가 지수와 동일 peer 그룹들이 모두 하락한다. H1: 대형 IPO 이벤트시 주가 지수와 동일 peer 그룹들이 모두 상승한다.</p>
    {html_table(["Case", "Listing date", "Market return [0,+20]", "Peer avg CAR [0,+20]", "Peer CAR signs", "Result", "Interpretation"], hypothesis_rows)}

    <h2>Regression and CAR Table</h2>
    {html_table(["Case", "Peer stock", "Market", "Alpha", "Beta market", "Beta industry", "R²", "N", "CAR [-1,+1]", "t", "CAR [0,+5]", "t", "CAR [0,+20]", "t"], regression_rows)}

    <p class="note">p-value는 정규근사 기반 보조 지표이며, 작은 표본/비정규 수익률에서는 해석에 주의가 필요하다. DATA_SOURCE=public 실행 시 개별 주식 가격은 공공데이터포털 주식시세정보 API를 사용하고, 시장지수는 별도 지수 API가 없을 경우 기존 지수 데이터 fallback을 사용한다.</p>
  </main>
</body>
</html>
"""
    (REPORT_DIR / "ipo_regression_analysis.html").write_text(report, encoding="utf-8")


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    results: list[RegressionResult] = []
    hypothesis_rows = []

    for case in CASES:
        frames, peer_panel = build_case_dataset(case)
        case_results = []
        for asset in case.peers:
            result = run_asset_regression(case, asset, frames, peer_panel)
            results.append(result)
            case_results.append(result)

        market_frame = frames[case.benchmark.name]
        market_return = cumulative_return(market_frame, 0, 20)
        peer_cars = [result.car_0_p20 for result in case_results]
        label, interpretation = conclusion_label(market_return, peer_cars)
        hypothesis_rows.append(
            {
                "case": case.name,
                "listing_date": case.listing_date,
                "market_return_0_20": market_return,
                "peer_avg_car_0_20": float(np.mean(peer_cars)),
                "peer_car_signs": ", ".join("+" if value > 0 else "-" for value in peer_cars),
                "result": label,
                "interpretation": interpretation,
            }
        )

    results_frame = pd.DataFrame([result.__dict__ for result in results])
    hypothesis_frame = pd.DataFrame(hypothesis_rows)

    results_frame.to_csv(DATA_DIR / "regression_results.csv", index=False, encoding="utf-8-sig")
    hypothesis_frame.to_csv(DATA_DIR / "hypothesis_test_summary.csv", index=False, encoding="utf-8-sig")
    build_report(results_frame, hypothesis_frame)


if __name__ == "__main__":
    main()
