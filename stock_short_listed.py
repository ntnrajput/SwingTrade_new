# add stocks from 5000Cr Market cap to 11000Cr
# fetch the data for stocks given in list and then identifies the bullish stocks as per the technicals

import os
import pickle
import numpy as np
if not hasattr(np, 'NaN'):
    np.NaN = np.nan

import pandas as pd
import yfinance as yf
import pandas_ta as ta
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fix for numpy NaN import issue (if needed)

# --- Configuration ---
CACHE_FILE = "stock_data_cache.pkl"  # File to cache downloaded data
MAX_WORKERS = 10                     # Number of parallel threads for fetching
PERIOD = "10mo" 

# --- Load Nifty 500 Symbols from CSV ---
def fetch_nifty500_symbols():

  symbols_stocks = [
    '360ONE.NS','3MINDIA.NS','ABB.NS','ACC.NS','ACMESOLAR.NS','AIAENG.NS','APLAPOLLO.NS','AUBANK.NS','AWL.NS','AADHARHFC.NS','AARTIIND.NS','AAVAS.NS','ABBOTINDIA.NS','ACE.NS','ADANIENSOL.NS','ADANIENT.NS','ADANIGREEN.NS','ADANIPORTS.NS','ADANIPOWER.NS','ATGL.NS','ABCAPITAL.NS','ABFRL.NS','ABREL.NS','ABSLAMC.NS','AEGISLOG.NS','AFCONS.NS','AFFLE.NS','AJANTPHARM.NS','AKUMS.NS','APLLTD.NS','ALIVUS.NS','ALKEM.NS','ALKYLAMINE.NS','ALOKINDS.NS','ARE&M.NS','AMBER.NS','AMBUJACEM.NS','ANANDRATHI.NS','ANANTRAJ.NS','ANGELONE.NS','APARINDS.NS','APOLLOHOSP.NS','APOLLOTYRE.NS','APTUS.NS','ASAHIINDIA.NS','ASHOKLEY.NS','ASIANPAINT.NS','ASTERDM.NS','ASTRAZEN.NS','ASTRAL.NS','ATUL.NS','AUROPHARMA.NS','AIIL.NS','DMART.NS','AXISBANK.NS','BASF.NS','BEML.NS','BLS.NS','BSE.NS','BAJAJ-AUTO.NS','BAJFINANCE.NS','BAJAJFINSV.NS','BAJAJHLDNG.NS','BAJAJHFL.NS','BALKRISIND.NS','BALRAMCHIN.NS','BANDHANBNK.NS','BANKBARODA.NS','BANKINDIA.NS','MAHABANK.NS','BATAINDIA.NS','BAYERCROP.NS','BERGEPAINT.NS','BDL.NS','BEL.NS','BHARATFORG.NS','BHEL.NS','BPCL.NS','BHARTIARTL.NS','BHARTIHEXA.NS','BIKAJI.NS','BIOCON.NS','BSOFT.NS','BLUEDART.NS','BLUESTARCO.NS','BBTC.NS','BOSCHLTD.NS','FIRSTCRY.NS','BRIGADE.NS','BRITANNIA.NS','MAPMYINDIA.NS','CCL.NS','CESC.NS','CGPOWER.NS','CRISIL.NS','CAMPUS.NS','CANFINHOME.NS','CANBK.NS','CAPLIPOINT.NS','CGCL.NS','CARBORUNIV.NS','CASTROLIND.NS','CEATLTD.NS','CENTRALBK.NS','CDSL.NS','CENTURYPLY.NS','CERA.NS','CHALET.NS','CHAMBLFERT.NS','CHENNPETRO.NS','CHOLAHLDNG.NS','CHOLAFIN.NS','CIPLA.NS','CUB.NS','CLEAN.NS','COALINDIA.NS','COCHINSHIP.NS','COFORGE.NS','COHANCE.NS','COLPAL.NS','CAMS.NS','CONCORDBIO.NS','CONCOR.NS','COROMANDEL.NS','CRAFTSMAN.NS','CREDITACC.NS','CROMPTON.NS','CUMMINSIND.NS','CYIENT.NS','DCMSHRIRAM.NS','DLF.NS','DOMS.NS','DABUR.NS','DALBHARAT.NS','DATAPATTNS.NS','DEEPAKFERT.NS','DEEPAKNTR.NS','DELHIVERY.NS','DEVYANI.NS','DIVISLAB.NS','DIXON.NS','LALPATHLAB.NS','DRREDDY.NS','EIDPARRY.NS','EIHOTEL.NS','EICHERMOT.NS','ELECON.NS','ELGIEQUIP.NS','EMAMILTD.NS','EMCURE.NS','ENDURANCE.NS','ENGINERSIN.NS','ERIS.NS','ESCORTS.NS','ETERNAL.NS','EXIDEIND.NS','NYKAA.NS','FEDERALBNK.NS','FACT.NS','FINCABLES.NS','FINPIPE.NS','FSL.NS','FIVESTAR.NS','FORTIS.NS','GAIL.NS','GVT&D.NS','GMRAIRPORT.NS','GRSE.NS','GICRE.NS','GILLETTE.NS','GLAND.NS','GLAXO.NS','GLENMARK.NS','MEDANTA.NS','GODIGIT.NS','GPIL.NS','GODFRYPHLP.NS','GODREJAGRO.NS','GODREJCP.NS','GODREJIND.NS','GODREJPROP.NS','GRANULES.NS','GRAPHITE.NS','GRASIM.NS','GRAVITA.NS','GESHIP.NS','FLUOROCHEM.NS','GUJGASLTD.NS','GMDCLTD.NS','GNFC.NS','GPPL.NS','GSPL.NS','HEG.NS','HBLENGINE.NS','HCLTECH.NS','HDFCAMC.NS','HDFCBANK.NS','HDFCLIFE.NS','HFCL.NS','HAPPSTMNDS.NS','HAVELLS.NS','HEROMOTOCO.NS','HSCL.NS','HINDALCO.NS','HAL.NS','HINDCOPPER.NS','HINDPETRO.NS','HINDUNILVR.NS','HINDZINC.NS','POWERINDIA.NS','HOMEFIRST.NS','HONASA.NS','HONAUT.NS','HUDCO.NS','HYUNDAI.NS','ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS','IDBI.NS','IDFCFIRSTB.NS','IFCI.NS','IIFL.NS','INOXINDIA.NS','IRB.NS','IRCON.NS','ITC.NS','ITI.NS','INDGN.NS','INDIACEM.NS','INDIAMART.NS','INDIANB.NS','IEX.NS','INDHOTEL.NS','IOC.NS','IOB.NS','IRCTC.NS','IRFC.NS','IREDA.NS','IGL.NS','INDUSTOWER.NS','INDUSINDBK.NS','NAUKRI.NS','INFY.NS','INOXWIND.NS','INTELLECT.NS','INDIGO.NS','IGIL.NS','IKS.NS','IPCALAB.NS','JBCHEPHARM.NS','JKCEMENT.NS','JBMA.NS','JKTYRE.NS','JMFINANCIL.NS','JSWENERGY.NS','JSWHL.NS','JSWINFRA.NS','JSWSTEEL.NS','JPPOWER.NS','J&KBANK.NS','JINDALSAW.NS','JSL.NS','JINDALSTEL.NS','JIOFIN.NS','JUBLFOOD.NS','JUBLINGREA.NS','JUBLPHARMA.NS','JWL.NS','JUSTDIAL.NS','JYOTHYLAB.NS','JYOTICNC.NS','KPRMILL.NS','KEI.NS','KNRCON.NS','KPITTECH.NS','KAJARIACER.NS','KPIL.NS','KALYANKJIL.NS','KANSAINER.NS','KARURVYSYA.NS','KAYNES.NS','KEC.NS','KFINTECH.NS','KIRLOSBROS.NS','KIRLOSENG.NS','KOTAKBANK.NS','KIMS.NS','LTF.NS','LTTS.NS','LICHSGFIN.NS','LTFOODS.NS','LTIM.NS','LT.NS','LATENTVIEW.NS','LAURUSLABS.NS','LEMONTREE.NS','LICI.NS','LINDEINDIA.NS','LLOYDSME.NS','LUPIN.NS','MMTC.NS','MRF.NS','LODHA.NS','MGL.NS','MAHSEAMLES.NS','M&MFIN.NS','M&M.NS','MANAPPURAM.NS','MRPL.NS','MANKIND.NS','MARICO.NS','MARUTI.NS','MASTEK.NS','MFSL.NS','MAXHEALTH.NS','MAZDOCK.NS','METROPOLIS.NS','MINDACORP.NS','MSUMI.NS','MOTILALOFS.NS','MPHASIS.NS','MCX.NS','MUTHOOTFIN.NS','NATCOPHARM.NS','NBCC.NS','NCC.NS','NHPC.NS','NLCINDIA.NS','NMDC.NS','NSLNISP.NS','NTPCGREEN.NS','NTPC.NS','NH.NS','NATIONALUM.NS','NAVA.NS','NAVINFLUOR.NS','NESTLEIND.NS','NETWEB.NS','NETWORK18.NS','NEULANDLAB.NS','NEWGEN.NS','NAM-INDIA.NS','NIVABUPA.NS','NUVAMA.NS','OBEROIRLTY.NS','ONGC.NS','OIL.NS','OLAELEC.NS','OLECTRA.NS','PAYTM.NS','OFSS.NS','POLICYBZR.NS','PCBL.NS','PGEL.NS','PIIND.NS','PNBHOUSING.NS','PNCINFRA.NS','PTCIL.NS','PVRINOX.NS','PAGEIND.NS','PATANJALI.NS','PERSISTENT.NS','PETRONET.NS','PFIZER.NS','PHOENIXLTD.NS','PIDILITIND.NS','PEL.NS','PPLPHARMA.NS','POLYMED.NS','POLYCAB.NS','POONAWALLA.NS','PFC.NS','POWERGRID.NS','PRAJIND.NS','PREMIERENE.NS','PRESTIGE.NS','PNB.NS','RRKABEL.NS','RBLBANK.NS','RECLTD.NS','RHIM.NS','RITES.NS','RADICO.NS','RVNL.NS','RAILTEL.NS','RAINBOW.NS','RKFORGE.NS','RCF.NS','RTNINDIA.NS','RAYMONDLSL.NS','RAYMOND.NS','REDINGTON.NS','RELIANCE.NS','RPOWER.NS','ROUTE.NS','SBFC.NS','SBICARD.NS','SBILIFE.NS','SJVN.NS','SKFINDIA.NS','SRF.NS','SAGILITY.NS','SAILIFE.NS','SAMMAANCAP.NS','MOTHERSON.NS','SAPPHIRE.NS','SARDAEN.NS','SAREGAMA.NS','SCHAEFFLER.NS','SCHNEIDER.NS','SCI.NS','SHREECEM.NS','RENUKA.NS','SHRIRAMFIN.NS','SHYAMMETL.NS','SIEMENS.NS','SIGNATURE.NS','SOBHA.NS','SOLARINDS.NS','SONACOMS.NS','SONATSOFTW.NS','STARHEALTH.NS','SBIN.NS','SAIL.NS','SWSOLAR.NS','SUMICHEM.NS','SUNPHARMA.NS','SUNTV.NS','SUNDARMFIN.NS','SUNDRMFAST.NS','SUPREMEIND.NS','SUZLON.NS','SWANENERGY.NS','SWIGGY.NS','SYNGENE.NS','SYRMA.NS','TBOTEK.NS','TVSMOTOR.NS','TANLA.NS','TATACHEM.NS','TATACOMM.NS','TCS.NS','TATACONSUM.NS','TATAELXSI.NS','TATAINVEST.NS','TATAMOTORS.NS','TATAPOWER.NS','TATASTEEL.NS','TATATECH.NS','TTML.NS','TECHM.NS','TECHNOE.NS','TEJASNET.NS','NIACL.NS','RAMCOCEM.NS','THERMAX.NS','TIMKEN.NS','TITAGARH.NS','TITAN.NS','TORNTPHARM.NS','TORNTPOWER.NS','TARIL.NS','TRENT.NS','TRIDENT.NS','TRIVENI.NS','TRITURBINE.NS','TIINDIA.NS','UCOBANK.NS','UNOMINDA.NS','UPL.NS','UTIAMC.NS','ULTRACEMCO.NS','UNIONBANK.NS','UBL.NS','UNITDSPR.NS','USHAMART.NS','VGUARD.NS','DBREALTY.NS','VTL.NS','VBL.NS','MANYAVAR.NS','VEDL.NS','VIJAYA.NS','VMM.NS','IDEA.NS','VOLTAS.NS','WAAREEENER.NS','WELCORP.NS','WELSPUNLIV.NS','WESTLIFE.NS','WHIRLPOOL.NS','WIPRO.NS','WOCKPHARMA.NS','YESBANK.NS','ZFCVINDIA.NS','ZEEL.NS','ZENTEC.NS','ZENSARTECH.NS','ZYDUSLIFE.NS','ECLERX.NS']
