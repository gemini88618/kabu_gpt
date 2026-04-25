import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

SYMBOLS = {
    "jp": [
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
        ("9983.T", "ファーストリテイリング"),
        ("6857.T", "アドバンテスト"),
        ("8316.T", "三井住友フィナンシャルグループ"),
        ("8411.T", "みずほフィナンシャルグループ"),
        ("9433.T", "KDDI"),
        ("9434.T", "ソフトバンク"),
        ("6367.T", "ダイキン工業"),
        ("6954.T", "ファナック"),
        ("6762.T", "TDK"),
        ("7741.T", "HOYA"),
        ("6981.T", "村田製作所"),
        ("6273.T", "SMC"),
        ("7011.T", "三菱重工業"),
        ("7012.T", "川崎重工業"),
        ("7013.T", "IHI"),
        ("5401.T", "日本製鉄"),
        ("5803.T", "フジクラ"),
        ("5802.T", "住友電気工業"),
        ("7751.T", "キヤノン"),
        ("6902.T", "デンソー"),
        ("7267.T", "本田技研工業"),
        ("8766.T", "東京海上ホールディングス"),
        ("8725.T", "MS&ADインシュアランスグループ"),
        ("8750.T", "第一生命ホールディングス"),
        ("8591.T", "オリックス"),
        ("8001.T", "伊藤忠商事"),
        ("8002.T", "丸紅"),
        ("8031.T", "三井物産"),
        ("8053.T", "住友商事"),
        ("4568.T", "第一三共"),
        ("4519.T", "中外製薬"),
        ("4502.T", "武田薬品工業"),
        ("4503.T", "アステラス製薬"),
        ("7733.T", "オリンパス"),
        ("6702.T", "富士通"),
        ("6701.T", "NEC"),
        ("9613.T", "NTTデータグループ"),
        ("4661.T", "オリエンタルランド"),
        ("9201.T", "日本航空"),
        ("9202.T", "ANAホールディングス"),
        ("3382.T", "セブン&アイ・ホールディングス"),
        ("8267.T", "イオン"),
        ("2914.T", "日本たばこ産業"),
        ("2502.T", "アサヒグループホールディングス"),
        ("2802.T", "味の素"),
        ("5108.T", "ブリヂストン"),
        ("8801.T", "三井不動産"),
        ("8802.T", "三菱地所"),
        ("7261.T", "マツダ"),
        ("7201.T", "日産自動車"),
        ("7270.T", "SUBARU"),
        ("7202.T", "いすゞ自動車"),
        ("6594.T", "ニデック"),
        ("6723.T", "ルネサスエレクトロニクス"),
        ("6146.T", "ディスコ"),
        ("6920.T", "レーザーテック"),
        ("7735.T", "SCREENホールディングス"),
        ("6971.T", "京セラ"),
        ("6770.T", "アルプスアルパイン"),
        ("6645.T", "オムロン"),
        ("7731.T", "ニコン"),
        ("4901.T", "富士フイルムホールディングス"),
        ("4911.T", "資生堂"),
        ("4452.T", "花王"),
        ("4578.T", "大塚ホールディングス"),
        ("4523.T", "エーザイ"),
        ("2413.T", "エムスリー"),
        ("4689.T", "LINEヤフー"),
        ("4755.T", "楽天グループ"),
        ("3659.T", "ネクソン"),
        ("7832.T", "バンダイナムコホールディングス"),
        ("9766.T", "コナミグループ"),
        ("9684.T", "スクウェア・エニックス・ホールディングス"),
        ("2432.T", "ディー・エヌ・エー"),
        ("4751.T", "サイバーエージェント"),
        ("9020.T", "東日本旅客鉄道"),
        ("9021.T", "西日本旅客鉄道"),
        ("9022.T", "東海旅客鉄道"),
        ("9147.T", "NIPPON EXPRESSホールディングス"),
        ("9101.T", "日本郵船"),
        ("9104.T", "商船三井"),
        ("9107.T", "川崎汽船"),
        ("1605.T", "INPEX"),
        ("5020.T", "ENEOSホールディングス"),
        ("5713.T", "住友金属鉱山"),
        ("5714.T", "DOWAホールディングス"),
        ("3402.T", "東レ"),
        ("4188.T", "三菱ケミカルグループ"),
    ],
    "us": [
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
        ("KO", "Coca-Cola"),
        ("PG", "Procter & Gamble"),
        ("NKE", "Nike"),
        ("TGT", "Target"),
        ("LOW", "Lowe's"),
        ("DIS", "Walt Disney"),
        ("BKNG", "Booking Holdings"),
        ("MAR", "Marriott International"),
        ("RCL", "Royal Caribbean Group"),
        ("NCLH", "Norwegian Cruise Line"),
        ("DAL", "Delta Air Lines"),
        ("UAL", "United Airlines"),
        ("CAT", "Caterpillar"),
        ("DE", "Deere"),
        ("GE", "GE Aerospace"),
        ("HON", "Honeywell"),
        ("RTX", "RTX"),
        ("BA", "Boeing"),
        ("LMT", "Lockheed Martin"),
        ("XOM", "Exxon Mobil"),
        ("CVX", "Chevron"),
        ("COP", "ConocoPhillips"),
        ("LIN", "Linde"),
        ("SHW", "Sherwin-Williams"),
        ("SPGI", "S&P Global"),
        ("MS", "Morgan Stanley"),
        ("AXP", "American Express"),
        ("BLK", "BlackRock"),
        ("SCHW", "Charles Schwab"),
        ("PYPL", "PayPal"),
        ("SQ", "Block"),
        ("RBLX", "Roblox"),
        ("ROKU", "Roku"),
        ("TOST", "Toast"),
        ("HOOD", "Robinhood Markets"),
        ("SNDK", "SanDisk"),
        ("ON", "ON Semiconductor"),
        ("MPWR", "Monolithic Power Systems"),
    ],
}

