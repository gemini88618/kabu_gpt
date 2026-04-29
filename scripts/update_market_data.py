import json
import math
import io
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import urlopen

JPX_LIST_URL = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
JP_FALLBACK_COUNT = 1000
US_TARGET_COUNT = 500

JP_SEED = [
    ("7203.T", "Toyota Motor"),
    ("6758.T", "Sony Group"),
    ("8035.T", "Tokyo Electron"),
    ("9984.T", "SoftBank Group"),
    ("6861.T", "Keyence"),
    ("7974.T", "Nintendo"),
    ("6098.T", "Recruit Holdings"),
    ("4063.T", "Shin-Etsu Chemical"),
    ("6501.T", "Hitachi"),
    ("8058.T", "Mitsubishi Corp"),
    ("8306.T", "Mitsubishi UFJ Financial Group"),
    ("9432.T", "Nippon Telegraph and Telephone"),
]

JP_PRIORITY_SYMBOLS = """
7203.T 6758.T 8306.T 8035.T 9984.T 6861.T 7974.T 9432.T 4063.T 6501.T
8058.T 9983.T 6098.T 4568.T 8031.T 8001.T 8316.T 8411.T 8766.T 8591.T
7011.T 7012.T 7013.T 5803.T 6146.T 6857.T 7741.T 6273.T 6920.T 7735.T
6954.T 6981.T 6723.T 6988.T 6762.T 7751.T 6702.T 6701.T 6594.T 6367.T
6301.T 8053.T 8002.T 8015.T 2768.T 3382.T 8267.T 9843.T 4452.T 4911.T
2802.T 2914.T 2502.T 2503.T 2269.T 2282.T 2871.T 2897.T 4502.T 4503.T
4519.T 4523.T 4578.T 4151.T 4543.T 4901.T 8801.T 8802.T 8830.T 3289.T
8804.T 1925.T 1928.T 1801.T 1802.T 1803.T 1812.T 9020.T 9021.T 9022.T
9101.T 9104.T 9107.T 9201.T 9202.T 6503.T 6752.T 7267.T 7269.T 7201.T
7202.T 7270.T 6902.T 7259.T 5108.T 5401.T 5411.T 5713.T 5711.T 5020.T
1605.T 9531.T 9532.T 9501.T 9502.T 9503.T 9506.T 4661.T 4689.T 4755.T
4751.T 9613.T 3659.T 4307.T 4385.T 2413.T 7832.T 9697.T 9735.T 9766.T
9024.T 9042.T 9147.T 9005.T 9007.T 9008.T 9009.T 9041.T 7453.T 7532.T
3092.T 3086.T 8233.T 8252.T 8273.T 3099.T 3397.T 9843.T 2267.T 2587.T
2579.T 2810.T 2801.T 2002.T 2212.T 2229.T 2264.T 2268.T 3402.T 3407.T
4005.T 4183.T 4188.T 4204.T 3405.T 4004.T 4042.T 4043.T 4061.T 4186.T
4189.T 4208.T 4631.T 5201.T 5202.T 5232.T 5301.T 5332.T 5333.T 5334.T
5706.T 5714.T 5801.T 5802.T 5831.T 5838.T 7182.T 7186.T 7167.T 7172.T
8304.T 8308.T 8309.T 8331.T 8354.T 8359.T 8308.T 8601.T 8604.T 8609.T
8725.T 8750.T 8795.T 8630.T 8729.T 8253.T 8439.T 8473.T 8600.T 8697.T
3288.T 3291.T 3462.T 8951.T 8952.T 8953.T 8954.T 8955.T 8956.T 8957.T
285A.T 543A.T
""".split()

