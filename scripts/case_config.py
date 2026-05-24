from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Asset:
    code: str
    name: str
    market: str


@dataclass(frozen=True)
class EventCase:
    key: str
    name: str
    listing_date: str
    industry: str
    ipo: Asset
    benchmark: Asset
    peers: tuple[Asset, ...]
    region: str
    thesis: str


ESTIMATION_START = -250
ESTIMATION_END = -20

EVENT_WINDOWS = [(-1, 1), (0, 1), (0, 5), (0, 20), (0, 60), (0, 120)]

CASES = [
    EventCase(
        key="lg_energy_solution",
        name="LG Energy Solution IPO",
        listing_date="2022-01-27",
        industry="Secondary battery / EV battery",
        ipo=Asset("373220", "LG Energy Solution", "KOSPI"),
        benchmark=Asset("KOSPI", "KOSPI", "Index"),
        peers=(
            Asset("051910", "LG Chem", "KOSPI"),
            Asset("006400", "Samsung SDI", "KOSPI"),
            Asset("096770", "SK Innovation", "KOSPI"),
        ),
        region="KR",
        thesis="Mega battery IPO; useful for demand-shock and peer valuation repricing.",
    ),
    EventCase(
        key="doosan_robotics",
        name="Doosan Robotics IPO",
        listing_date="2023-10-05",
        industry="Robotics / automation",
        ipo=Asset("454910", "Doosan Robotics", "KOSPI"),
        benchmark=Asset("KOSPI", "KOSPI", "Index"),
        peers=(
            Asset("000150", "Doosan Corp", "KOSPI"),
            Asset("277810", "Rainbow Robotics", "KOSDAQ"),
            Asset("090360", "Robostar", "KOSDAQ"),
        ),
        region="KR",
        thesis="Growth-theme IPO; useful for information-transfer versus competition effects.",
    ),
    EventCase(
        key="lg_cns",
        name="LG CNS IPO",
        listing_date="2025-02-05",
        industry="AI / cloud / digital transformation",
        ipo=Asset("064400", "LG CNS", "KOSPI"),
        benchmark=Asset("KOSPI", "KOSPI", "Index"),
        peers=(
            Asset("018260", "Samsung SDS", "KOSPI"),
            Asset("307950", "Hyundai AutoEver", "KOSPI"),
            Asset("022100", "POSCO DX", "KOSPI"),
        ),
        region="KR",
        thesis="Domestic AI/cloud/DX case; closest Korean analogue to AI-platform IPO spillovers.",
    ),
    EventCase(
        key="arm_holdings",
        name="Arm Holdings IPO",
        listing_date="2023-09-14",
        industry="Semiconductor IP / AI infrastructure",
        ipo=Asset("ARM.US", "Arm Holdings", "NASDAQ"),
        benchmark=Asset("QQQ.US", "Nasdaq 100 ETF", "US ETF"),
        peers=(
            Asset("AMD.US", "AMD", "NASDAQ"),
            Asset("QCOM.US", "Qualcomm", "NASDAQ"),
            Asset("AVGO.US", "Broadcom", "NASDAQ"),
            Asset("SNPS.US", "Synopsys", "NASDAQ"),
            Asset("CDNS.US", "Cadence", "NASDAQ"),
        ),
        region="US",
        thesis="Large AI-infrastructure IPO; useful for semiconductor ecosystem repricing.",
    ),
    EventCase(
        key="snowflake",
        name="Snowflake IPO",
        listing_date="2020-09-16",
        industry="Cloud data platform / software",
        ipo=Asset("SNOW.US", "Snowflake", "NYSE"),
        benchmark=Asset("QQQ.US", "Nasdaq 100 ETF", "US ETF"),
        peers=(
            Asset("DDOG.US", "Datadog", "NASDAQ"),
            Asset("MDB.US", "MongoDB", "NASDAQ"),
            Asset("CRM.US", "Salesforce", "NYSE"),
            Asset("NOW.US", "ServiceNow", "NYSE"),
            Asset("ORCL.US", "Oracle", "NYSE"),
        ),
        region="US",
        thesis="Largest software IPO of its time; useful analogue for AI/software valuation resets.",
    ),
    EventCase(
        key="rivian",
        name="Rivian IPO",
        listing_date="2021-11-10",
        industry="Electric vehicles / mobility",
        ipo=Asset("RIVN.US", "Rivian", "NASDAQ"),
        benchmark=Asset("SPY.US", "S&P 500 ETF", "US ETF"),
        peers=(
            Asset("TSLA.US", "Tesla", "NASDAQ"),
            Asset("F.US", "Ford", "NYSE"),
            Asset("GM.US", "General Motors", "NYSE"),
            Asset("NIO.US", "NIO", "NYSE"),
            Asset("XPEV.US", "XPeng", "NYSE"),
        ),
        region="US",
        thesis="EV unicorn IPO; useful for competition effect and growth-stock demand shock.",
    ),
]


def is_korean_asset(asset: Asset) -> bool:
    return asset.code in {"KOSPI", "KOSDAQ"} or asset.code.isdigit()


def is_us_case(case: EventCase) -> bool:
    return case.region.upper() == "US"