#   symbols_stocks = ['HEG.NS']
  return symbols_stocks

def fetch_stock_data(symbol):
    """Fetch historical data and compute indicators."""
    try:
        df = yf.Ticker(symbol).history(period="10mo")
        if df.empty:
            print(symbol)
            return None

        df = df.copy()

        df["EMA_20"] = ta.ema(df["Close"], length=20)
        df["EMA_50"] = ta.ema(df["Close"], length=50)
        df["EMA_200"] = ta.ema(df["Close"], length=200)
        df["RSI"] = ta.rsi(df["Close"], length=14)
        macd_df = ta.macd(df["Close"])

        if macd_df is not None and not macd_df.empty:
            df["MACD"] = macd_df["MACD_12_26_9"]
            df["Signal"] = macd_df["MACDs_12_26_9"]
        else:
            df["MACD"] = df["Signal"] = np.nan

        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def is_bullish(df):
    """Check if stock meets bullish criteria."""
    if df is None or len(df) < 2:
        return False

    latest, prev = df.iloc[-1], df.iloc[-2]
    volume_avg = df['Volume'].mean()

    try:
        candle_ok = (latest['Close'] > (latest['Low'] + 0.6 * (latest['High'] - latest['Low']))) and (latest['Close'] > prev['Close']) and (latest['Open'] < latest ['Close']) and (latest['Low']> prev['Low']) and (latest['High'] > prev['High'])
        ema_ok = (latest["EMA_20"] > latest["EMA_50"] > latest["EMA_200"])
        # ema_ok = (latest["EMA_50"] > latest["EMA_200"]) and ((0.95 * latest["EMA_50"] < latest["EMA_20"] < 1.05 * latest["EMA_50"]) and (latest["EMA_50"] > 1.15 * latest["EMA_200"])) 
        rsi_ok = latest["RSI"] > 45
        macd_ok = latest["MACD"] > latest["Signal"] and prev["MACD"] < prev["Signal"]
        vol_ok = latest['Volume']
        

        # print(df)

        # return all([candle_ok, ema_ok, rsi_ok, macd_ok])
        return all([candle_ok,ema_ok, vol_ok])
    except:
        return False

