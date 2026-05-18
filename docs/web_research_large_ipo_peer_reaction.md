# Web Research: Large IPOs and Peer-Firm Market Reaction

조사일: 2026-05-18  
범위: 실제 웹에서 확인 가능한 학술 페이지, 저널 페이지, KCI/DBpia/KISS, 주요 언론 기사만 사용했다. 기존 로컬 PDF에서만 확인한 내용은 이 문서의 근거로 쓰지 않았다.

## 1. 핵심 결론

대형 IPO가 동일 산업 내 상장기업 주가에 미치는 영향은 한 방향으로 고정되지 않는다. 웹에서 확인한 연구들은 대체로 세 가지 경로를 제시한다.

1. 정보전이 또는 contagion effect
   - IPO가 산업의 성장성, 투자기회, 시장 수요를 긍정적으로 신호하면 peer 기업 주가도 상승할 수 있다.

2. 경쟁효과 또는 competitive effect
   - IPO 기업이 자본조달, 인증효과, 지식자본, R&D, 인지도 상승을 통해 경쟁력이 커지면 기존 상장 peer는 하락할 수 있다.

3. 수급/공급 충격 또는 demand/supply effect
   - 대형 IPO가 투자자 자금과 포트폴리오 비중을 흡수하면 기존 상장주, 특히 IPO와 상관관계가 높은 대체 종목이 단기적으로 하락할 수 있다.

따라서 현재 연구에서는 단순히 “대형 IPO는 peer를 상승/하락시킨다”가 아니라, `정보전이 효과`, `경쟁효과`, `수급충격`, `산업 추세` 중 무엇이 우세했는지를 사건별로 분류하는 방식이 더 설득력 있다.

## 2. 근거 강도 기준

- 강함: peer-reviewed journal 또는 공식 학술 DB 초록에서 직접 확인되는 연구결과
- 중간: 연구기관/대학/SSRN/ScienceDirect/DBpia/KCI/KISS 등에서 확인되지만 원문 전체 검토가 제한적이거나 표본 특수성이 있는 경우
- 약함: 뉴스 기사, 애널리스트 코멘트, 단일 사례 관찰. 정량 검정 전에는 가설 또는 배경 설명으로만 사용

## 3. 선행연구 근거

