import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import urlopen

JPX_LIST_URL = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
JP_TARGET_COUNT = 1000
US_TARGET_COUNT = 500

JP_SEED = [
    ("7203.T", "トヨタ自動車"),
    ("6758.T", "ソニーグループ"),
    ("8035.T", "東京エレクトロン"),
    ("9984.T", "ソフトバンクグループ"),
    ("6861.T", "キーエンス"),
    ("7974.T", "任天堂"),
    ("6098.T", "リクルートホールディングス"),
    ("4063.T", "信越化学工業"),
    ("6501.T", "日立製作所"),
    ("8058.T", "三菱商事"),
    ("8306.T", "三菱UFJフィナンシャル・グループ"),
    ("9432.T", "日本電信電話"),
]

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
    start = datetime.now(timezone.utc).date() - timedelta(days=days * 1.45)
    dates: list[str] = []
    close: list[float] = []
    volume: list[int] = []
    price = 80 + index * 7
    day = start

    while len(close) < days:
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

    return {"symbol": symbol, "dates": dates, "close": close, "volume": volume}


def fetch_jpx_universe() -> list[tuple[str, str]]:
    try:
        import pandas as pd

        with urlopen(JPX_LIST_URL, timeout=30) as response:
            frame = pd.read_excel(response)

        code_col = next(col for col in frame.columns if "コード" in str(col))
        name_col = next(col for col in frame.columns if "銘柄名" in str(col))
        market_col = next(col for col in frame.columns if "市場・商品区分" in str(col))

        market_priority = {"プライム": 0, "スタンダード": 1, "グロース": 2}

        def priority(value: str) -> int:
            text = str(value)
            for key, rank in market_priority.items():
                if key in text:
                    return rank
            return 9

        rows = []
        for _, row in frame.iterrows():
            code = str(row[code_col]).strip()
            name = str(row[name_col]).strip()
            market = str(row[market_col]).strip()
            if not code.isdigit() or len(code) != 4:
                continue
            if "ETF" in market or "ETN" in market or "REIT" in market or "インフラ" in market:
                continue
            rows.append((priority(market), f"{code}.T", name))

        rows.sort(key=lambda item: (item[0], item[1]))
        return [(symbol, name) for _, symbol, name in rows[:JP_TARGET_COUNT]]
    except Exception:
        return []


def build_jp_universe() -> list[tuple[str, str]]:
    universe = []
    seen = set()
    for symbol, name in fetch_jpx_universe() or JP_SEED:
        if symbol not in seen:
            universe.append((symbol, name))
            seen.add(symbol)
        if len(universe) >= JP_TARGET_COUNT:
            break

    # Offline fallback for local generation. GitHub Actions replaces this with the JPX official list.
    code = 1300
    while len(universe) < JP_TARGET_COUNT:
        symbol = f"{code}.T"
        if symbol not in seen:
            universe.append((symbol, symbol))
            seen.add(symbol)
        code += 1

    return universe[:JP_TARGET_COUNT]


def build_us_universe() -> list[tuple[str, str]]:
    universe = []
    seen = set()
    for symbol, name in US_SEED:
        if symbol not in seen:
            universe.append((symbol, name))
            seen.add(symbol)
    for symbol in ADDITIONAL_US_TICKERS:
        if symbol not in seen:
            universe.append((symbol, symbol))
            seen.add(symbol)
        if len(universe) >= US_TARGET_COUNT:
            break
    return universe[:US_TARGET_COUNT]


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


def build_market_data() -> dict:
    symbol_groups = {
        "jp": build_jp_universe(),
        "us": build_us_universe(),
    }

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "jpx_yfinance_with_synthetic_fallback",
        "universe_policy": "jp_1000_jpx_list_us_500_large_liquid_universe",
        "markets": {},
    }

    global_index = 0
    for market, symbols in symbol_groups.items():
        output["markets"][market] = []
        for symbol, name in symbols:
            history = fetch_yfinance_history(symbol) or synthetic_history(symbol, global_index)
            output["markets"][market].append({"symbol": symbol, "name": name, **history})
            global_index += 1

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
