# Fin-analytics

## Research Topic

**대형 기업 IPO가 시장지수와 피어그룹 주가에 어떤 영향을 미치는가?**

OpenAI, SpaceX, Anthropic처럼 초대형 비상장 성장기업의 IPO 기대가 커지는 상황에서, 실제 대형 IPO가 동일 산업 피어그룹과 시장지수에 어떤 영향을 주는지 과거 사례로 검정한다.

## Research Background

대형 유니콘의 IPO는 단순히 해당 기업의 상장 이벤트에 그치지 않고, 같은 산업 내 상장기업의 밸류에이션 재평가, 투자자 관심 이동, 산업지수 및 시장지수 변동으로 이어질 수 있다.

본 프로젝트는 국내 3개, 미국 3개 IPO 사례를 활용해 IPO 전후 기간 동안 관련 산업과 시장이 어떻게 반응했는지 분석한다. 핵심 메커니즘은 수요충격효과, 정보전이효과, 경쟁효과로 구분한다.

## Case Events

| Case | IPO company | Listing date | Industry theme | Main comparison targets |
| --- | --- | --- | --- | --- |
| 1 | LG Energy Solution | 2022-01-27 | Secondary battery / EV battery | Battery peers, KOSPI |
| 2 | Doosan Robotics | 2023-10-05 | Robotics / automation | Robotics-related listed firms, KOSPI/KOSDAQ |
| 3 | LG CNS | 2025-02-05 | AI / cloud / digital transformation | IT service peers, KOSPI |
| 4 | Arm Holdings | 2023-09-14 | Semiconductor IP / AI infrastructure | Semiconductor peers, Nasdaq 100 ETF |
| 5 | Snowflake | 2020-09-16 | Cloud data platform / software | Cloud software peers, Nasdaq 100 ETF |
| 6 | Rivian | 2021-11-10 | Electric vehicles / mobility | EV and auto peers, S&P 500 ETF |

## Core Question

대형 IPO가 시장지수와 피어그룹에 단기·중기·장기 초과수익률을 만들었는가? 그 반응은 수요충격효과, 정보전이효과, 경쟁효과 중 무엇으로 해석되는가?

## Analysis Design

### 1. Event Window

각 IPO 상장일을 기준일 `t = 0`으로 두고 다음 구간을 비교한다.

| Window | Meaning |
| --- | --- |
| `t-20` to `t-1` | IPO 직전 기대 형성 구간 |
| `t=0` | 상장 당일 |
| `t+1` to `t+5` | 단기 사후 반응 |
| `t+6` to `t+20` | 사후 조정 구간 |
| `t+21` to `t+60` | 중장기 산업 재평가 구간 |
| `t+61` to `t+120` | 장기 반응 점검 구간 |

메인 추정기간은 IPO일 기준 `t-250`부터 `t-20`까지다.

### 2. Comparison Groups

각 IPO 기업별로 세 가지 그룹을 비교한다.

| Group | Description |
| --- | --- |
| IPO firm | 상장 당사자 |
| Industry peers | 같은 산업 또는 테마의 상장기업 |
| Market benchmark | KOSPI, KOSDAQ 등 전체 시장 지수 |

### 3. Main Metrics

| Metric | Purpose |
| --- | --- |
| Daily return | IPO 전후 주가 반응 확인 |
| Cumulative return | 기간별 누적 성과 비교 |
| Abnormal return | 회귀 기반 정상수익률 대비 초과수익률 측정 |
| Cumulative abnormal return | IPO 이벤트의 누적 영향 측정 |
| Trading volume change | 투자자 관심 증가 여부 확인 |
| Valuation multiple | PER, PBR, EV/EBITDA 등 재평가 여부 확인 |

## Suggested Hypotheses

1. H1: 수요충격효과로 지수와 피어그룹 주가가 내려간다.
2. H2: 정보전이효과로 피어그룹 주가가 올라간다.
3. H3: 경쟁효과로 라이벌 기업들의 주가가 떨어진다.
4. 효과는 단기와 중장기에서 서로 다르게 나타날 수 있다.

## Data Plan

### Price Data

- IPO 기업 및 비교기업의 일별 종가
- KOSPI, KOSDAQ 등 시장지수
- 산업지수 또는 테마 ETF/섹터 지수
- 거래량

### Valuation Data

- 시가총액
- PER
- PBR
- EV/EBITDA, 가능할 경우
- IPO 공모가 및 상장일 종가

## Expected Output

1. IPO별 전후 수익률 그래프
2. 시장지수 대비 초과수익률 그래프
3. peer group cumulative abnormal return 비교
4. 상장 전후 valuation multiple 변화 표
5. 세 사례 간 공통점과 차이점 정리

## Generated Outputs

- `docs/best_practice_research_plan.md`: 국내+미국 6개 사례 기준 최종 연구 실행계획
- `reports/ipo_event_study_report.html`: IPO 이벤트 스터디 결과를 한 화면에서 볼 수 있는 HTML 리포트
- `reports/ipo_regression_analysis.html`: 회귀식 기반 AR/CAR 및 H1/H2/H3 검정 리포트
- `reports/ipo_unicorn_valuation_paper.pdf`: 벤치마킹 논문/이슈보고서 형식을 반영한 최종 논문형 PDF
- `data/event_summary.csv`: 6개 IPO 사례의 핵심 수익률 요약표
- `data/event_window_prices.csv`: 이벤트 윈도우 기준 전체 가격 및 수익률 데이터
- `data/regression_results.csv`: peer 기업별 회귀계수, R², CAR, t-stat 결과
- `data/hypothesis_test_summary.csv`: IPO 사례별 H1/H2/H3 판정 요약
- `data/*_*.csv`: 사례별 종목/지수 원자료

리포트를 다시 생성하려면 다음 명령을 실행한다.

```powershell
& 'C:\Users\박준성\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts\build_report.py
```

공공데이터포털 주식시세정보 API를 사용해 회귀분석을 다시 실행하려면 인증키를 환경변수로 설정한 뒤 실행한다.

```powershell
$env:DATA_GO_KR_SERVICE_KEY = "본인_공공데이터포털_인증키"
$env:DATA_SOURCE = "public"
& 'C:\Users\박준성\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts\regression_analysis.py
```

현재 공공데이터포털 주식시세정보 API는 개별 상장주식 가격 데이터에 사용한다. KOSPI/KOSDAQ 시장지수는 별도 지수시세 API가 없을 경우 기존 지수 데이터 fallback을 사용한다.

## Initial Sources

- LG Energy Solution listing date: 2022-01-27
- Doosan Robotics listing date: 2023-10-05
- LG CNS listing date: 2025-02-05
- Arm Holdings listing date: 2023-09-14
- Snowflake listing date: 2020-09-16
- Rivian listing date: 2021-11-10
