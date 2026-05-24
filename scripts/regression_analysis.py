from __future__ import annotations

import html
import math
import os
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from io import BytesIO, StringIO
from pathlib import Path

import numpy as np
import pandas as pd

from build_report import fetch_prices as fetch_market_prices
from case_config import Asset, CASES, ESTIMATION_END, ESTIMATION_START, EVENT_WINDOWS, EventCase, is_us_case
from public_data_api import fetch_prices as fetch_public_prices


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"

FAMA_FRENCH_DAILY_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip"


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
    beta_smb: float
    beta_hml: float
    factor_model: str
    r_squared: float
    n_estimation: int
    sigma: float
    car_m1_p1: float
    t_m1_p1: float
    p_m1_p1: float
    car_0_p1: float
    t_0_p1: float
    p_0_p1: float
    car_0_p5: float
    t_0_p5: float
    p_0_p5: float
    car_0_p20: float
    t_0_p20: float
    p_0_p20: float
    car_0_p60: float
    t_0_p60: float
    p_0_p60: float
    car_0_p120: float
    t_0_p120: float
    p_0_p120: float


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


def fetch_fama_french_daily() -> pd.DataFrame:
    cache_path = DATA_DIR / "fama_french_daily_factors.csv"
    if cache_path.exists():
        return pd.read_csv(cache_path, parse_dates=["date"])

    raw = urllib.request.urlopen(FAMA_FRENCH_DAILY_URL, timeout=30).read()
    with zipfile.ZipFile(BytesIO(raw)) as archive:
        csv_name = archive.namelist()[0]
        text = archive.read(csv_name).decode("latin1")

    lines = text.splitlines()
    start_idx = next(i for i, line in enumerate(lines) if line.startswith(",Mkt-RF"))
    end_idx = next(i for i in range(start_idx + 1, len(lines)) if not lines[i].strip())
    csv_text = "\n".join(lines[start_idx:end_idx])
    factors = pd.read_csv(StringIO(csv_text))
    factors = factors.rename(columns={factors.columns[0]: "date", "Mkt-RF": "mkt_rf", "SMB": "smb", "HML": "hml", "RF": "rf"})
    factors["date"] = pd.to_datetime(factors["date"].astype(str), format="%Y%m%d")
    for column in ["mkt_rf", "smb", "hml", "rf"]:
        factors[column] = pd.to_numeric(factors[column], errors="coerce") / 100.0
    factors.to_csv(cache_path, index=False, encoding="utf-8-sig")
    return factors


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
    end = event_date + timedelta(days=190)
    fetcher = fetch_public_prices if os.environ.get("DATA_SOURCE") == "public" and asset.code.isdigit() else fetch_market_prices
    return add_returns(fetcher(asset, start, end), event_date)


def market_assets_for_case(case: EventCase) -> list[Asset]:
    assets = {case.benchmark.name: case.benchmark}
    if any(asset.market.upper() == "KOSPI" for asset in case.peers):
        assets["KOSPI"] = Asset("KOSPI", "KOSPI", "Index")
    if any(asset.market.upper() == "KOSDAQ" for asset in case.peers):
        assets["KOSDAQ"] = Asset("KOSDAQ", "KOSDAQ", "Index")
    return list(assets.values())


def market_name_for_asset(case: EventCase, asset: Asset) -> str:
    if asset.market.upper() == "KOSDAQ":
        return "KOSDAQ"
    if asset.market.upper() == "KOSPI":
        return "KOSPI"
    return case.benchmark.name


def build_case_dataset(case: EventCase) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    event_date = datetime.strptime(case.listing_date, "%Y-%m-%d")
    assets = list(case.peers)

    frames: dict[str, pd.DataFrame] = {}
    for asset in [*assets, *market_assets_for_case(case)]:
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


