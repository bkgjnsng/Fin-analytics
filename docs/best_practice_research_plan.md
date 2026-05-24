# 대형 기업 IPO가 지수와 피어그룹 주가에 미치는 영향: 실행 계획

## 1. 연구 주제

대형 기업 IPO가 시장지수와 동일 산업 피어그룹 주가에 미치는 영향을 사건연구와 회귀 기반 초과수익률 분석으로 검정한다. 연구의 실질적 출발점은 OpenAI, SpaceX, Anthropic 같은 초대형 비상장 성장기업이 상장할 경우 Palantir, Snowflake, Rocket Lab 등 기존 상장 피어기업과 관련 지수가 어떤 방향으로 움직일지에 대한 투자적 질문이다.

## 2. 연구 배경과 문제의식

최근 대형 AI·우주·인프라 기업의 IPO 기대가 커지면서, IPO가 해당 기업만의 자금조달 이벤트를 넘어 기존 상장기업의 valuation과 섹터 자금흐름을 바꿀 가능성이 커졌다. 만약 피어그룹이 상승한다면 투자자는 IPO 전후 어느 시점에 매수해야 하는지, 반대로 하락한다면 언제 위험을 줄여야 하는지가 중요한 문제가 된다.

본 연구는 이 질문을 직접 상장 전의 OpenAI·SpaceX 자료로 검정하기 어렵기 때문에, 과거 대형 IPO 사례를 이용해 유사한 시장 반응을 관찰한다.

## 3. 핵심 연구질문

1. 대형 IPO는 시장지수 또는 섹터지수에 음(-)의 초과수익률을 유발하는가?
2. 대형 IPO는 동일 산업 피어그룹에 양(+)의 정보전이효과를 유발하는가?
3. 대형 IPO는 직접 라이벌 기업에 음(-)의 경쟁효과를 유발하는가?
4. 효과는 IPO 당일 단기 반응과 이후 중기·장기 반응에서 다르게 나타나는가?

## 4. 이론적 메커니즘

| 메커니즘 | 예상 방향 | 해석 |
| --- | --- | --- |
| 수요충격효과 | 지수/피어 하락 | 대형 IPO가 투자자 자금을 흡수하면서 기존 상장기업에서 자금이 이탈 |
| 정보전이효과 | 피어 상승 | IPO 흥행이 산업 성장성과 valuation benchmark를 긍정적으로 재평가 |
| 경쟁효과 | 라이벌 하락 | 신규 상장기업이 자본조달과 시장 주목도를 확보하면서 기존 경쟁기업의 상대 매력 하락 |

## 5. 연구가설

| 구분 | 가설 |
| --- | --- |
| H1 | 수요충격효과로 지수와 피어그룹 주가가 내려간다. |
| H0_1 | 대형 IPO는 지수와 피어그룹 주가를 유의하게 하락시키지 않는다. |
| H2 | 정보전이효과로 피어그룹 주가가 올라간다. |
| H0_2 | 대형 IPO는 피어그룹 주가를 유의하게 상승시키지 않는다. |
| H3 | 경쟁효과로 라이벌 기업들의 주가가 떨어진다. |
| H0_3 | 대형 IPO는 라이벌 기업 주가를 유의하게 하락시키지 않는다. |

## 6. 분석 사례

국내와 미국을 한 표본에 섞어 단일 결론을 내리기보다, 국내 3개와 미국 3개 패널을 병렬로 비교한다. 국내 사례는 한국 시장에서 접근 가능한 대형 IPO 반응을 보고, 미국 사례는 OpenAI·SpaceX·Anthropic IPO의 선행 유사사례로 해석한다.

| 패널 | IPO 사례 | 상장일 | 산업 | 연구상 의미 |
| --- | --- | --- | --- | --- |
| 국내 | LG에너지솔루션 | 2022-01-27 | 2차전지 | 초대형 IPO와 수요충격효과 |
| 국내 | 두산로보틱스 | 2023-10-05 | 로봇/자동화 | 성장 테마 IPO와 정보전이효과 |
| 국내 | LG CNS | 2025-02-05 | AI·클라우드·DX | 국내 AI/클라우드 피어 재평가 |
| 미국 | Arm Holdings | 2023-09-14 | 반도체 IP/AI 인프라 | AI 인프라 valuation benchmark |
| 미국 | Snowflake | 2020-09-16 | 클라우드 데이터 | 소프트웨어 고성장 IPO |
| 미국 | Rivian | 2021-11-10 | 전기차 | 대형 성장기업 IPO와 경쟁효과 |

## 7. 피어그룹 설계