| 구분 | 출처 | 웹에서 확인한 내용 | 네 연구에 적용 | 근거 강도 |
|---|---|---|---|---|
| IPO 산업효과의 평균값은 약할 수 있음 | Akhigbe, Borde & Whyte, "Does an Industry Effect Exist for Initial Public Offerings?", SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=421001 | IPO가 rival firms에 미치는 평균 valuation effect는 유의하지 않을 수 있으며, 이는 정보효과와 경쟁효과가 상쇄되기 때문이라고 설명한다. 반면 대형 IPO, 경쟁산업, 기술섹터에서는 음(-)의 competitive effect가 나타날 수 있다고 제시한다. | 네 연구의 세 사례 결과가 서로 다르게 나와도 이상한 것이 아니다. 전체 평균보다 사건별 이질성을 강조해야 한다. | 강함 |
| IPO 이후 rival 성과 하락과 산업추세 분리 | Spiegel & Tookes, "Why Does an IPO Affect Rival Firms?", Review of Financial Studies: https://academic.oup.com/rfs/advance-article-pdf/doi/10.1093/rfs/hhz081/33389621/hhz081.pdf | IPO firms의 rivals는 IPO 이후 성과 하락을 경험하는 경향이 있지만, 상당 부분은 IPO 자체보다 IPO를 유발한 산업 추세와 관련된다고 설명한다. 일부 IPO에서는 IPO 기업이 경쟁기업을 희생시키며 성과를 얻는 competitive IPO가 존재한다고 제시한다. | `-20~-1` 구간을 사전추세로 보고, IPO 당일 이후 효과와 분리해야 한다. Palantir-OpenAI/SpaceX 해석에서도 산업 추세와 IPO 인과효과를 구분해야 한다. | 강함 |
| 완료된 IPO는 경쟁기업에 음(-), 철회는 양(+) | Hsu, Reed & Rocholl, "The New Game in Town: Competitive Effects of IPOs", SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1365940 | completed IPO가 있는 산업의 경쟁기업은 음(-)의 주가 반응을 보이고, IPO 철회에는 양(+)의 반응을 보인다고 제시한다. 또한 성공적 IPO 이후 경쟁기업의 영업성과 악화도 보고한다. | IPO가 단순 이벤트가 아니라 경쟁기업의 미래 영업환경을 바꾸는 사건이라는 논리로 사용 가능하다. | 강함 |
| IPO는 제품시장 경쟁전략의 일부 | Chod & Lyandres, "Strategic IPOs and Product Market Competition", ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0304405X10002461 | 상장기업은 위험분산 능력 때문에 더 공격적인 제품시장 전략을 채택할 수 있고, 이는 public firm의 경쟁지위를 강화한다고 설명한다. IPO가 market share와 rivals' valuations에 미치는 예측도 제시한다. | OpenAI/SpaceX가 IPO 이후 자본조달과 공격적 확장을 통해 Palantir의 경쟁환경을 바꿀 수 있다는 이론적 근거가 된다. | 강함 |
| 대형 자산 공급은 비슷한 기존 자산 가격을 낮출 수 있음 | Braun & Larrain, "Do IPOs Affect the Prices of Other Stocks? Evidence from Emerging Markets", DocsLib: https://docslib.org/doc/11084106/do-ipos-affect-the-prices-of-other-stocks-evidence-from-emerging-markets | 22개 신흥국 254개 IPO를 분석해, IPO와 높은 공분산을 보이는 포트폴리오가 IPO 발행월에 다른 포트폴리오보다 가격이 하락한다고 제시한다. 큰 IPO와 국제통합도가 낮은 시장에서 효과가 강하다고 설명한다. | LG에너지솔루션처럼 초대형 IPO가 기존 대형주 또는 유사 산업주에 수급 부담을 줄 수 있다는 근거로 사용한다. | 중간 |
| 국내 IPO 상장일 전후 경쟁기업 하락 | 민재훈, "IPO가 경쟁기업의 주가에 미치는 영향", DBpia: https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE10695862 / KISS: https://kiss.kstudy.com/Detail/Ar?key=3776358 | 2007~2017년 한국 IPO 531건 분석. IPO 공시 시점에는 경쟁기업 포트폴리오가 유의하게 반응하지 않았으나, 상장일 전후 11일에는 시장 대비 약 1.2~1.5% 하락했다고 제시한다. 하락은 수요충격보다 경쟁효과에 더 가까운 것으로 해석한다. | 국내 사례 연구의 핵심 근거. 현재 분석도 공시일/상장일을 분리하면 더 좋아진다. | 강함 |
| 기존 상장기업 정보가 IPO 가격에도 spillover | 전진규, "Spillover Effects of Analyst Coverage on IPO Firms", KCI: https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002770720 / Dongguk: https://pure.dongguk.edu/en/publications/spillover-effects-of-analyst-coverage-on-ipo-firms | 기존 상장기업에 대한 투자의견 상향은 IPO 저가발행률을 낮추는 contagion effect를, 기존 상장기업의 이익예측치 상향은 IPO 저가평가율을 높이는 competitive effect를 지지한다고 제시한다. 효과는 기업의 경쟁적 지위와 산업경쟁도에 따라 달라진다. | peer 기업과 IPO 기업 사이 정보전이가 양방향일 수 있음을 보여준다. 산업 전망 정보와 개별 경쟁력 정보는 분리해야 한다. | 강함 |
| 인도 시장에서도 경쟁효과와 전염효과 병존 | Pulikottil, "Competitive and contagion effect of initial public offerings in India", ScienceDirect: https://www.sciencedirect.com/science/article/pii/S2590291123002486 | 인도 6개 산업 13개 기업 표본에서 IPO가 산업 경쟁기업 주가에 미치는 영향을 분석했고, 주가 측면에서는 경쟁효과와 전염효과가 모두 관찰되나 거래량 관계는 유의하지 않았다고 제시한다. | 비미국/신흥시장에서도 효과가 혼재될 수 있음을 보강한다. 단, 표본이 작아 보조 근거로만 사용한다. | 중간 |
| 중국 IPO 승인도 기존 주식 가격에 음(-)의 영향 | Li, Sun & Tian, "The impact of IPO approval on the price of existing stocks: Evidence from China", ScienceDirect: https://www.sciencedirect.com/science/article/abs/pii/S0929119917302183 | 중국 IPO 승인제도를 이용해 IPO approval announcement가 관련 기존 주식 가격에 음(-)의 영향을 미친다고 보고한다. IPO와 더 상관관계가 높은 주식에서 효과가 강하며, 실제 IPO 주식 거래 전에도 supply-demand expectation이 가격에 반영될 수 있다고 설명한다. | OpenAI/SpaceX의 실제 상장일뿐 아니라 상장 승인, S-1 제출, 공모가 확정 같은 선행 이벤트도 분석 대상으로 둘 수 있다. | 강함 |
| 장기 산업성과도 음(-)일 수 있음 | Akhigbe, Johnston & Madura, "Long-term industry performance following IPOs", ScienceDirect: https://www.sciencedirect.com/science/article/abs/pii/S1062976906000846 | IPO 이후 36개월 동안 관련 산업 rival portfolios가 평균적으로 불리한 가격성과를 보였고, 경쟁효과와 IPO 타이밍 신호가 장기 산업효과를 설명한다고 제시한다. | 본 과제는 단기 이벤트 스터디가 중심이지만, 결론/한계에서 장기성과 분석을 후속 연구로 제안할 수 있다. | 강함 |