def run_asset_regression(case: EventCase, asset: Asset, frames: dict[str, pd.DataFrame], peer_panel: pd.DataFrame) -> RegressionResult:
    asset_frame = frames[asset.name].copy()
    market_name = market_name_for_asset(case, asset)
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

    factor_model = "market_industry"
    factor_columns: list[str] = []
    if is_us_case(case):
        try:
            factors = fetch_fama_french_daily()[["date", "smb", "hml"]]
            panel = panel.merge(factors, on="date", how="inner")
            factor_columns = ["smb", "hml"]
            factor_model = "market_industry_smb_hml"
        except Exception:
            factor_columns = []
            factor_model = "market_industry_factor_unavailable"

    estimation = panel[(panel["event_day"] >= ESTIMATION_START) & (panel["event_day"] <= ESTIMATION_END)]
    if len(estimation) < 40:
        raise ValueError(f"Not enough estimation data for {asset.name}: {len(estimation)} rows")

    x_columns = ["market_return", "industry_return", *factor_columns]
    x = np.column_stack(
        [
            np.ones(len(estimation)),
            *[estimation[column].to_numpy(dtype=float) for column in x_columns],
        ]
    )
    y = estimation["return"].to_numpy(dtype=float)
    beta, r_squared, sigma = ols(y, x)

    event_panel = panel[(panel["event_day"] >= -5) & (panel["event_day"] <= 120)].copy()
    expected = beta[0]
    for idx, column in enumerate(x_columns, start=1):
        expected = expected + beta[idx] * event_panel[column]
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
        beta_smb=float(beta[3]) if len(beta) > 3 else float("nan"),
        beta_hml=float(beta[4]) if len(beta) > 4 else float("nan"),
        factor_model=factor_model,
        r_squared=float(r_squared),
        n_estimation=int(len(estimation)),
        sigma=float(sigma),
        car_m1_p1=window_values[(-1, 1)][0],
        t_m1_p1=window_values[(-1, 1)][1],
        p_m1_p1=window_values[(-1, 1)][2],
        car_0_p1=window_values[(0, 1)][0],
        t_0_p1=window_values[(0, 1)][1],
        p_0_p1=window_values[(0, 1)][2],
        car_0_p5=window_values[(0, 5)][0],
        t_0_p5=window_values[(0, 5)][1],
        p_0_p5=window_values[(0, 5)][2],
        car_0_p20=window_values[(0, 20)][0],
        t_0_p20=window_values[(0, 20)][1],
        p_0_p20=window_values[(0, 20)][2],
        car_0_p60=window_values[(0, 60)][0],
        t_0_p60=window_values[(0, 60)][1],
        p_0_p60=window_values[(0, 60)][2],
        car_0_p120=window_values[(0, 120)][0],
        t_0_p120=window_values[(0, 120)][1],
        p_0_p120=window_values[(0, 120)][2],
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


def effect_labels(market_return: float, peer_car_values: list[float]) -> tuple[str, str, str, str]:
    clean = [value for value in peer_car_values if not pd.isna(value)]
    if not clean:
        return "Insufficient", "Insufficient", "Insufficient", "peer CAR 표본이 부족해 판단을 보류한다."

    peer_avg = float(np.mean(clean))
    negative_share = sum(value < 0 for value in clean) / len(clean)
    positive_share = sum(value > 0 for value in clean) / len(clean)

    h1 = "Supported" if market_return < 0 and peer_avg < 0 and negative_share >= 0.5 else "Not supported"
    h2 = "Supported" if peer_avg > 0 and positive_share >= 0.5 else "Not supported"
    h3 = "Supported" if peer_avg < 0 and negative_share >= 0.5 else "Not supported"

    if h1 == "Supported":
        interpretation = "시장/peer 평균이 함께 음(-)으로 나타나 단기 수요충격효과가 우세하다."
    elif h2 == "Supported":
        interpretation = "peer 평균 CAR이 양(+)으로 나타나 산업 성장성 재평가 또는 정보전이효과가 우세하다."
    elif h3 == "Supported":
        interpretation = "peer 평균 CAR이 음(-)으로 나타나 기존 상장 경쟁기업에 대한 경쟁효과가 우세하다."
    else:
        interpretation = "시장과 peer 반응이 엇갈려 단일 효과보다 수요충격, 정보전이, 경쟁효과가 혼재된 것으로 해석한다."
    return h1, h2, h3, interpretation