| IPO 기업 | 피어그룹 | 벤치마크 |
| --- | --- | --- |
| LG에너지솔루션 | LG Chem, Samsung SDI, SK Innovation | KOSPI |
| 두산로보틱스 | Doosan Corp, Rainbow Robotics, Robostar | KOSPI/KOSDAQ |
| LG CNS | Samsung SDS, Hyundai AutoEver, POSCO DX | KOSPI |
| Arm Holdings | AMD, Qualcomm, Broadcom, Synopsys, Cadence | Nasdaq 100 ETF |
| Snowflake | Datadog, MongoDB, Salesforce, ServiceNow, Oracle | Nasdaq 100 ETF |
| Rivian | Tesla, Ford, GM, NIO, XPeng | S&P 500 ETF |

피어그룹은 단순 유사기업이 아니라 직접 경쟁기업, 보완재, 산업 생태계 기업이 섞여 있다. 따라서 결과 해석에서는 평균 CAR뿐 아니라 개별 기업 방향도 함께 본다.

## 8. 사건일과 이벤트 윈도우

메인 사건일은 IPO 상장일 `t=0`으로 둔다. 이후 자료가 확보되면 IPO 발표일, 증권신고서 제출일, 공모가 확정일을 보조 사건일로 추가한다.

| 구간 | 목적 |
| --- | --- |
| `[-250,-20]` | 정상수익률 회귀 추정기간 |
| `[-1,+1]` | IPO 직전·당일·직후 초단기 반응 |
| `[0,+1]` | 상장일과 다음 거래일 반응 |
| `[0,+5]` | 1주 이내 단기 반응 |
| `[0,+20]` | 약 1개월 중기 반응 |
| `[0,+60]` | 약 3개월 중장기 반응 |
| `[0,+120]` | 약 6개월 장기 반응 |

## 9. 회귀모형

정상수익률은 다음 모형으로 추정한다.

```text
r_i,t = α_i + β_1 r_m,t + β_2 r_ind,t + β_3 SMB_t + β_4 HML_t + ε_i,t
```

초과수익률과 누적초과수익률은 다음과 같이 계산한다.

```text
AR_i,t = r_i,t - E(r_i,t)
CAR_i(τ1, τ2) = Σ AR_i,t
```

미국 사례는 Fama-French daily factor의 SMB/HML을 사용한다. 국내 사례는 무료 공개 일별 SMB/HML 자료가 제한적이므로, 현재 구현에서는 시장수익률과 산업수익률을 이용한 모형을 사용하고 향후 KRX/FnGuide 기반 팩터 구축을 보완 과제로 둔다.

## 10. 검정과 해석 기준

| 효과 | 판정 기준 |
| --- | --- |
| H1 수요충격효과 | 시장수익률과 피어 평균 CAR이 모두 음(-), 피어 과반이 하락 |
| H2 정보전이효과 | 피어 평균 CAR이 양(+), 피어 과반이 상승 |
| H3 경쟁효과 | 피어 평균 CAR이 음(-), 피어 과반이 하락 |

작은 표본 연구이므로 p-value만으로 결론을 내리지 않고, 방향성, 효과 크기, 사례 간 일관성을 함께 해석한다.

## 11. 산출물

| 산출물 | 파일 |
| --- | --- |
| IPO 전후 가격/누적수익률 시각화 | `reports/ipo_event_study_report.html` |
| 회귀계수, AR/CAR, 가설검정 결과 | `reports/ipo_regression_analysis.html` |
| 사례별 이벤트 윈도우 가격 데이터 | `data/event_window_prices.csv` |
| 회귀결과 테이블 | `data/regression_results.csv` |
| 가설검정 요약 | `data/hypothesis_test_summary.csv` |

## 12. 발표용 메시지

핵심 결론은 단순히 "대형 IPO는 피어를 올린다/내린다"가 아니다. 대형 IPO는 단기적으로는 수요충격을 만들 수 있고, 중기적으로는 산업 성장성에 대한 정보전이를 만들 수 있으며, 직접 경쟁기업에는 경쟁효과를 유발할 수 있다. 따라서 OpenAI나 SpaceX 같은 초대형 IPO를 투자 관점에서 볼 때도 상장일 전후의 단기 반응과 이후 산업 재평가를 분리해서 봐야 한다.

## 13. 배경 참고자료

- OpenAI IPO 준비 관련 보도: [Axios](https://www.axios.com/2026/05/20/openai-ipo-spacex-musk)
- SpaceX, OpenAI, Anthropic IPO 기대 관련 보도: [Axios](https://www.axios.com/2026/05/20/spacex-openai-anthropic-ipos)
- Anthropic IPO 준비 관련 보도: [Reuters via Investing.com](https://m.investing.com/news/stock-market-news/anthropic-plans-an-ipo-as-early-as-2026-ft-reports-4387279?ampMode=1)
- 미국 SMB/HML 팩터 출처: [Kenneth R. French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