## 4. 한국 사례 관련 웹 근거

| 사례 | 출처 | 웹에서 확인한 내용 | 연구 적용 | 근거 강도 |
|---|---|---|---|---|
| LG에너지솔루션 IPO | Reuters via Investing.com: https://www.investing.com/news/stock-market-news/lg-energy-solution-debuts-after-13-trillion-frenzy-in-skoreas-biggest-ipo-2749657 | LGES는 한국 최대 IPO 이후 상장 첫날 종가가 공모가 대비 68% 높았고, 장중 시가총액 기준 한국 2위 기업 수준으로 부상했다. 기사에 따르면 KOSPI는 그날 3.5% 하락했다. | 초대형 IPO가 시장지수 및 기존 대형주 수급에 영향을 줄 가능성을 분석할 가치가 크다. | 중간 |
| LG에너지솔루션 수급 부담 | The Korea Times: https://www.koreatimes.co.kr/amp/business/banking-finance/20220116/lg-energy-solutions-ipo-eating-up-stock-market-liquidity-like-black-hole | LGES IPO를 앞두고 기관투자자들이 편입 자금을 마련하기 위해 국내 주식을 매도하고 있다는 보도. 기사에 따르면 첫 2주 동안 기관은 KOSPI/KOSDAQ에서 9조 원 이상 순매도했고, KOSPI는 3.26%, KOSDAQ은 5.46% 하락했다. 삼성증권 애널리스트는 LGES가 단기적으로 KOSPI200 대형주에 제약을 주는 'black hole'이 될 수 있다고 언급했다. | 수급충격 가설의 사례 근거. 다만 뉴스/애널리스트 코멘트이므로 정량분석 전에는 약한 근거로 표시해야 한다. | 약함 |
| LG에너지솔루션 공모규모 | Business Standard/Reuters: https://www.business-standard.com/article/companies/lg-energy-solution-targets-10-8-billion-in-s-korea-s-biggest-ever-ipo-122010300132_1.html | LGES IPO는 최대 108억 달러 규모로 한국 최대 IPO가 될 것으로 보도되었다. 공모자금은 생산시설 확장과 부채상환 등에 사용될 예정이라고 기사에 제시되어 있다. | Akhigbe et al.이 말한 IPO 규모와 자금 사용 목적 변수를 국내 사례에 연결할 수 있다. | 중간 |
| 두산로보틱스 IPO | Yonhap: https://en.yna.co.kr/view/AEN20231005002100320 / Reuters via Moneycontrol: https://www.moneycontrol.com/news/world/south-koreas-doosan-robotics-shares-jump-127-in-trading-debut-11479381.html | 두산로보틱스는 2023년 한국 최대 IPO였고, 상장 첫날 공모가 대비 큰 폭 상승했다. Reuters 보도는 공모 규모 4,212억 원, 첫 거래 개시가 공모가 대비 127% 상승을 제시한다. | 로봇 산업 기대가 peer 기업에 전염효과를 줄지, 신규 대표주 등장으로 기존 로봇주가 희석될지 분리해서 봐야 한다. | 중간 |
| 크래프톤 IPO | Bloomberg: https://www.bloomberg.com/news/articles/2021-07-29/krafton-ipo-to-raise-3-8-billion-in-second-largest-korean-debut / Bloomberg: https://www.bloomberg.com/news/articles/2021-08-10/pubg-maker-krafton-drops-after-raising-3-8-billion-in-ipo | 크래프톤은 38억 달러 규모의 대형 IPO였고, 상장 첫날 장중 최대 20% 하락 후 8.8% 하락 마감했다고 보도되었다. 공모가 부담, PUBG 의존도, 중국 게임 규제 우려가 언급되었다. | 크래프톤 사례에서는 IPO 자체보다 게임 산업/규제/valuation 부담이 peer 반응을 설명할 가능성이 크다. | 중간 |