def get_bullish_stocks():
    """Main pipeline to get bullish stocks from Nifty 500."""
    symbols = fetch_nifty500_symbols()

    bullish = []

    for symbol in symbols:
        df = fetch_stock_data(symbol)
        # print(df.columns)
        
        if is_bullish(df):
            bullish.append(symbol)

    print("\nScan complete.")
    return bullish

if __name__ == "__main__":
    bullish_symbols = get_bullish_stocks()
    print("Bullish Stocks:")
    print(bullish_symbols)













# import os
# import pickle
# import numpy as np
# if not hasattr(np, 'NaN'):
#     np.NaN = np.nan
# import pandas as pd
# import yfinance as yf
# import pandas_ta as ta
# from concurrent.futures import ThreadPoolExecutor, as_completed

# # --- Configuration ---
# CACHE_FILE = "stock_data_cache.pkl"
# MAX_WORKERS = 10
# PERIOD = "10mo"

# # --- Cache Management ---
# def load_cache():
#     """Safely load cache data with error handling."""
#     if not os.path.exists(CACHE_FILE):
#         return {}
#     try:
#         with open(CACHE_FILE, "rb") as f:
#             return pickle.load(f)
#     except (pickle.PickleError, EOFError):
#         print("Cache corrupted - creating new cache")
#         return {}