ADDITIONAL_US_TICKERS = """
ABBV ABT ACN AEP AIG AJG ALB ALGN ALL AME AMP AMT AON APD APTV ARE ATO
AVB AWK AXP AZO BAX BDX BEN BG BIIB BIO BK BKR BMY BR BRO BSX BWA BX BXP
C CAG CAH CARR CB CBOE CBRE CCI CCL CDNS CDW CE CERN CFG CHD CI CINF CL
CLX CMA CME CMG CMI CMS CNC CNP COO COTY CPB CPRT CPT CTRA CTSH CTVA CVS
D DHI DHR DLR DOV DOW DPZ DRI DTE DUK DVA DVN DXCM EA EBAY ECL ED EFX
EIX EL ELV EMN EMR ENPH EOG EPAM EQIX EQR ES ESS ETN ETR ETSY EVRG EW
EXC EXPD EXPE F FANG FAST FCX FDX FE FFIV FIS FISV FITB FMC FOX FOXA
FRT FSLR FTNT FTV GD GDDY GEN GILD GIS GL GLW GM GNRC GPC GPN GRMN
GWW HAL HAS HBAN HCA HES HIG HLT HOLX HPQ HRL HSIC HST HSY HUM HWM ICE
IDXX IEX IFF ILMN INCY INTC IP IPG IQV IR IRM IT ITW IVZ J JCI JKHY JNJ
JNPR K KDP KEY KEYS KHC KIM KMB KMI KR LDOS LEN LH LKQ LNT LULU LUV LVS
LW LYB MAA MAS MCHP MCK MDLZ MDT MET MGM MHK MKC MKTX MLM MMC MMM MNST
MO MOS MPC MTD NDAQ NDSN NEE NEM NI NOC NRG NSC NTAP NTRS NUE NVR NXPI
ODFL OKE OMC OXY PAYC PAYX PCAR PCG PFG PGR PH PHM PKG PNC PNR PNW PODD
POOL PPG PPL PRU PSA PSX PTC PWR PXD QRVO ROK ROL ROP ROST SBNY SBUX
SEDG SEE SJM SLB SNA SO STT STX SWK SWKS SYF SYK SYY TAP TDG TEL TER
TFC TFX TJX TMO TMUS TROW TRV TSCO TT TTWO TXT UDR UHS ULTA UNP UPS URI
VFC VICI VLO VMC VRSK VRSN VTR VTRS VZ WAB WAT WBA WBD WDC WELL WFC WHR
WM WRB WST WY WYNN XEL XYL YUM ZBH ZBRA ZION ZTS
""".split()


def normalize_symbol_universe() -> None:
    existing = {symbol for symbol, _ in SYMBOLS["us"]}
    for ticker in ADDITIONAL_US_TICKERS:
        if ticker not in existing:
            SYMBOLS["us"].append((ticker, ticker))
            existing.add(ticker)
        if len(SYMBOLS["jp"]) + len(SYMBOLS["us"]) >= 500:
            break


def synthetic_history(symbol: str, index: int, days: int = 560) -> dict:
    start = datetime.now(timezone.utc).date() - timedelta(days=days * 1.45)
    dates: list[str] = []
    close: list[float] = []
    volume: list[int] = []
    price = 80 + index * 11
    day = start

    while len(close) < days:
        if day.weekday() < 5:
            t = len(close)
            drift = 0.0009 + (index % 5) * 0.00018
            wave = math.sin(t / (13 + index % 4)) * 0.014
            pulse = math.cos(t / (37 + index % 5)) * 0.008
            price = max(5, price * (1 + drift + wave + pulse))
            dates.append(day.isoformat())
            close.append(round(price, 2))
            volume.append(int(900_000 + index * 140_000 + abs(math.sin(t / 9)) * 700_000))
        day += timedelta(days=1)

    return {"symbol": symbol, "dates": dates, "close": close, "volume": volume}


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
    normalize_symbol_universe()

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "yfinance_with_synthetic_fallback",
        "universe_policy": "liquid_recommended_japan_us_growth_universe",
        "markets": {},
    }

    global_index = 0
    for market, symbols in SYMBOLS.items():
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