## 5. 연구 설계 구체화 제안

### 5.1 이벤트를 하나만 보지 말 것

웹 근거상 IPO 영향은 상장일에만 발생하지 않는다. 중국 연구는 IPO approval announcement만으로도 기존 주식 가격이 움직일 수 있다고 제시한다. 국내 민재훈 연구도 공시일과 상장일을 분리했다.

권장 이벤트:

- 증권신고서 제출일 또는 IPO approval date
- 수요예측 결과 또는 공모가 확정일
- 일반청약일
- 상장일
- 주요 지수 편입일, 가능하면 MSCI/FTSE/KOSPI200 편입일

### 5.2 peer 그룹 선정 기준

단순 업종코드만으로 부족할 수 있다. 웹 근거상 경쟁효과는 산업경쟁도, 기술근접성, 상관관계, 시장점유율, 기존 주식과 IPO 주식의 대체성에 따라 달라진다.

권장 기준:

- 동일 산업 또는 테마
- 이벤트 이전 수익률 상관관계
- 제품시장 경쟁관계
- 시가총액 유사성
- 성장주/가치주 스타일 유사성
- 거래대금 및 개인투자자 관심도

### 5.3 회귀식 보완

기본 정상수익률 모형:

```text
r_i,t = alpha_i + beta_1i * r_mkt,t + beta_2i * r_ind,t + epsilon_i,t
```

확장 정상수익률 모형:

```text
r_i,t = alpha_i
      + beta_1i * r_mkt,t
      + beta_2i * r_ind,t
      + beta_3i * SMB_t
      + beta_4i * HML_t
      + epsilon_i,t
```

사례별 설명변수 후보:

- `IPO_Size`: 공모금액 또는 상장 시가총액
- `Relative_Size`: IPO 시가총액 / peer 평균 시가총액
- `Industry_Momentum`: 이벤트 전 -20~-1 산업수익률
- `Industry_Concentration`: Herfindahl Index 또는 proxy
- `Underpricing`: 상장 첫날 수익률
- `Demand_Shock`: 청약증거금, 기관경쟁률, 거래대금 급증률
- `Tech_Growth_Dummy`: 기술/성장주 여부

### 5.4 그래프 보완

정치테마주 연구의 이벤트-시계열 아이디어와 웹 연구의 선행 이벤트 근거를 결합해 다음 그래프를 권장한다.

- event day = 0 기준 정규화 가격지수
- peer 평균 vs 시장지수 vs 산업지수
- AR bar chart
- CAR line chart
- 거래대금 변화율
- 이벤트 전후 변동성
- -20~-1, 0, +1~+20 구간별 누적수익률 비교

## 6. Palantir, OpenAI, SpaceX로 연결하는 논리