US_SEED = [
    ("NVDA", "NVIDIA"),
    ("AAPL", "Apple"),
    ("MSFT", "Microsoft"),
    ("AMZN", "Amazon"),
    ("GOOGL", "Alphabet"),
    ("GOOG", "Alphabet Class C"),
    ("META", "Meta Platforms"),
    ("TSLA", "Tesla"),
    ("AVGO", "Broadcom"),
    ("AMD", "Advanced Micro Devices"),
    ("NFLX", "Netflix"),
    ("CRM", "Salesforce"),
    ("COST", "Costco"),
    ("ADBE", "Adobe"),
    ("ORCL", "Oracle"),
    ("NOW", "ServiceNow"),
    ("PLTR", "Palantir Technologies"),
    ("CRWD", "CrowdStrike"),
    ("PANW", "Palo Alto Networks"),
    ("SNOW", "Snowflake"),
    ("SHOP", "Shopify"),
    ("UBER", "Uber Technologies"),
    ("ABNB", "Airbnb"),
    ("COIN", "Coinbase"),
    ("MSTR", "MicroStrategy"),
    ("SMCI", "Super Micro Computer"),
    ("MU", "Micron Technology"),
    ("QCOM", "Qualcomm"),
    ("TXN", "Texas Instruments"),
    ("AMAT", "Applied Materials"),
    ("LRCX", "Lam Research"),
    ("KLAC", "KLA"),
    ("ASML", "ASML Holding"),
    ("TSM", "Taiwan Semiconductor Manufacturing"),
    ("INTC", "Intel"),
    ("ARM", "Arm Holdings"),
    ("MRVL", "Marvell Technology"),
    ("DELL", "Dell Technologies"),
    ("IBM", "IBM"),
    ("INTU", "Intuit"),
    ("APP", "AppLovin"),
    ("DDOG", "Datadog"),
    ("NET", "Cloudflare"),
    ("MDB", "MongoDB"),
    ("ZS", "Zscaler"),
    ("TEAM", "Atlassian"),
    ("V", "Visa"),
    ("MA", "Mastercard"),
    ("JPM", "JPMorgan Chase"),
    ("BAC", "Bank of America"),
    ("GS", "Goldman Sachs"),
    ("LLY", "Eli Lilly"),
    ("UNH", "UnitedHealth Group"),
    ("ISRG", "Intuitive Surgical"),
    ("REGN", "Regeneron Pharmaceuticals"),
    ("AMGN", "Amgen"),
    ("VRTX", "Vertex Pharmaceuticals"),
    ("WMT", "Walmart"),
    ("HD", "Home Depot"),
    ("MCD", "McDonald's"),
    ("SBUX", "Starbucks"),
    ("PEP", "PepsiCo"),
]

US_PRIORITY_SYMBOLS = """
NVDA AAPL MSFT AMZN META GOOGL GOOG AVGO TSLA LLY JPM V MA COST NFLX WMT
ORCL PG XOM HD JNJ BAC ABBV PLTR KO CRM UNH CSCO IBM GE AMD CVX WFC MS
AXP GS DIS MCD CAT NOW ISRG INTU QCOM TXN AMAT PANW AMGN PEP TMO LIN RTX
BKNG SPGI LOW HON UBER NKE BLK SCHW SYK C DE BA LMT ADP TJX GILD MDT ADI
VRTX MU LRCX KLAC INTC ARM MRVL DELL ASML TSM SMCI CRWD NET DDOG MDB SNOW
SHOP COIN MSTR APP RDDT SPOT DASH ABNB RBLX HOOD SOFI DUOL CAVA ELF HIMS
LLY REGN BIIB CVS CI ELV MRK PFE BMY ABT DHR BSX ZTS ISRG VEEV WDAY TEAM
CRM NOW ADBE ORCL IBM ACN INTU PYPL SQ FI FIS GPN V MA AXP JPM BAC C GS
MS BLK SCHW BX KKR APO ARES COF USB PNC TFC NDAQ CME ICE CB AJG AON MMC
XOM CVX COP SLB EOG MPC PSX VLO OXY FANG HAL BKR CAT DE GE HON ETN EMR
PH ITW CMI URI BA LMT RTX NOC GD TXT UPS FDX UNP NSC CSX DAL UAL AAL RCL
NCLH MAR HLT BKNG ABNB WMT COST HD LOW TGT TJX ROST ULTA SBUX MCD YUM CMG
DPZ NKE LULU TPR RL KO PEP MNST KDP PG CL KMB COST MDLZ HSY GIS KR CAG
AMZN TSLA F GM RIVN LCID
""".split()

