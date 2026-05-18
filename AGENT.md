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

The user holds Palantir and wants to infer how OpenAI or SpaceX IPOs could affect Palantir and related indices. Because Korean data is easier to access and the domestic literature is thinner on this exact topic, the empirical analysis uses Korean IPO cases.

Main cases:

- LG Energy Solution
- Doosan Robotics
- LG CNS

## Methodology

Use event study and multiple regression.

Estimation window:

- IPO date -250 to -20 trading days

Event window:

- -20 to +20 trading days
- Key windows: -5~-1, -1~+1, 0, 0~+5, 0~+10, 0~+20

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

- H0: Large IPO events cause both market indices and peer groups to fall.
- H1: Large IPO events cause both market indices and peer groups to rise.

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

Reports:

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

- LG Energy Solution: market and peer CAR both negative; most consistent with competitive effect or valuation re-rating.
- Doosan Robotics: market negative, peer reaction mixed; information transfer and competitive effect are both plausible.
- LG CNS: analyze AI/cloud/DX peer reaction with Samsung SDS, Hyundai AutoEver, and POSCO DX. Re-run scripts before reporting.

Use these as provisional results only.

## Public Data API Status

The public data portal stock API integration exists in `scripts/public_data_api.py`.

- API key must be passed through `DATA_GO_KR_SERVICE_KEY`.
- Do not hardcode the key.
- Earlier tests returned `HTTP 401 Unauthorized`, so current results mostly rely on Naver Finance fallback data.

## Next Tasks

1. Add SMB and HML proxies to `scripts/regression_analysis.py`.
2. Improve event-window graphs by separating -20~-1, 0, +1~+20.
3. Add volume and volatility analysis.
4. Update the HTML report with literature-based interpretation.
5. Convert results into paper structure: introduction, literature review, hypotheses, data, methodology, results, conclusion.