# def save_cache(cache_data):
#     """Safely save cache data with atomic write."""
#     temp_file = f"{CACHE_FILE}.tmp"
#     try:
#         with open(temp_file, "wb") as f:
#             pickle.dump(cache_data, f)
#         os.replace(temp_file, CACHE_FILE)
#     except Exception as e:
#         print(f"Error saving cache: {e}")
#         try:
#             os.remove(temp_file)
#         except:
#             pass


# # --- Load Nifty 500 Symbols from CSV ---
# def fetch_nifty500_symbols():

#   symbols_stocks = [
#    '360ONE.NS','3MINDIA.NS','ABB.NS','ACC.NS','ACMESOLAR.NS','AIAENG.NS','APLAPOLLO.NS','AUBANK.NS','AWL.NS','AADHARHFC.NS','AARTIIND.NS','AAVAS.NS','ABBOTINDIA.NS','ACE.NS','ADANIENSOL.NS','ADANIENT.NS','ADANIGREEN.NS','ADANIPORTS.NS','ADANIPOWER.NS','ATGL.NS','ABCAPITAL.NS','ABFRL.NS','ABREL.NS','ABSLAMC.NS','AEGISLOG.NS','AFCONS.NS','AFFLE.NS','AJANTPHARM.NS','AKUMS.NS','APLLTD.NS','ALIVUS.NS','ALKEM.NS','ALKYLAMINE.NS','ALOKINDS.NS','ARE&M.NS','AMBER.NS','AMBUJACEM.NS','ANANDRATHI.NS','ANANTRAJ.NS','ANGELONE.NS','APARINDS.NS','APOLLOHOSP.NS','APOLLOTYRE.NS','APTUS.NS','ASAHIINDIA.NS','ASHOKLEY.NS','ASIANPAINT.NS','ASTERDM.NS','ASTRAZEN.NS','ASTRAL.NS','ATUL.NS','AUROPHARMA.NS','AIIL.NS','DMART.NS','AXISBANK.NS','BASF.NS','BEML.NS','BLS.NS','BSE.NS','BAJAJ-AUTO.NS','BAJFINANCE.NS','BAJAJFINSV.NS','BAJAJHLDNG.NS','BAJAJHFL.NS','BALKRISIND.NS','BALRAMCHIN.NS','BANDHANBNK.NS','BANKBARODA.NS','BANKINDIA.NS','MAHABANK.NS','BATAINDIA.NS','BAYERCROP.NS','BERGEPAINT.NS','BDL.NS','BEL.NS','BHARATFORG.NS','BHEL.NS','BPCL.NS','BHARTIARTL.NS','BHARTIHEXA.NS','BIKAJI.NS','BIOCON.NS','BSOFT.NS','BLUEDART.NS','BLUESTARCO.NS','BBTC.NS','BOSCHLTD.NS','FIRSTCRY.NS','BRIGADE.NS','BRITANNIA.NS','MAPMYINDIA.NS','CCL.NS','CESC.NS','CGPOWER.NS','CRISIL.NS','CAMPUS.NS','CANFINHOME.NS','CANBK.NS','CAPLIPOINT.NS','CGCL.NS','CARBORUNIV.NS','CASTROLIND.NS','CEATLTD.NS','CENTRALBK.NS','CDSL.NS','CENTURYPLY.NS','CERA.NS','CHALET.NS','CHAMBLFERT.NS','CHENNPETRO.NS','CHOLAHLDNG.NS','CHOLAFIN.NS','CIPLA.NS','CUB.NS','CLEAN.NS','COALINDIA.NS','COCHINSHIP.NS','COFORGE.NS','COHANCE.NS','COLPAL.NS','CAMS.NS','CONCORDBIO.NS','CONCOR.NS','COROMANDEL.NS','CRAFTSMAN.NS','CREDITACC.NS','CROMPTON.NS','CUMMINSIND.NS','CYIENT.NS','DCMSHRIRAM.NS','DLF.NS','DOMS.NS','DABUR.NS','DALBHARAT.NS','DATAPATTNS.NS','DEEPAKFERT.NS','DEEPAKNTR.NS','DELHIVERY.NS','DEVYANI.NS','DIVISLAB.NS','DIXON.NS','LALPATHLAB.NS','DRREDDY.NS','EIDPARRY.NS','EIHOTEL.NS','EICHERMOT.NS','ELECON.NS','ELGIEQUIP.NS','EMAMILTD.NS','EMCURE.NS','ENDURANCE.NS','ENGINERSIN.NS','ERIS.NS','ESCORTS.NS','ETERNAL.NS','EXIDEIND.NS','NYKAA.NS','FEDERALBNK.NS','FACT.NS','FINCABLES.NS','FINPIPE.NS','FSL.NS','FIVESTAR.NS','FORTIS.NS','GAIL.NS','GVT&D.NS','GMRAIRPORT.NS','GRSE.NS','GICRE.NS','GILLETTE.NS','GLAND.NS','GLAXO.NS','GLENMARK.NS','MEDANTA.NS','GODIGIT.NS','GPIL.NS','GODFRYPHLP.NS','GODREJAGRO.NS','GODREJCP.NS','GODREJIND.NS','GODREJPROP.NS','GRANULES.NS','GRAPHITE.NS','GRASIM.NS','GRAVITA.NS','GESHIP.NS','FLUOROCHEM.NS','GUJGASLTD.NS','GMDCLTD.NS','GNFC.NS','GPPL.NS','GSPL.NS','HEG.NS','HBLENGINE.NS','HCLTECH.NS','HDFCAMC.NS','HDFCBANK.NS','HDFCLIFE.NS','HFCL.NS','HAPPSTMNDS.NS','HAVELLS.NS','HEROMOTOCO.NS','HSCL.NS','HINDALCO.NS','HAL.NS','HINDCOPPER.NS','HINDPETRO.NS','HINDUNILVR.NS','HINDZINC.NS','POWERINDIA.NS','HOMEFIRST.NS','HONASA.NS','HONAUT.NS','HUDCO.NS','HYUNDAI.NS','ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS','IDBI.NS','IDFCFIRSTB.NS','IFCI.NS','IIFL.NS','INOXINDIA.NS','IRB.NS','IRCON.NS','ITC.NS','ITI.NS','INDGN.NS','INDIACEM.NS','INDIAMART.NS','INDIANB.NS','IEX.NS','INDHOTEL.NS','IOC.NS','IOB.NS','IRCTC.NS','IRFC.NS','IREDA.NS','IGL.NS','INDUSTOWER.NS','INDUSINDBK.NS','NAUKRI.NS','INFY.NS','INOXWIND.NS','INTELLECT.NS','INDIGO.NS','IGIL.NS','IKS.NS','IPCALAB.NS','JBCHEPHARM.NS','JKCEMENT.NS','JBMA.NS','JKTYRE.NS','JMFINANCIL.NS','JSWENERGY.NS','JSWHL.NS','JSWINFRA.NS','JSWSTEEL.NS','JPPOWER.NS','J&KBANK.NS','JINDALSAW.NS','JSL.NS','JINDALSTEL.NS','JIOFIN.NS','JUBLFOOD.NS','JUBLINGREA.NS','JUBLPHARMA.NS','JWL.NS','JUSTDIAL.NS','JYOTHYLAB.NS','JYOTICNC.NS','KPRMILL.NS','KEI.NS','KNRCON.NS','KPITTECH.NS','KAJARIACER.NS','KPIL.NS','KALYANKJIL.NS','KANSAINER.NS','KARURVYSYA.NS','KAYNES.NS','KEC.NS','KFINTECH.NS','KIRLOSBROS.NS','KIRLOSENG.NS','KOTAKBANK.NS','KIMS.NS','LTF.NS','LTTS.NS','LICHSGFIN.NS','LTFOODS.NS','LTIM.NS','LT.NS','LATENTVIEW.NS','LAURUSLABS.NS','LEMONTREE.NS','LICI.NS','LINDEINDIA.NS','LLOYDSME.NS','LUPIN.NS','MMTC.NS','MRF.NS','LODHA.NS','MGL.NS','MAHSEAMLES.NS','M&MFIN.NS','M&M.NS','MANAPPURAM.NS','MRPL.NS','MANKIND.NS','MARICO.NS','MARUTI.NS','MASTEK.NS','MFSL.NS','MAXHEALTH.NS','MAZDOCK.NS','METROPOLIS.NS','MINDACORP.NS','MSUMI.NS','MOTILALOFS.NS','MPHASIS.NS','MCX.NS','MUTHOOTFIN.NS','NATCOPHARM.NS','NBCC.NS','NCC.NS','NHPC.NS','NLCINDIA.NS','NMDC.NS','NSLNISP.NS','NTPCGREEN.NS','NTPC.NS','NH.NS','NATIONALUM.NS','NAVA.NS','NAVINFLUOR.NS','NESTLEIND.NS','NETWEB.NS','NETWORK18.NS','NEULANDLAB.NS','NEWGEN.NS','NAM-INDIA.NS','NIVABUPA.NS','NUVAMA.NS','OBEROIRLTY.NS','ONGC.NS','OIL.NS','OLAELEC.NS','OLECTRA.NS','PAYTM.NS','OFSS.NS','POLICYBZR.NS','PCBL.NS','PGEL.NS','PIIND.NS','PNBHOUSING.NS','PNCINFRA.NS','PTCIL.NS','PVRINOX.NS','PAGEIND.NS','PATANJALI.NS','PERSISTENT.NS','PETRONET.NS','PFIZER.NS','PHOENIXLTD.NS','PIDILITIND.NS','PEL.NS','PPLPHARMA.NS','POLYMED.NS','POLYCAB.NS','POONAWALLA.NS','PFC.NS','POWERGRID.NS','PRAJIND.NS','PREMIERENE.NS','PRESTIGE.NS','PNB.NS','RRKABEL.NS','RBLBANK.NS','RECLTD.NS','RHIM.NS','RITES.NS','RADICO.NS','RVNL.NS','RAILTEL.NS','RAINBOW.NS','RKFORGE.NS','RCF.NS','RTNINDIA.NS','RAYMONDLSL.NS','RAYMOND.NS','REDINGTON.NS','RELIANCE.NS','RPOWER.NS','ROUTE.NS','SBFC.NS','SBICARD.NS','SBILIFE.NS','SJVN.NS','SKFINDIA.NS','SRF.NS','SAGILITY.NS','SAILIFE.NS','SAMMAANCAP.NS','MOTHERSON.NS','SAPPHIRE.NS','SARDAEN.NS','SAREGAMA.NS','SCHAEFFLER.NS','SCHNEIDER.NS','SCI.NS','SHREECEM.NS','RENUKA.NS','SHRIRAMFIN.NS','SHYAMMETL.NS','SIEMENS.NS','SIGNATURE.NS','SOBHA.NS','SOLARINDS.NS','SONACOMS.NS','SONATSOFTW.NS','STARHEALTH.NS','SBIN.NS','SAIL.NS','SWSOLAR.NS','SUMICHEM.NS','SUNPHARMA.NS','SUNTV.NS','SUNDARMFIN.NS','SUNDRMFAST.NS','SUPREMEIND.NS','SUZLON.NS','SWANENERGY.NS','SWIGGY.NS','SYNGENE.NS','SYRMA.NS','TBOTEK.NS','TVSMOTOR.NS','TANLA.NS','TATACHEM.NS','TATACOMM.NS','TCS.NS','TATACONSUM.NS','TATAELXSI.NS','TATAINVEST.NS','TATAMOTORS.NS','TATAPOWER.NS','TATASTEEL.NS','TATATECH.NS','TTML.NS','TECHM.NS','TECHNOE.NS','TEJASNET.NS','NIACL.NS','RAMCOCEM.NS','THERMAX.NS','TIMKEN.NS','TITAGARH.NS','TITAN.NS','TORNTPHARM.NS','TORNTPOWER.NS','TARIL.NS','TRENT.NS','TRIDENT.NS','TRIVENI.NS','TRITURBINE.NS','TIINDIA.NS','UCOBANK.NS','UNOMINDA.NS','UPL.NS','UTIAMC.NS','ULTRACEMCO.NS','UNIONBANK.NS','UBL.NS','UNITDSPR.NS','USHAMART.NS','VGUARD.NS','DBREALTY.NS','VTL.NS','VBL.NS','MANYAVAR.NS','VEDL.NS','VIJAYA.NS','VMM.NS','IDEA.NS','VOLTAS.NS','WAAREEENER.NS','WELCORP.NS','WELSPUNLIV.NS','WESTLIFE.NS','WHIRLPOOL.NS','WIPRO.NS','WOCKPHARMA.NS','YESBANK.NS','ZFCVINDIA.NS','ZEEL.NS','ZENTEC.NS','ZENSARTECH.NS','ZYDUSLIFE.NS','ECLERX.NS']

