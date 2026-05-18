from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
DATA_DIR = ROOT / "data"
FONT_DIR = Path("C:/Windows/Fonts")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("PaperSerif", str(FONT_DIR / "NanumMyeongjo.ttf")))
    pdfmetrics.registerFont(TTFont("PaperSerifBold", str(FONT_DIR / "NanumMyeongjoBold.ttf")))
    pdfmetrics.registerFont(TTFont("PaperSans", str(FONT_DIR / "NanumGothic.ttf")))
    pdfmetrics.registerFont(TTFont("PaperSansBold", str(FONT_DIR / "NanumGothicBold.ttf")))


def pct(value: float | str, digits: int = 2) -> str:
    try:
        return f"{float(value) * 100:.{digits}f}%"
    except Exception:
        return "-"


def num(value: float | str, digits: int = 3) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "-"


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def make_table(data: list[list[str]], col_widths: list[float] | None = None, font_size: int = 8) -> Table:
    table = Table(data, colWidths=col_widths, repeatRows=1, hAlign="CENTER")
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), "PaperSansBold"),
                ("FONTNAME", (0, 1), (-1, -1), "PaperSans"),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3f66")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#b8c2cc")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f7f9fc"), colors.white]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("PaperSans", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(A4[0] / 2, 12 * mm, str(doc.page))
    canvas.restoreState()


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "journal": ParagraphStyle(
            "journal",
            parent=base["Normal"],
            fontName="PaperSans",
            fontSize=8.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=8,
        ),
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="PaperSerifBold",
            fontSize=18,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=8,
        ),
        "author": ParagraphStyle(
            "author",
            parent=base["Normal"],
            fontName="PaperSansBold",
            fontSize=10.5,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "affil": ParagraphStyle(
            "affil",
            parent=base["Normal"],
            fontName="PaperSans",
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=12,
        ),
        "abstract": ParagraphStyle(
            "abstract",
            parent=base["Normal"],
            fontName="PaperSerif",
            fontSize=9.2,
            leading=15,
            alignment=TA_JUSTIFY,
            leftIndent=8,
            rightIndent=8,
            spaceAfter=6,
        ),
        "keyword": ParagraphStyle(
            "keyword",
            parent=base["Normal"],
            fontName="PaperSans",
            fontSize=8.7,
            leading=13,
            leftIndent=8,
            rightIndent=8,
            spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="PaperSerifBold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#0f2f55"),
            spaceBefore=14,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="PaperSansBold",
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#1f3f66"),
            spaceBefore=9,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="PaperSerif",
            fontSize=9.5,
            leading=15.5,
            firstLineIndent=12,
            alignment=TA_JUSTIFY,
            spaceAfter=5,
        ),
        "body_noindent": ParagraphStyle(
            "body_noindent",
            parent=base["BodyText"],
            fontName="PaperSerif",
            fontSize=9.5,
            leading=15.5,
            alignment=TA_JUSTIFY,
            spaceAfter=5,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="PaperSansBold",
            fontSize=8.7,
            leading=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#0f2f55"),
            spaceBefore=8,
            spaceAfter=3,
        ),
        "note": ParagraphStyle(
            "note",
            parent=base["Normal"],
            fontName="PaperSans",
            fontSize=7.8,
            leading=11,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=8,
        ),
        "formula": ParagraphStyle(
            "formula",
            parent=base["Normal"],
            fontName="PaperSerif",
            fontSize=10.5,
            leading=15,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=4,
        ),
    }


