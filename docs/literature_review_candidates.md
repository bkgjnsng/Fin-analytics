# OASIS 문헌 탐색 및 연구 보완 계획

## 1. 현재 연구의 중심 질문

본 연구는 대형 비상장 유니콘의 IPO 기대 및 실제 상장이 관련 상장기업의 valuation에 어떤 영향을 주는지 분석한다. 출발점은 OpenAI와 SpaceX가 향후 상장될 경우 Palantir 및 미국 기술주/방산·우주/AI 관련 지수가 어떻게 반응할지에 대한 투자자 관점의 질문이다. 다만 국내 자료 접근성과 한국 시장 내 연구 공백을 고려하여 LG에너지솔루션, 두산로보틱스, LG CNS IPO를 국내 대형 IPO 사례로 삼고, 동일 산업 peer 기업과 시장지수의 이벤트 전후 반응을 분석한다.

핵심 방법론은 사건연구(event study)와 다중회귀분석이다. 기본 시장모형에 시장수익률과 산업수익률을 넣고, 확장모형에서는 SMB와 HML 요인을 추가하여 정상수익률을 추정한 뒤 AR 및 CAR을 산출한다.

## 2. 반드시 반영할 핵심 문헌

### 2.1 Spiegel & Tookes (2020), "Why Does an IPO Affect Rival Firms?"

- 출처: The Review of Financial Studies, 33(7), 3205-3249.
- OASIS 검색어: `IPO rival firms`
- 활용도: 최상
- 연구 적용:
  - 본 연구의 이론적 중심축으로 사용한다.
  - IPO가 경쟁기업에 미치는 영향은 단순히 "상승/하락"이 아니라, 산업 전체 전망 개선, 경쟁 심화, 수요 충격, 자본 재배분이 섞여 나타날 수 있다는 틀을 제공한다.
  - 논문은 IPO 이후 경쟁기업의 성과 악화를 보이지만, 상당 부분은 IPO 자체의 인과효과라기보다 IPO가 발생한 산업 환경의 사전 추세와 관련되어 있다고 해석한다.
- 본 연구 보완점:
  - 단순 CAR 부호 검정에 그치지 말고, 각 IPO 사례를 다음 네 가지 유형으로 분류한다.
    - 산업 전망 개선형: IPO가 산업 전체 성장 기대를 강화하여 peer도 상승
    - 경쟁 심화형: IPO 기업으로 투자자 관심과 자본이 이동하여 peer 하락
    - 산업 추세 반영형: IPO 이전부터 산업이 상승/하락하고 있었고 IPO는 그 추세의 관찰 가능한 사건
    - 혼합형: 단기에는 상승하나 이후 경쟁 압력 또는 밸류에이션 부담으로 하락
  - OpenAI/SpaceX와 Palantir 연결에서는 "IPO 자체의 효과"와 "AI/우주·방산 산업 기대 변화"를 분리하는 논리로 확장한다.

### 2.2 Akhigbe, Borde & Whyte (2003), "Does an Industry Effect Exist for Initial Public Offerings?"

- 출처: Financial Review, 38(4), 531-551.
- OASIS/기존 첨부 논문
- 활용도: 최상
- 연구 적용:
  - 경쟁기업 포트폴리오를 구성하고 IPO 이벤트 전후의 비정상수익률을 측정하는 표준 구조를 제공한다.
  - 평균적으로 경쟁기업 효과가 유의하지 않을 수 있다는 점을 보여주며, 이는 정보효과와 경쟁효과가 서로 상쇄될 수 있음을 의미한다.
- 본 연구 보완점:
  - IPO 규모가 클수록, 기술산업일수록, 경쟁강도가 높을수록 peer 기업에는 부정적 효과가 커질 수 있다는 설명변수를 추가한다.
  - 국내 사례에서는 다음 변수를 사례별 정성 변수 또는 회귀 통제변수로 구성한다.
    - IPO 상대규모: IPO 공모금액 / 기존 peer 시가총액
    - 산업 경쟁도: peer 수, 시장점유율 집중도, Herfindahl Index 가능 여부
    - 기술/성장주 여부
    - 상장 직전 산업 모멘텀
    - 상장 직전 시장 분위기