US_NAME_OVERRIDES = {
    "PG": "Procter & Gamble",
    "XOM": "Exxon Mobil",
    "JNJ": "Johnson & Johnson",
    "ABBV": "AbbVie",
    "KO": "Coca-Cola",
    "IBM": "IBM",
    "GE": "GE Aerospace",
    "TMO": "Thermo Fisher Scientific",
    "LIN": "Linde",
    "SPGI": "S&P Global",
    "SYK": "Stryker",
    "MDT": "Medtronic",
    "KLAC": "KLA",
    "REGN": "Regeneron Pharmaceuticals",
    "BIIB": "Biogen",
    "CVS": "CVS Health",
    "CI": "Cigna",
    "ELV": "Elevance Health",
    "MRK": "Merck",
    "PFE": "Pfizer",
    "BMY": "Bristol Myers Squibb",
    "ABT": "Abbott Laboratories",
    "DHR": "Danaher",
    "BSX": "Boston Scientific",
    "ZTS": "Zoetis",
    "ACN": "Accenture",
    "PYPL": "PayPal",
    "FI": "Fiserv",
    "FIS": "Fidelity National Information Services",
    "GPN": "Global Payments",
    "BLK": "BlackRock",
    "SCHW": "Charles Schwab",
    "BX": "Blackstone",
    "KKR": "KKR",
    "APO": "Apollo Global Management",
    "ARES": "Ares Management",
    "COF": "Capital One Financial",
    "USB": "U.S. Bancorp",
    "PNC": "PNC Financial Services",
    "TFC": "Truist Financial",
    "NDAQ": "Nasdaq",
    "CME": "CME Group",
    "ICE": "Intercontinental Exchange",
    "CB": "Chubb",
    "AJG": "Arthur J. Gallagher",
    "AON": "Aon",
    "MMC": "Marsh & McLennan",
    "CVX": "Chevron",
    "COP": "ConocoPhillips",
    "SLB": "SLB",
    "EOG": "EOG Resources",
    "MPC": "Marathon Petroleum",
    "PSX": "Phillips 66",
    "VLO": "Valero Energy",
    "OXY": "Occidental Petroleum",
    "FANG": "Diamondback Energy",
    "HAL": "Halliburton",
    "BKR": "Baker Hughes",
}

ADDITIONAL_US_TICKERS = """
KO PG NKE TGT LOW DIS BKNG MAR RCL NCLH DAL UAL CAT DE GE HON RTX BA LMT
XOM CVX COP LIN SHW SPGI MS AXP BLK SCHW PYPL SQ RBLX ROKU TOST HOOD SNDK
ON MPWR ABBV ABT ACN AEP AIG AJG ALB ALGN ALL AME AMP AMT AON APD APTV ARE
ATO AVB AWK AZO BAX BDX BEN BG BIIB BIO BK BKR BMY BR BRO BSX BWA BX BXP
C CAG CAH CARR CB CBOE CBRE CCI CCL CDNS CDW CE CFG CHD CI CINF CL CLX
CMA CME CMG CMI CMS CNC CNP COO COTY CPB CPRT CPT CTRA CTSH CTVA CVS D
DHI DHR DLR DOV DOW DPZ DRI DTE DUK DVA DVN DXCM EA EBAY ECL ED EFX EIX
EL ELV EMN EMR ENPH EOG EPAM EQIX EQR ES ESS ETN ETR ETSY EVRG EW EXC
EXPD EXPE F FANG FAST FCX FDX FE FFIV FIS FITB FMC FOX FOXA FRT FSLR FTNT
FTV GD GDDY GEN GILD GIS GL GLW GM GNRC GPC GPN GRMN GWW HAL HAS HBAN HCA
HES HIG HLT HOLX HPQ HRL HSIC HST HSY HUM HWM ICE IDXX IEX IFF ILMN INCY
IP IPG IQV IR IRM IT ITW IVZ J JCI JKHY JNJ JNPR K KDP KEY KEYS KHC KIM
KMB KMI KR LDOS LEN LH LKQ LNT LULU LUV LVS LW LYB MAA MAS MCHP MCK MDLZ
MDT MET MGM MHK MKC MKTX MLM MMC MMM MNST MO MOS MPC MTD NDAQ NDSN NEE NEM
NI NOC NRG NSC NTAP NTRS NUE NVR NXPI ODFL OKE OMC OXY PAYC PAYX PCAR PCG
PFG PGR PH PHM PKG PNC PNR PNW PODD POOL PPG PPL PRU PSA PSX PTC PWR QRVO
ROK ROL ROP ROST SEE SJM SLB SNA SO STT STX SWK SWKS SYF SYK SYY TAP TDG
TEL TER TFC TFX TJX TMO TMUS TROW TRV TSCO TT TTWO TXT UDR UHS ULTA UNP
UPS URI VFC VICI VLO VMC VRSK VRSN VTR VTRS VZ WAB WAT WBA WBD WDC WELL
WFC WHR WM WRB WST WY WYNN XEL XYL YUM ZBH ZBRA ZION ZTS
AAL AFL AKAM APA APO ARCC ARES BAH BALL BBY BILI BURL CAVA CELH CHWY CHTR
CLF CLS CNM CNQ COF COKE CSL DASH DBX DKNG DOCU DOCS DKS DLO DOC DRVN DT
DUOL ELF ERIE ESTC EXAS FIX FLEX FND FOUR FRPT FTAI GFS GH GLBE GLOB GLPI
GME GMED GTLB GWRE HIMS HUBS IOT JBL KKR LPLA LSCC MNDY NBIX NTRA OKTA
PATH PINS PTC RDDT RGEN RIVN RMD ROKU SAIA SE SEIC SNAP SOFI SOLV SPOT
SSNC TCOM TKO TWLO U UPST VEEV WDAY WING WIX WSM XPEV XYZ ZM
""".split()