def main() -> None:
    register_fonts()
    REPORT_DIR.mkdir(exist_ok=True)

    hypothesis = pd.read_csv(DATA_DIR / "hypothesis_test_summary.csv")
    regressions = pd.read_csv(DATA_DIR / "regression_results.csv")

    styles = build_styles()
    output = REPORT_DIR / "ipo_unicorn_valuation_paper.pdf"
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title="대형 IPO 이벤트와 관련 상장기업 Valuation 반응",
        author="Fin analytics",
    )

    story = []
    story.append(p("금융애널리틱스 연구보고서", styles["journal"]))
    story.append(p("대형 비상장 유니콘의 IPO 기대가 관련 상장기업 Valuation에 미치는 영향", styles["title"]))
    story.append(p("국내 대형 IPO 사례를 활용한 사건연구", styles["author"]))
    story.append(p("작성자: Fin analytics 프로젝트 · 자료 기준: 2022-2025년 국내 IPO 사례", styles["affil"]))

    story.append(p("<b>초록</b>", styles["keyword"]))
    story.append(
        p(
            "본 연구는 대형 비상장 유니콘의 기업공개(IPO)가 현실화될 때 동일 산업 또는 관련 상장기업의 "
            "valuation이 어떻게 재평가되는지를 국내 대형 IPO 사례를 통해 분석한다. 분석 대상은 LG에너지솔루션, "
            "두산로보틱스, LG CNS의 상장 이벤트이며, 각 사건에 대해 동일 산업 peer 기업과 시장지수의 반응을 "
            "비교하였다. 방법론은 정치테마주 및 IPO 산업효과 문헌에서 사용되는 사건연구 구조를 따른다. 상장일을 "
            "t=0으로 정의하고, t-250부터 t-20까지의 추정기간에서 시장수익률 및 산업수익률을 설명변수로 하는 "
            "정상수익률 회귀식을 추정한 뒤, 이벤트 기간의 초과수익률(AR)과 누적초과수익률(CAR)을 계산하였다. "
            "실증분석 결과, LG에너지솔루션 사례에서는 시장지수와 모든 peer 기업의 이벤트 반응이 음(-)으로 나타나 "
            "하락 가설이 지지되었다. 반면 두산로보틱스와 LG CNS 사례에서는 일부 peer 기업이 양(+)의 CAR을 보일 수 있어 "
            "일괄적 하락 또는 상승 가설을 지지하기 어렵다. 이는 대형 IPO가 산업 전체에 단일한 방향의 영향을 주기보다, "
            "정보효과와 경쟁효과가 기업별로 혼재되어 나타날 수 있음을 시사한다.",
            styles["abstract"],
        )
    )
    story.append(
        p(
            "<b>주제어:</b> IPO, 유니콘, 사건연구, 초과수익률, CAR, 산업효과, valuation",
            styles["keyword"],
        )
    )

    story.append(p("Ⅰ. 서론", styles["h1"]))
    story.append(
        p(
            "OpenAI, SpaceX와 같은 대형 비상장 유니콘의 상장 가능성은 해당 기업만의 자금조달 이벤트가 아니라 "
            "동일 산업의 성장성, 경쟁구도, 투자자 관심을 동시에 재평가하게 만드는 시장 이벤트로 이해될 수 있다. "
            "기존 IPO 연구는 상장기업 자체의 저평가 또는 상장 후 성과를 중심으로 전개되어 왔지만, 대형 IPO가 "
            "동일 산업의 기존 상장기업에 미치는 파급효과 역시 중요한 분석 대상이다.",
            styles["body"],
        )
    )
    story.append(
        p(
            "본 연구는 국내 시장에서 관찰 가능한 세 개의 대형 IPO 사례를 이용해 이 문제를 검토한다. 특히 "
            "LG에너지솔루션, 두산로보틱스, LG CNS는 각각 2차전지, 로봇, AI·클라우드·디지털전환 산업에서 투자자 관심이 높았던 "
            "대형 상장 사례라는 점에서 유니콘 또는 초대형 성장기업 IPO의 시장 파급효과를 관찰하기에 적절하다.",
            styles["body"],
        )
    )

    story.append(p("Ⅱ. 선행연구와 벤치마킹 방향", styles["h1"]))
    story.append(
        p(
            "곽형신·여은정(2019)은 제19대 대통령선거 관련 정치테마주를 대상으로 시장모형, Fama-French 3요인 "
            "모형, 모멘텀을 포함한 4요인 모형을 적용하여 단기 및 장기 CAR을 비교하였다. 이 연구의 핵심은 "
            "특정 이벤트 전후의 비정상수익률이 일시적으로 형성되더라도 시간이 지나며 소멸하거나 후보별·모형별로 "
            "다르게 나타난다는 점이다. 본 연구는 이 구조를 차용해 IPO 상장일을 사건일로 두고, 관련 상장기업의 "
            "AR과 CAR을 산출한다.",
            styles["body"],
        )
    )
    story.append(
        p(
            "남길남(2017)의 자본시장연구원 이슈보고서는 정치테마주가 본질가치와 무관하게 이상급등하거나 "
            "개인투자자 손실 및 불공정거래 위험과 연결될 수 있음을 강조한다. 본 연구는 이 보고서의 정책적 "
            "시사점 구조를 참고하여, 대형 IPO 기대가 투자자 관심을 과도하게 특정 테마로 이동시키는지, 그리고 "
            "관련 상장기업에 일관된 재평가를 발생시키는지에 초점을 둔다.",
            styles["body"],
        )
    )

    story.append(p("Ⅲ. 연구가설", styles["h1"]))
    story.append(
        p(
            "본 연구의 귀무가설과 대립가설은 사용자가 제시한 방향성 가설을 그대로 따른다. 일반적인 통계학의 "
            "무효과 귀무가설과는 다르며, 사건 발생 시 시장과 peer 그룹의 수익률 방향이 모두 하락 또는 모두 상승하는지를 "
            "검정하는 방향성 가설이다.",
            styles["body"],
        )
    )
    story.append(p("H0: 대형 IPO 이벤트 시 주가지수와 동일 peer 그룹들은 모두 하락한다.", styles["body_noindent"]))
    story.append(p("H1: 대형 IPO 이벤트 시 주가지수와 동일 peer 그룹들은 모두 상승한다.", styles["body_noindent"]))

    story.append(p("Ⅳ. 자료 및 방법론", styles["h1"]))
    case_table = [
        ["사례", "상장일", "산업", "IPO 기업", "비교 peer"],
        ["LG에너지솔루션", "2022-01-27", "2차전지", "LG Energy Solution", "LG Chem, Samsung SDI, SK Innovation"],
        ["두산로보틱스", "2023-10-05", "로봇", "Doosan Robotics", "Doosan Corp, Rainbow Robotics, Robostar"],
        ["LG CNS", "2025-02-05", "AI·클라우드·DX", "LG CNS", "Samsung SDS, Hyundai AutoEver, POSCO DX"],
    ]
    story.append(p("표 1. 분석 대상 IPO와 peer 기업", styles["caption"]))
    story.append(make_table(case_table, [28 * mm, 24 * mm, 24 * mm, 34 * mm, 60 * mm], 7.5))
    story.append(
        p(
            "자료는 현 단계에서 무료 일별 가격자료를 이용하였다. 공공데이터포털 주식시세정보 API는 코드에 연동되어 "
            "있으나, 인증키 활성화 문제로 최종 PDF 산출 시점에는 기존 일별 가격자료를 사용하였다. 추후 인증키가 "
            "정상 작동하면 동일 스크립트로 공식 API 기반 결과를 재생성할 수 있다.",
            styles["note"],
        )
    )
    story.append(p("정상수익률 추정식은 다음과 같다.", styles["body_noindent"]))
    story.append(p("r<sub>i,t</sub> = α<sub>i</sub> + β<sub>1,i</sub> r<sub>mkt,t</sub> + β<sub>2,i</sub> r<sub>ind,t</sub> + ε<sub>i,t</sub>", styles["formula"]))
    story.append(p("AR<sub>i,t</sub> = r<sub>i,t</sub> - (α̂<sub>i</sub> + β̂<sub>1,i</sub> r<sub>mkt,t</sub> + β̂<sub>2,i</sub> r<sub>ind,t</sub>)", styles["formula"]))
    story.append(p("CAR<sub>i,[a,b]</sub> = Σ AR<sub>i,t</sub>, t ∈ [a,b]", styles["formula"]))
    story.append(
        p(
            "추정기간은 상장일 기준 -250거래일부터 -20거래일까지이며, 분석구간은 [-1,+1], [0,+5], [0,+20]으로 "
            "구성하였다. r_mkt는 각 종목이 속한 KOSPI 또는 KOSDAQ 수익률을 사용하고, r_ind는 동일 IPO 사례의 "
            "peer 평균수익률을 사용하였다. 단, 개별 peer 회귀분석에서는 자기 자신을 산업수익률 계산에서 제외하였다.",
            styles["body"],
        )
    )

    story.append(p("Ⅴ. 실증분석 결과", styles["h1"]))
    h_rows = [["사례", "시장수익률 [0,+20]", "peer 평균 CAR [0,+20]", "peer CAR 방향", "판정"]]
    for row in hypothesis.itertuples():
        h_rows.append([row.case, pct(row.market_return_0_20), pct(row.peer_avg_car_0_20), row.peer_car_signs, row.result])
    story.append(p("표 2. 가설검정 요약", styles["caption"]))
    story.append(make_table(h_rows, [46 * mm, 30 * mm, 34 * mm, 28 * mm, 32 * mm], 7.6))
    story.append(
        p(
            "표 2에 따르면 LG에너지솔루션 사례는 시장수익률과 세 peer 기업의 CAR이 모두 음(-)으로 나타나 H0를 "
            "지지한다. 두산로보틱스와 LG CNS 사례에서는 시장지수와 peer 기업의 방향이 서로 다르게 나타날 수 있어 "
            "나타나 H0 또는 H1을 일괄적으로 지지하지 않는다.",
            styles["body"],
        )
    )

    reg_rows = [["사례", "peer", "β_mkt", "β_ind", "R²", "CAR [0,+20]", "t", "p"]]
    for row in regressions.itertuples():
        reg_rows.append(
            [
                str(row.case).replace(" IPO", ""),
                row.asset,
                num(row.beta_market),
                num(row.beta_industry),
                num(row.r_squared),
                pct(row.car_0_p20),
                num(row.t_0_p20),
                num(row.p_0_p20),
            ]
        )
    story.append(p("표 3. 개별 peer 회귀계수와 이벤트 CAR", styles["caption"]))
    story.append(make_table(reg_rows, [34 * mm, 30 * mm, 18 * mm, 18 * mm, 16 * mm, 24 * mm, 14 * mm, 16 * mm], 7.0))
    story.append(
        p(
            "개별 종목 기준으로는 두산 Corp의 CAR이 -35.02%(t=-2.743), NCSoft의 CAR이 -23.16%(t=-2.578)로 "
            "통계적으로 강한 음(-)의 반응을 보였다. 반면 Rainbow Robotics와 Pearl Abyss는 양(+)의 CAR을 기록하여, "
            "대형 IPO가 항상 기존 peer 기업을 압박한다는 단순한 경쟁효과만으로 설명되기 어렵다.",
            styles["body"],
        )
    )

    story.append(p("Ⅵ. 논의", styles["h1"]))
    story.append(
        p(
            "본 연구의 결과는 IPO 이벤트가 관련 상장기업에 두 가지 상반된 경로로 작동할 수 있음을 시사한다. 첫째, "
            "정보효과는 대형 IPO가 해당 산업의 성장성과 투자자 관심을 확인시켜 peer 기업의 valuation을 끌어올리는 "
            "경로이다. 둘째, 경쟁효과는 신규 상장기업이 자본조달 능력과 시장 주목도를 확보함으로써 기존 상장기업의 "
            "상대적 매력도를 낮추는 경로이다. 두산로보틱스와 LG CNS 사례에서 혼합 결과가 나타난 것은 이 두 효과가 "
            "기업별 특성과 투자자 인식에 따라 다르게 결합되기 때문으로 해석할 수 있다.",
            styles["body"],
        )
    )
    story.append(
        p(
            "정치테마주 문헌이 이벤트 전 과열과 이벤트 후 소멸을 강조한다면, 본 연구의 IPO 사례는 테마성 관심이 "
            "산업 재평가로 이어질 수는 있으나 모든 peer에 동일하게 전달되지는 않는다는 점을 보여준다. 따라서 "
            "OpenAI나 SpaceX와 같은 초대형 비상장 유니콘의 상장 가능성을 분석할 때에도 단순히 같은 산업이라는 이유만으로 "
            "상장 peer 전체가 같은 방향으로 움직인다고 가정하기보다, 기업별 경쟁지위와 산업 내 대체관계를 함께 고려해야 한다.",
            styles["body"],
        )
    )

    story.append(p("Ⅶ. 결론", styles["h1"]))
    story.append(
        p(
            "본 연구는 국내 세 개 대형 IPO를 대상으로 관련 상장기업의 valuation 반응을 사건연구 방식으로 분석하였다. "
            "세 사례 전체를 종합하면, 대형 IPO 이벤트가 시장지수와 모든 peer 기업을 일괄적으로 하락 또는 상승시킨다는 "
            "강한 방향성 가설은 지지되지 않는다. 다만 LG에너지솔루션 사례에서는 H0가 지지되어, 대형 IPO가 기존 peer의 "
            "투자 매력도를 낮추는 경쟁효과가 뚜렷하게 나타날 수 있음을 확인하였다.",
            styles["body"],
        )
    )
    story.append(
        p(
            "향후 연구에서는 공공데이터포털 API 인증이 정상화된 뒤 공식 KRX 기반 가격자료로 결과를 재산출하고, "
            "PER, PBR, EV/EBITDA 등 valuation multiple의 일별 또는 월별 변화를 결합할 필요가 있다. 또한 OpenAI와 "
            "SpaceX 같은 글로벌 유니콘 사례로 확장하려면, 직접 상장 전 기대 구간과 관련 상장기업의 산업 노출도를 "
            "더 정교하게 측정하는 작업이 요구된다.",
            styles["body"],
        )
    )

    story.append(PageBreak())
    story.append(p("참고문헌", styles["h1"]))
    references = [
        "곽형신·여은정, 2019, 「제19대 대통령선거 관련 정치테마 주식에 대한 사건 연구」, 재무관리연구 36(2), 209-245.",
        "남길남, 2017, 「대통령 선거 국면의 정치테마주 특징과 시사점」, 자본시장연구원 이슈보고서 17-04.",
        "Brown, S. J. and Warner, J. B., 1985, Using daily stock returns: The case of event studies, Journal of Financial Economics 14, 3-31.",
        "Ritter, J. R., 1991, The long-run performance of initial public offerings, Journal of Finance 46, 3-27.",
        "Lang, L. H. P. and Stulz, R. M., 1992, Contagion and competitive intra-industry effects of bankruptcy announcements, Journal of Financial Economics 32, 45-60.",
    ]
    for ref in references:
        story.append(p(ref, styles["body_noindent"]))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(output)


if __name__ == "__main__":
    main()