### 2.3 강명혜·임윤수 (2011), "The Impact of Initial Public Offerings on Rival Firms: Evidence from KOSDAQ Market"

- 출처: 경영경제연구, 34(1), 209-236.
- OASIS 검색어: `IPO rival firms`, `기업공개 경쟁기업`
- 활용도: 최상
- 연구 적용:
  - 한국 시장에서 IPO가 경쟁기업에 미치는 영향을 직접 다룬 문헌이다.
  - 본 연구가 국내 대형 IPO 사례를 쓰는 이유를 뒷받침한다.
  - KOSDAQ 시장 중심이라는 점에서 두산로보틱스처럼 성장주·기술주 성격이 강한 사례 해석에 도움을 준다.
- 본 연구 보완점:
  - 한국 시장에서는 개인투자자 수급, 테마성, 신규상장주 관심 집중이 강하므로 미국 문헌과 별도의 시장 미시구조적 해석을 추가한다.
  - 공모주 청약, 상장 당일 거래대금, 기관 의무보유 확약 등 국내 IPO 특유의 변수도 후속 확장변수로 제시한다.

### 2.4 민재훈 (2020), "IPO가 경쟁기업의 주가에 미치는 영향: 정보전이 효과와 수요충격효과"

- 출처: 금융지식연구, 18(1), 33-69.
- OASIS 검색어: `기업공개 경쟁기업`
- 활용도: 최상
- 연구 적용:
  - 제목 자체가 본 연구와 매우 가깝다.
  - 정보전이 효과와 수요충격효과를 구분한다는 점이 중요하다.
- 본 연구 보완점:
  - LG에너지솔루션, 두산로보틱스, LG CNS 사례를 각각 정보전이와 수요충격 관점으로 해석한다.
  - 예시:
    - 정보전이 효과: IPO 기업의 높은 valuation이 산업 전체 성장 기대를 반영하여 peer도 상승
    - 수요충격 효과: 투자자 자금이 신규 대형 IPO로 이동하면서 기존 peer가 하락
  - 회귀분석 결과를 해석할 때 단순히 "하락했다"가 아니라 "수요충격이 정보전이를 압도했다"는 방식으로 논문식 해석을 만든다.

### 2.5 Chod & Lyandres (2011), "Strategic IPOs and Product Market Competition"

- 출처: Journal of Financial Economics, 100(1), 45-67.
- OASIS 검색어: `IPO competitive effect rival firms`
- 활용도: 높음
- 연구 적용:
  - IPO가 단순 자금조달이 아니라 제품시장 경쟁전략의 일부라는 관점을 제공한다.
  - OpenAI/SpaceX처럼 IPO 이후 대규모 자금조달과 설비투자, 인재 확보, R&D 확대가 예상되는 기업을 해석할 때 특히 유용하다.
- 본 연구 보완점:
  - IPO 이벤트를 금융시장 이벤트이면서 동시에 산업경쟁 구조 변화 신호로 정의한다.
  - Palantir 관점에서는 OpenAI IPO가 AI 응용시장 내 경쟁 심화를 의미하는지, 아니면 AI 산업 전체 TAM 확대로 해석되는지 구분한다.

## 3. 시계열·이벤트 분석에 반영할 문헌

### 3.1 곽형신·여은정, "제19대 대통령선거 관련 정치테마 주식에 대한 사건 연구"

- 출처: KCI 첨부 논문
- 활용도: 높음
- 연구 적용:
  - 정치테마주가 선거일 하루에만 반응하는 것이 아니라 사전 기대 형성, 이벤트 직전 과열, 이벤트 이후 되돌림을 보인다는 점을 참고한다.
  - 본 연구에서도 IPO 당일만 보지 않고, 상장 전 20거래일, 상장 당일, 상장 후 20거래일의 누적 흐름을 시각화한다.