def synthetic_history(symbol: str, index: int, days: int = 560) -> dict:
    end = datetime.now(timezone.utc).date()
    while end.weekday() >= 5:
        end -= timedelta(days=1)
    start = end - timedelta(days=int(days * 1.65))
    dates: list[str] = []
    close: list[float] = []
    volume: list[int] = []
    price = 80 + index * 7
    day = start

    while day <= end:
        if day.weekday() < 5:
            t = len(close)
            drift = 0.0008 + (index % 7) * 0.00012
            wave = math.sin(t / (13 + index % 5)) * 0.012
            pulse = math.cos(t / (37 + index % 6)) * 0.007
            price = max(5, price * (1 + drift + wave + pulse))
            dates.append(day.isoformat())
            close.append(round(price, 2))
            volume.append(int(700_000 + index * 18_000 + abs(math.sin(t / 9)) * 550_000))
        day += timedelta(days=1)

    dates = dates[-days:]
    close = close[-days:]
    volume = volume[-days:]
    return {"symbol": symbol, "dates": dates, "close": close, "volume": volume}


def find_column(columns, candidates: list[str], fallback_index: int):
    normalized = {str(col): col for col in columns}
    for text, original in normalized.items():
        if any(candidate in text for candidate in candidates):
            return original
    return list(columns)[fallback_index]


def fetch_jpx_universe() -> list[tuple[str, str]]:
    try:
        import pandas as pd

        with urlopen(JPX_LIST_URL, timeout=30) as response:
            frame = pd.read_excel(io.BytesIO(response.read()))

        code_col = find_column(frame.columns, ["コード", "Code"], 0)
        name_col = find_column(frame.columns, ["銘柄名", "Company", "Name"], 1)
        market_col = find_column(frame.columns, ["市場", "Market", "商品区分"], 3)

        priority_words = [
            ("プライム", 0),
            ("Prime", 0),
            ("スタンダード", 1),
            ("Standard", 1),
            ("グロース", 2),
            ("Growth", 2),
        ]

        def priority(value: str) -> int:
            text = str(value)
            for key, rank in priority_words:
                if key in text:
                    return rank
            return 9

        rows = []
        for _, row in frame.iterrows():
            raw_code = str(row[code_col]).strip().split(".")[0].upper()
            code = raw_code.zfill(4) if raw_code.isdigit() else raw_code
            name = str(row[name_col]).strip()
            market = str(row[market_col]).strip()
            if not code.isalnum() or len(code) != 4:
                continue
            if any(word in market.upper() for word in ["ETF", "ETN", "REIT"]):
                continue
            if "インフラ" in market:
                continue
            rows.append((priority(market), f"{code}.T", name))

        rows.sort(key=lambda item: (item[0], item[1]))
        return [(symbol, name) for _, symbol, name in rows]
    except Exception:
        return []


def build_jp_universe() -> list[tuple[str, str]]:
    universe = []
    seen = set()
    fetched = fetch_jpx_universe()
    source = fetched or JP_SEED
    for symbol, name in source:
        if symbol not in seen:
            universe.append((symbol, name))
            seen.add(symbol)
        if not fetched and len(universe) >= JP_FALLBACK_COUNT:
            break

    # Local fallback only. GitHub Actions replaces this with the JPX official list.
    code = 1300
    while len(universe) < JP_FALLBACK_COUNT:
        symbol = f"{code}.T"
        if symbol not in seen:
            universe.append((symbol, f"JPX {code}"))
            seen.add(symbol)
        code += 1

    return universe