#   return symbols_stocks

# def fetch_stock_data(symbol, cache=True):
#     """Fetch data with thread-safe caching."""
#     cache_data = load_cache() if cache else {}
    
#     if cache and symbol in cache_data:
#         return cache_data[symbol]

#     try:
#         df = yf.Ticker(symbol).history(period=PERIOD)
#         if df.empty:
#             return None

#         df = df.copy()
#         df["EMA_20"] = ta.ema(df["Close"], length=20)
#         df["EMA_50"] = ta.ema(df["Close"], length=50)
#         df["EMA_200"] = ta.ema(df["Close"], length=200)
#         df["RSI"] = ta.rsi(df["Close"], length=14)
        
#         macd = ta.macd(df["Close"])
#         df["MACD"] = macd["MACD_12_26_9"] if macd is not None else np.nan
#         df["Signal"] = macd["MACDs_12_26_9"] if macd is not None else np.nan

#         if cache:
#             cache_data = load_cache()
#             cache_data[symbol] = df
#             save_cache(cache_data)

#         return df
#     except Exception as e:
#         print(f"Error processing {symbol}: {str(e)[:100]}")
#         return None

# # --- Main Execution ---
# def get_bullish_stocks():
#     symbols = fetch_nifty500_symbols()
#     bullish = []
    