- 본 연구 보완점:
  - CAR 그래프를 단순 선그래프가 아니라 구간별로 나눈다.
    - 기대 형성 구간: -20~-1
    - 이벤트 구간: 0
    - 재평가 구간: +1~+20
  - 각 구간의 평균수익률, 누적수익률, 변동성, 거래대금 변화율을 함께 표로 제시한다.

### 3.2 자본시장연구원 이슈보고서, "대통령 선거 국면의 정치테마주 특징과 시사점"

- 출처: KCMI 이슈보고서 첨부 파일
- 활용도: 중상
- 연구 적용:
  - 특정 정치 이벤트 주변에서 테마성 종목의 가격과 거래대금이 어떻게 동행하는지 분석하는 아이디어를 차용한다.
  - IPO도 투자자 관심이 집중되는 이벤트이므로 가격 반응뿐 아니라 거래대금/변동성 반응을 함께 본다.
- 본 연구 보완점:
  - IPO 전후 peer 그룹의 거래대금 급증 여부를 분석한다.
  - "가격 하락 + 거래대금 증가"는 수급 이동 또는 재평가 압력으로 해석한다.
  - "가격 상승 + 거래대금 증가"는 정보전이 또는 산업 기대 강화로 해석한다.

## 4. 회귀분석·설명변수 확장에 반영할 문헌

### 4.1 확장 회귀식

기본 정상수익률 모형:

```text
r_it = alpha_i + beta_1i * r_mkt,t + beta_2i * r_ind,t + epsilon_it
```

확장 모형:

```text
r_it = alpha_i
     + beta_1i * r_mkt,t
     + beta_2i * r_ind,t
     + beta_3i * SMB_t
     + beta_4i * HML_t
     + beta_5i * MOM_t
     + beta_6i * VOL_t
     + epsilon_it
```

우선 사용자 요구에 맞춰 SMB와 HML을 필수 확장변수로 넣고, MOM과 VOL은 후속 강건성 검정용 후보로 둔다.

### 4.2 변수별 역할

- 시장수익률 `r_mkt,t`: KOSPI 또는 KOSDAQ 수익률
- 산업수익률 `r_ind,t`: 해당 IPO 기업이 속한 산업지수 또는 peer portfolio 수익률
- SMB: 소형주-대형주 프리미엄. 대형 IPO가 시장 내 규모 스타일에 미치는 영향을 통제
- HML: 가치주-성장주 프리미엄. LG CNS, 두산로보틱스처럼 성장주·기술주 성격이 강한 이벤트 해석에 필요
- MOM: 상장 전 산업 모멘텀 통제
- VOL: 이벤트 주변 변동성 확대 통제

### 4.3 가설 검정 방식 보완

기존 가설:

```text
H0: 대형 IPO 이벤트 시 주가지수와 peer 그룹들은 모두 하락한다.
H1: 대형 IPO 이벤트 시 주가지수와 peer 그룹들은 모두 상승한다.
```

논문식으로는 다음처럼 정교화하는 것이 좋다.

```text
H0-1: 대형 IPO 이벤트 주변에서 peer 그룹의 CAR은 0보다 작다.
H1-1: 대형 IPO 이벤트 주변에서 peer 그룹의 CAR은 0보다 크다.

H0-2: 대형 IPO 이벤트 주변에서 시장지수의 누적수익률은 0보다 작다.
H1-2: 대형 IPO 이벤트 주변에서 시장지수의 누적수익률은 0보다 크다.

H0-3: 대형 IPO 이벤트의 수요충격 효과가 정보전이 효과보다 크다.
H1-3: 대형 IPO 이벤트의 정보전이 효과가 수요충격 효과보다 크다.
```

이렇게 바꾸면 단순 방향성 검정에서 끝나지 않고, 왜 그런 방향이 나왔는지 설명할 수 있다.

## 5. 추가 참고 가치가 있는 OASIS 검색 문헌

### 5.1 McGilvery, Faff & Pathan (2012), "Competitive Valuation Effects of Australian IPOs"

- 출처: International Review of Financial Analysis, 24, 74-83.
- OASIS 검색어: `IPO competitive effect rival firms`
- 활용:
  - 미국 외 시장에서 IPO 경쟁효과를 분석한 사례로, 한국 사례와 비교하기 좋다.
  - 표본 수가 작거나 특정 국가 시장을 다룰 때 방법론적 근거로 사용 가능하다.