def build_us_universe() -> list[tuple[str, str]]:
    universe = []
    seen = set()
    for symbol, name in US_SEED:
        if symbol not in seen:
            universe.append((symbol, name))
            seen.add(symbol)
    for symbol in ADDITIONAL_US_TICKERS:
        if symbol not in seen:
            universe.append((symbol, US_NAME_OVERRIDES.get(symbol, symbol)))
            seen.add(symbol)
        if len(universe) >= US_TARGET_COUNT:
            break
    return universe[:US_TARGET_COUNT]


def ordered_symbols(symbols: list[tuple[str, str]], priority_symbols: list[str]) -> list[tuple[str, str]]:
    priority = {}
    for index, symbol in enumerate(priority_symbols):
        priority.setdefault(symbol, index)
    return sorted(symbols, key=lambda item: (priority.get(item[0], 100_000), item[0]))


def average_traded_value(item: dict) -> float:
    closes = item.get("close", [])[-25:]
    volumes = item.get("volume", [])[-25:]
    if not closes or not volumes:
        return 0.0
    pairs = list(zip(closes, volumes))
    return sum(float(close) * float(volume) for close, volume in pairs) / len(pairs)


def sort_market_rows(market: str, rows: list[dict]) -> list[dict]:
    priority_symbols = JP_PRIORITY_SYMBOLS if market == "jp" else US_PRIORITY_SYMBOLS
    priority = {}
    for index, symbol in enumerate(priority_symbols):
        priority.setdefault(symbol, index)
    if market == "us":
        for item in rows:
            item["name"] = US_NAME_OVERRIDES.get(item["symbol"], item.get("name", item["symbol"]))
    return sorted(
        rows,
        key=lambda item: (
            priority.get(item["symbol"], 100_000),
            -average_traded_value(item),
            item["symbol"],
        ),
    )


def fetch_yfinance_history(symbol: str) -> dict | None:
    try:
        import yfinance as yf

        history = yf.Ticker(symbol).history(period="2y", interval="1d", auto_adjust=True)
        if history.empty or "Close" not in history:
            return None
        history = history.dropna(subset=["Close"])
        return {
            "symbol": symbol,
            "dates": [idx.strftime("%Y-%m-%d") for idx in history.index],
            "close": [round(float(value), 4) for value in history["Close"].tolist()],
            "volume": [int(value) for value in history["Volume"].fillna(0).tolist()],
        }
    except Exception:
        return None


def fetch_yfinance_fundamentals(symbol: str) -> dict:
    try:
        import yfinance as yf

        ticker = yf.Ticker(symbol)
        info = ticker.get_info() or {}

        def number(*keys: str):
            for key in keys:
                value = info.get(key)
                if isinstance(value, (int, float)) and math.isfinite(float(value)):
                    return float(value)
            return None

        roe = number("returnOnEquity")
        revenue_growth = number("revenueGrowth", "earningsQuarterlyGrowth")
        fundamentals = {
            "per": number("trailingPE", "forwardPE"),
            "pbr": number("priceToBook"),
            "roe": roe * 100 if roe is not None and abs(roe) <= 2 else roe,
            "sales_growth": revenue_growth * 100 if revenue_growth is not None and abs(revenue_growth) <= 2 else revenue_growth,
            "market_cap": number("marketCap"),
            "average_volume": number("averageVolume", "averageDailyVolume10Day"),
        }
        return {key: value for key, value in fundamentals.items() if value is not None}
    except Exception:
        return {}


def build_market_data() -> dict:
    symbol_groups = {
        "jp": ordered_symbols(build_jp_universe(), JP_PRIORITY_SYMBOLS),
        "us": ordered_symbols(build_us_universe(), US_PRIORITY_SYMBOLS),
    }

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "jpx_yfinance_with_synthetic_fallback",
        "universe_policy": "jp_all_jpx_ordinary_equities_us_500_large_liquid_universe",
        "markets": {},
    }

    global_index = 0
    for market, symbols in symbol_groups.items():
        output["markets"][market] = []
        for symbol, name in symbols:
            history = fetch_yfinance_history(symbol)
            data_source = "yfinance" if history else "synthetic_fallback"
            history = history or synthetic_history(symbol, global_index)
            fundamentals = fetch_yfinance_fundamentals(symbol)
            output["markets"][market].append({"symbol": symbol, "name": name, "data_source": data_source, **history, **fundamentals})
            global_index += 1
        output["markets"][market] = sort_market_rows(market, output["markets"][market])

    return output


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "market-data.json").write_text(
        json.dumps(build_market_data(), ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
