from __future__ import annotations

import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

import pandas as pd

from build_report import Asset, fetch_prices as fetch_naver_prices


PUBLIC_DATA_ENDPOINT = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"


def _service_key() -> str:
    key = os.environ.get("DATA_GO_KR_SERVICE_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "DATA_GO_KR_SERVICE_KEY environment variable is required for the public data portal stock API."
        )
    return key


def _service_key_candidates() -> list[str]:
    key = _service_key()
    decoded = urllib.parse.unquote(key)
    encoded = urllib.parse.quote(decoded, safe="")
    candidates = [key, decoded, encoded]
    unique: list[str] = []
    for candidate in candidates:
        if candidate not in unique:
            unique.append(candidate)
    return unique


def _parse_number(value: str | None) -> float:
    if value is None:
        return float("nan")
    clean = value.replace(",", "").strip()
    if not clean:
        return float("nan")
    return float(clean)


def fetch_public_stock_prices(asset: Asset, start: datetime, end: datetime) -> pd.DataFrame:
    last_error: Exception | None = None
    root: ET.Element | None = None
    for service_key in _service_key_candidates():
        params = {
            "serviceKey": service_key,
            "numOfRows": "10000",
            "pageNo": "1",
            "resultType": "xml",
            "beginBasDt": start.strftime("%Y%m%d"),
            "endBasDt": end.strftime("%Y%m%d"),
            "likeSrtnCd": asset.code,
        }
        url = PUBLIC_DATA_ENDPOINT + "?" + urllib.parse.urlencode(params, safe="%")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            raw = urllib.request.urlopen(req, timeout=30).read()
            root = ET.fromstring(raw)
            break
        except Exception as exc:
            last_error = exc

    if root is None:
        raise RuntimeError(f"Public data API request failed for {asset.code}") from last_error

    result_code = root.findtext(".//resultCode")
    if result_code not in (None, "00"):
        result_message = root.findtext(".//resultMsg") or "Unknown API error"
        raise RuntimeError(f"Public data API error for {asset.code}: {result_code} {result_message}")

    rows = []
    for item in root.findall(".//item"):
        code = item.findtext("srtnCd")
        if code != asset.code:
            continue
        rows.append(
            {
                "date": pd.to_datetime(item.findtext("basDt"), format="%Y%m%d"),
                "open": _parse_number(item.findtext("mkp")),
                "high": _parse_number(item.findtext("hipr")),
                "low": _parse_number(item.findtext("lopr")),
                "close": _parse_number(item.findtext("clpr")),
                "volume": _parse_number(item.findtext("trqu")),
                "market_cap": _parse_number(item.findtext("mrktTotAmt")),
                "listed_shares": _parse_number(item.findtext("lstgStCnt")),
                "code": asset.code,
                "name": asset.name,
                "source": "data.go.kr",
            }
        )

    if not rows:
        raise ValueError(f"No public data portal price rows returned for {asset.code} {asset.name}")

    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def fetch_prices(asset: Asset, start: datetime, end: datetime) -> pd.DataFrame:
    if asset.market == "Index" or asset.code in {"KOSPI", "KOSDAQ"}:
        frame = fetch_naver_prices(asset, start, end)
        frame["source"] = "naver-index-fallback"
        return frame
    return fetch_public_stock_prices(asset, start, end)