### 5.2 Pulikottil (2023), "Competitive and Contagion Effect of Initial Public Offerings in India"

- 출처: Social Sciences & Humanities Open, 8(1), 100643.
- OASIS 검색어: `initial public offering industry effect`
- 활용:
  - 신흥시장 또는 비미국 시장에서 contagion effect와 competitive effect를 구분한 문헌이다.
  - 한국 시장을 미국 문헌만으로 설명하기 어려울 때 비교시장 근거로 쓸 수 있다.

### 5.3 Li & Zhang (2021), "Another Game in Town: Spillover Effects of IPOs in China"

- 출처: Journal of Corporate Finance, 67.
- OASIS 검색어: `IPO rival firms`
- 활용:
  - 중국 IPO spillover 분석으로, 대형 IPO가 주변 기업과 시장 attention을 바꾸는 효과를 설명할 때 유용하다.

### 5.4 Jiang, Wu & Zhu (2025), "A Revisit to the IPO Spillover Effect: On the Importance of Technological Proximity"

- 출처: Journal of Banking and Finance, 181.
- OASIS 검색어: `IPO spillover effects`
- 활용:
  - 기술적 근접성이 IPO spillover를 좌우한다는 관점이 OpenAI-Palantir 연결에 매우 잘 맞는다.
  - 본 연구의 peer 그룹 선정 기준을 단순 업종분류가 아니라 사업모델/기술근접성까지 확장하는 근거로 활용한다.

### 5.5 Nguyen, Sutton & Pham (2014), "Intra-Industry Effects of IPOs on Stock Repurchase Decisions of Rival Firms"

- 출처: Journal of Accounting & Finance, 14(4), 61-82.
- OASIS 검색어: `IPO rival firms`
- 활용:
  - IPO가 경쟁기업의 주가뿐 아니라 재무정책에도 영향을 줄 수 있음을 보여준다.
  - 본 연구에서는 직접 분석하지 않더라도 후속 연구 한계와 확장 가능성에 넣기 좋다.

### 5.6 전진규 (2021), "경쟁기업에 대한 애널리스트 투자정보가 신규 상장기업에 미치는 영향"

- 출처: 한국증권학회지, 50(5), 473-496.
- OASIS 검색어: `IPO competitive effect rival firms`
- 활용:
  - 경쟁기업의 정보가 IPO 기업 가격형성에 영향을 준다는 역방향 정보전이 논문이다.
  - 본 연구에서는 IPO 기업의 valuation이 다시 경쟁기업에 영향을 주는 양방향 정보전이 가능성을 논의할 수 있다.

### 5.7 최문수 (2011), "Review of Empirical Studies on IPO Activity and Pricing Behavior in Korea"

- 출처: 재무연구, 24(2).
- OASIS 검색어: `IPO spillover effects`
- 활용:
  - 한국 IPO 연구 흐름을 정리하는 배경문헌으로 적합하다.
  - 서론 또는 선행연구 파트에서 국내 IPO 연구의 중심이 공모가 저평가, 장기성과, 가격형성에 있었고 peer valuation 효과는 상대적으로 덜 다뤄졌다는 논리로 연결한다.

### 5.8 박진우·정준영·김주환 (2017), "Individual Investor Sentiment and IPO Stock Returns: Evidence from the Korean Stock Market"

- 출처: Asia-Pacific Journal of Financial Studies, 46(6).
- OASIS 검색어: `IPO spillover effects`
- 활용:
  - 국내 IPO 시장에서 개인투자자 심리와 수익률의 관계를 설명하는 보조문헌으로 쓸 수 있다.
  - 두산로보틱스와 같은 개인투자자 관심이 큰 IPO 사례 해석에 적합하다.

## 6. 본 연구의 개선된 분석 설계

### 6.1 이벤트 구간