def build_report(results: pd.DataFrame, hypothesis: pd.DataFrame) -> None:
    regression_rows = []
    for row in results.itertuples():
        regression_rows.append(
            [
                html.escape(row.case),
                html.escape(row.asset),
                html.escape(row.market),
                html.escape(row.factor_model),
                fmt_num(row.alpha, 5),
                fmt_num(row.beta_market),
                fmt_num(row.beta_industry),
                fmt_num(row.beta_smb),
                fmt_num(row.beta_hml),
                fmt_num(row.r_squared),
                str(row.n_estimation),
                fmt_pct(row.car_m1_p1),
                fmt_num(row.t_m1_p1),
                fmt_pct(row.car_0_p1),
                fmt_num(row.t_0_p1),
                fmt_pct(row.car_0_p5),
                fmt_num(row.t_0_p5),
                fmt_pct(row.car_0_p20),
                fmt_num(row.t_0_p20),
                fmt_pct(row.car_0_p60),
                fmt_num(row.t_0_p60),
                fmt_pct(row.car_0_p120),
                fmt_num(row.t_0_p120),
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
                fmt_pct(row.peer_avg_car_0_60),
                html.escape(row.peer_car_signs),
                html.escape(row.h1_demand_shock),
                html.escape(row.h2_information_transfer),
                html.escape(row.h3_competition_effect),
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
    <p>첨부한 이벤트 스터디 식을 기준으로 각 IPO 사례의 관련 상장 peer 기업에 대해 정상수익률을 추정하고, 이벤트 기간의 AR과 CAR을 산출했다. 국내 3개 사례와 미국 3개 사례를 분리해 비교한다.</p>

    <h2>Regression Model</h2>
    <div class="formula">r<sub>i,t</sub> = α<sub>i</sub> + β<sub>1,i</sub> r<sub>mkt,t</sub> + β<sub>2,i</sub> r<sub>ind,t</sub> + β<sub>3,i</sub> SMB<sub>t</sub> + β<sub>4,i</sub> HML<sub>t</sub> + ε<sub>i,t</sub></div>
    <div class="formula">AR<sub>i,t</sub> = r<sub>i,t</sub> - E(r<sub>i,t</sub>)</div>
    <div class="formula">CAR<sub>i,[a,b]</sub> = Σ AR<sub>i,t</sub>, t ∈ [a,b]</div>
    <p class="note">추정기간은 IPO일 기준 -250거래일부터 -20거래일까지다. r_mkt는 KOSPI/KOSDAQ 또는 미국 ETF 벤치마크 수익률, r_ind는 같은 IPO 사례의 peer 평균 수익률을 사용했다. 개별 peer 분석 시 r_ind에는 해당 종목을 제외했다. SMB/HML은 미국 사례에서 Fama-French daily factor를 사용하며, 국내 사례는 공개 일별 SMB/HML 데이터가 없어 시장-산업 모형으로 표시한다.</p>

    <h2>Hypothesis Test Summary</h2>
    <p>H1은 수요충격효과, H2는 정보전이효과, H3는 경쟁효과를 검정한다. 핵심 판정은 [0,+20] 구간을 중심으로 하되 [0,+60]을 중기 보조 지표로 함께 제시한다.</p>
    {html_table(["Case", "Listing date", "Market return [0,+20]", "Peer avg CAR [0,+20]", "Peer avg CAR [0,+60]", "Peer CAR signs", "H1 demand shock", "H2 information", "H3 competition", "Interpretation"], hypothesis_rows)}

    <h2>Regression and CAR Table</h2>
    {html_table(["Case", "Peer stock", "Market", "Model", "Alpha", "Beta market", "Beta industry", "Beta SMB", "Beta HML", "R²", "N", "CAR [-1,+1]", "t", "CAR [0,+1]", "t", "CAR [0,+5]", "t", "CAR [0,+20]", "t", "CAR [0,+60]", "t", "CAR [0,+120]", "t"], regression_rows)}

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
        market_return_60 = cumulative_return(market_frame, 0, 60)
        peer_cars = [result.car_0_p20 for result in case_results]
        peer_cars_60 = [result.car_0_p60 for result in case_results]
        h1, h2, h3, interpretation = effect_labels(market_return, peer_cars)
        hypothesis_rows.append(
            {
                "case": case.name,
                "listing_date": case.listing_date,
                "market_return_0_20": market_return,
                "market_return_0_60": market_return_60,
                "peer_avg_car_0_20": float(np.mean(peer_cars)),
                "peer_avg_car_0_60": float(np.mean(peer_cars_60)),
                "peer_car_signs": ", ".join("+" if value > 0 else "-" for value in peer_cars),
                "h1_demand_shock": h1,
                "h2_information_transfer": h2,
                "h3_competition_effect": h3,
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