웹 근거를 바탕으로 하면 OpenAI/SpaceX IPO가 Palantir에 미칠 영향은 다음 세 경로로 나눠야 한다.

1. 정보전이 효과
   - OpenAI 또는 SpaceX의 높은 valuation은 AI, 우주, 방산, 정부계약, 데이터 인프라 산업 전체의 성장성을 재평가하게 만들 수 있다.
   - 이 경우 Palantir에는 양(+)의 효과가 가능하다.

2. 경쟁효과
   - OpenAI가 enterprise AI, 데이터 분석, 정부/기업 AI 솔루션 쪽으로 확장하면 Palantir와의 기술/고객군 중복이 커질 수 있다.
   - SpaceX는 직접 경쟁보다는 방산·우주 생태계 내 정부계약 기대를 바꿀 가능성이 크다.

3. 수급충격
   - 초대형 IPO가 AI/방산/우주 관련 ETF 또는 성장주 포트폴리오에서 자금을 흡수하면 기존 관련주가 단기적으로 조정받을 수 있다.
   - 이 근거는 LGES 보도와 Braun & Larrain의 신흥시장 연구로 뒷받침되지만, 미국 대형주 시장에 그대로 적용하는 것은 약한 추론이다.

따라서 최종 논문에서는 "OpenAI/SpaceX IPO가 Palantir에 무조건 좋다/나쁘다"가 아니라, 기술근접성, 고객군 중복, IPO 규모, 산업 모멘텀, 시장 유동성에 따라 부호가 달라질 수 있다고 결론 내리는 편이 좋다.

## 7. 근거가 약한 부분

- LGES IPO가 KOSPI/KOSDAQ 하락의 직접 원인이라는 주장은 뉴스 기사와 애널리스트 코멘트 수준이므로 약한 근거다. 금리 상승, 글로벌 성장주 조정 등 동시 요인이 있었다.
- 두산로보틱스 IPO가 기존 로봇 peer에 어떤 방향의 영향을 줬는지는 별도 회귀분석 없이는 단정할 수 없다. 웹 기사들은 IPO 성공과 투자자 관심을 보여줄 뿐 peer 효과를 직접 검정하지 않는다.
- 크래프톤 IPO의 peer 효과도 웹 기사만으로는 단정하기 어렵다. IPO 자체보다 공모가 부담, 중국 규제, PUBG 의존도 등이 동시에 작동했다.
- OpenAI/SpaceX IPO가 Palantir에 미치는 효과는 아직 실제 이벤트가 발생하지 않았으므로 직접 실증근거가 없다. 현재 연구에서는 국내 IPO 사례를 이용한 유추로만 제시해야 한다.

## 8. 바로 반영할 문장 초안

선행연구는 IPO가 동일 산업 내 상장기업에 미치는 효과가 정보전이와 경쟁효과의 상대적 크기에 따라 달라진다고 보고한다. Akhigbe et al.은 평균적으로는 유의한 산업효과가 관찰되지 않을 수 있으나, 이는 정보효과와 경쟁효과가 상쇄되기 때문이며 대형·기술·경쟁산업 IPO에서는 음(-)의 경쟁효과가 나타날 수 있다고 제시한다. Hsu et al.과 Spiegel and Tookes는 IPO가 경쟁기업의 주가 및 영업성과에 부정적 영향을 줄 수 있음을 보이되, 산업 추세와 IPO 자체의 인과효과를 구분해야 한다고 강조한다. 국내 연구인 민재훈(2020)은 한국 IPO 531건을 분석하여 IPO 공시일에는 경쟁기업 포트폴리오가 유의하게 반응하지 않았지만, 상장일 전후에는 시장 대비 약 1.2~1.5% 하락했음을 보고한다. 이러한 문헌을 바탕으로 본 연구는 LG에너지솔루션, 두산로보틱스, 크래프톤 IPO를 대상으로 상장 전후 peer 기업의 AR과 CAR을 측정하고, 관찰된 반응을 정보전이, 경쟁효과, 수급충격, 산업추세로 구분해 해석한다.