- 추정기간: 상장일 기준 -250~-20 거래일
- 이벤트 분석기간: -20~+20 거래일
- 단기 창: -1~+1, 0~+1
- 중기 창: -5~+5, 0~+10
- 비교 창: -20~-1, +1~+20

### 6.2 그래프 구성

- IPO별 peer 기업 주가의 이벤트일 기준 정규화 지수 그래프
- 시장지수와 산업지수의 이벤트일 기준 정규화 지수 그래프
- AR 막대그래프
- CAR 누적 선그래프
- 거래대금 변화율 그래프
- 이벤트 전후 변동성 비교 그래프

### 6.3 테이블 구성

- 사건별 기본 정보: IPO 기업, 상장일, 공모금액, 시가총액, 산업, peer 기업
- 회귀계수 추정표: alpha, market beta, industry beta, SMB beta, HML beta, R-squared
- AR/CAR 검정표: 각 이벤트 창별 CAR, t-stat, p-value
- 가설 검정 요약표: 시장지수 방향, peer 평균 방향, peer 전원 동일 방향 여부, 결론
- 해석 분류표: 정보전이, 수요충격, 경쟁효과, 산업추세 중 어느 효과가 우세한지

## 7. 현재 사례별 예상 해석 방향

### 7.1 LG에너지솔루션 IPO

- 현재 분석 결과는 시장수익률과 peer 평균 CAR이 모두 음의 방향이다.
- 대형 IPO로 인한 수급 부담과 기존 2차전지 관련주의 valuation 재조정 가능성이 크다.
- 해석: 수요충격 및 경쟁효과가 정보전이 효과를 압도한 사례.

### 7.2 두산로보틱스 IPO

- 시장은 하락했지만 peer 기업 반응은 혼재되어 있다.
- 로봇 산업 성장 기대와 개별 기업 펀더멘털 차이가 동시에 작동했을 가능성이 있다.
- 해석: 산업 전망 개선과 수요충격이 혼재된 사례.

### 7.3 LG CNS IPO

- AI·클라우드·DX 산업 기대가 peer 기업으로 전이되는지 확인하는 사례다.
- 신규 대형 IT 서비스 기업이 등장하면서 기존 IT 서비스 peer의 상대 valuation이 재평가될 수 있다.
- 해석: 정보전이 효과와 경쟁효과가 혼재될 가능성이 큰 사례.

## 8. 논문 구조 제안

1. 서론
   - Palantir 투자자 관점의 문제의식
   - OpenAI/SpaceX IPO 가능성과 관련 상장기업 valuation 질문
   - 국내 대형 IPO를 이용한 실증분석의 필요성

2. 선행연구
   - IPO의 산업 내 파급효과
   - 경쟁기업 valuation 효과
   - 정보전이와 수요충격
   - 이벤트 연구와 정치테마주 시계열 분석

3. 연구가설
   - 대형 IPO 이벤트의 peer CAR 방향성
   - 시장지수 방향성
   - 정보전이 대 수요충격의 상대적 우세

4. 자료 및 표본
   - LG에너지솔루션, 두산로보틱스, LG CNS
   - peer 그룹 선정 기준
   - 시장지수, 산업지수, SMB, HML

5. 연구방법론
   - 이벤트 스터디
   - 다중회귀 정상수익률 모형
   - AR/CAR 산출
   - 가설검정

6. 실증분석 결과
   - 이벤트 전후 그래프
   - 회귀분석 결과표
   - CAR 검정표
   - 사례별 해석

7. 결론
   - 한국 대형 IPO의 peer valuation 효과
   - Palantir-OpenAI/SpaceX 사례에 대한 시사점
   - 한계 및 후속 연구

## 9. 바로 다음 작업 제안

1. 위 문헌을 바탕으로 `README.md`의 연구계획을 논문형 목차로 재정리한다.
2. 기존 `scripts/regression_analysis.py`에 SMB, HML 더미/프록시 변수를 추가한다.
3. 이벤트 전후 그래프를 더 자세히 나눈 HTML 리포트를 다시 생성한다.
4. OASIS에서 최우선 문헌 4개를 개인 열람용으로 확보한 뒤 인용정보를 정확히 정리한다.
