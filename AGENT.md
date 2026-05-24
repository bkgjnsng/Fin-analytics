# AGENT.md

## Working Rules

- Respond in Korean.
- Do not store or print API keys, OASIS credentials, passwords, or private tokens.
- Do not commit or push unless the user explicitly asks.
- Prefer concise research-oriented outputs: tables, figures, regression results, and paper-style writing.
- Treat current empirical results as provisional. Re-run scripts before final reporting.

## Project Goal

Research question:

> How do expectations or events around large unicorn IPOs affect the valuation of related listed firms?

Motivation:

The user holds Palantir and wants to infer how OpenAI, SpaceX, or Anthropic IPOs could affect Palantir, related peer firms, and indices. The empirical design now uses Korean cases for accessible domestic evidence and US cases as closer analogues to AI/software/EV mega-IPOs.

Main cases:

- LG Energy Solution
- Doosan Robotics
- LG CNS
- Arm Holdings
- Snowflake
- Rivian

## Methodology

Use event study and multiple regression.

Estimation window:

- IPO date -250 to -20 trading days

Event window:

- -20 to +20 trading days
- Key windows: -1~+1, 0~+1, 0~+5, 0~+20, 0~+60, 0~+120

Baseline model:

```text
r_i,t = alpha_i + beta_1i * r_mkt,t + beta_2i * r_ind,t + epsilon_i,t
```

Expanded model:

```text
r_i,t = alpha_i
      + beta_1i * r_mkt,t
      + beta_2i * r_ind,t
      + beta_3i * SMB_t
      + beta_4i * HML_t
      + epsilon_i,t
```

Compute:

- AR
- CAR
- peer portfolio CAR
- market/index return
- volume and volatility where possible

## Hypotheses

User's original hypotheses:

- H1: Demand shock causes indices and peer groups to fall.
- H0_1: Indices and peer groups do not fall.
- H2: Information transfer causes peer groups to rise.
- H0_2: Peer groups do not rise through information transfer.
- H3: Competition effect causes rival firms to fall.
- H0_3: Rival firms do not fall through competition effect.

Recommended paper-style framing:

- Test whether peer CAR around IPO events is significantly different from zero.
- Interpret the sign using information transfer, competitive effect, demand shock, and industry trend.

## Key Literature

Detailed notes are in:

- `docs/literature_review_candidates.md`
- `docs/deep_literature_review.md`

Most important papers:

- Spiegel & Tookes (2020), "Why Does an IPO Affect Rival Firms?"
- Akhigbe, Borde & Whyte (2003), "Does an Industry Effect Exist for Initial Public Offerings?"
- 민재훈 (2020), "IPO가 경쟁기업의 주가에 미치는 영향"
- Kang & Lim (2011), "The Impact of IPOs on Rival Firms: Evidence from KOSDAQ Market"
- 전진규 (2021), "경쟁기업에 대한 애널리스트 투자정보가 신규 상장기업에 미치는 영향"
- Political theme stock event-study papers for time-series/event-window design

## Important Files

Scripts:

- `scripts/build_report.py`
- `scripts/regression_analysis.py`
- `scripts/public_data_api.py`
- `scripts/build_research_paper.py`
- `scripts/case_config.py`

Reports:

- `docs/best_practice_research_plan.md`
- `reports/ipo_event_study_report.html`
- `reports/ipo_regression_analysis.html`
- `reports/ipo_unicorn_valuation_paper.pdf`

Data:

- `data/event_summary.csv`
- `data/event_window_prices.csv`
- `data/regression_results.csv`
- `data/hypothesis_test_summary.csv`
- `data/literature_extracts/`

Literature PDFs:

- `literature/`

## Current Findings

Current results suggest:

- LG Energy Solution: market and peer CAR both negative; H1 demand shock and H3 competition effect are supported.
- Doosan Robotics: market negative and peer average CAR negative, but individual peers are mixed; H1/H3 are directionally supported with caution.
- LG CNS: peer average CAR positive, but signs are mixed, so no single mechanism is strongly supported.
- Arm Holdings, Snowflake, Rivian: peer average CAR is positive in the current [0,+20] window; H2 information transfer is supported.

Use these as provisional results only.

## Public Data API Status

The public data portal stock API integration exists in `scripts/public_data_api.py`.

- API key must be passed through `DATA_GO_KR_SERVICE_KEY`.
- Do not hardcode the key.
- Earlier tests returned `HTTP 401 Unauthorized`, so current results mostly rely on Naver Finance fallback data.

## Next Tasks

1. Add announcement-date event windows when reliable event dates are collected.
2. Add volume and volatility analysis.
3. Build or source Korean daily SMB/HML factors; currently SMB/HML is implemented for US cases only.
4. Add valuation multiple data if FnGuide/KRX/fundamental sources become available.
5. Convert results into 10-12 presentation slides.