#     with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#         futures = {executor.submit(fetch_stock_data, sym): sym for sym in symbols}
#         for i, future in enumerate(as_completed(futures), 1):
#             sym = futures[future]
#             try:
#                 df = future.result()
#                 if df is not None and len(df) > 1:
#                     latest = df.iloc[-1]
#                     prev = df.iloc[-2]
#                     conditions = [
#                         latest['Close'] > (latest['Low'] + 0.75*(latest['High']-latest['Low'])),
#                         latest['Close'] > prev['Close'],
#                         latest["EMA_20"] > latest["EMA_50"] > latest["EMA_200"],
#                         latest["RSI"] > 50,
#                         latest["MACD"] > latest["Signal"],
#                         prev["MACD"] < prev["Signal"]
#                     ]
#                     if all(conditions):
#                         bullish.append(sym)
#             except Exception as e:
#                 print(f"Error evaluating {sym}: {e}")
            
#             if i % 10 == 0:
#                 print(f"Processed {i}/{len(symbols)}", end='\r')
    
#     print(f"\nScan complete. Found {len(bullish)} bullish stocks")
#     return sorted(bullish)

# if __name__ == "__main__":
#     # Clear corrupted cache if exists
#     if os.path.exists(CACHE_FILE) and os.path.getsize(CACHE_FILE) == 0:
#         os.remove(CACHE_FILE)
    
#     print("Starting scan...")
#     results = get_bullish_stocks()
#     print("\nBullish Stocks:")
#     for i, stock in enumerate(results, 1):
#         print(f"{i}. {stock}")