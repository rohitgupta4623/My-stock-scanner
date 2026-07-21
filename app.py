import streamlit as st
import pandas as pd
import yfinance as yf
import warnings
import logging
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Breakout Sniper Dashboard", page_icon="📈", layout="wide")

st.title("🎯 Institutional Breakout Sniper")
st.write("Click the button below to scan stocks with positive CAR & DMA alignment.")

# Stock List
my_stocks = [
    '360ONE.NS', 'ABB.NS', 'APLAPOLLO.NS', 'AUBANK.NS', 'ADANIENSOL.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 
    'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ABCAPITAL.NS', 'ALKEM.NS', 'AMBER.NS', 'AMBUJACEM.NS', 'ANGELONE.NS', 
    'APOLLOHOSP.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTRAL.NS', 'AUROPHARMA.NS', 'DMART.NS', 'AXISBANK.NS', 
    'BSE.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 
    'BANKINDIA.NS', 'BDL.NS', 'BEL.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BIOCON.NS', 
    'BLUESTARCO.NS', 'BOSCHLTD.NS', 'BRITANNIA.NS', 'CGPOWER.NS', 'CANBK.NS', 'CDSL.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 
    'COALINDIA.NS', 'COCHINSHIP.NS', 'COFORGE.NS', 'COLPAL.NS', 'CAMS.NS', 'CONCOR.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 
    'DLF.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DELHIVERY.NS', 'DIVISLAB.NS', 'DIXON.NS', 'DRREDDY.NS', 'ETERNAL.NS', 
    'EICHERMOT.NS', 'EXIDEIND.NS', 'FORCEMOT.NS', 'NYKAA.NS', 'FORTIS.NS', 'GAIL.NS', 'GVT&D.NS', 'GMRAIRPORT.NS', 
    'GLENMARK.NS', 'GODFRYPHLP.NS', 'GODREJCP.NS', 'GODREJPROP.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCAMC.NS', 
    'HDFCBANK.NS', 'HDFCLIFE.NS', 'HAVELLS.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HAL.NS', 'HINDPETRO.NS', 
    'HINDUNILVR.NS', 'HINDZINC.NS', 'POWERINDIA.NS', 'HYUNDAI.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 
    'IDFCFIRSTB.NS', 'ITC.NS', 'INDIANB.NS', 'IEX.NS', 'IOC.NS', 'IRFC.NS', 'IREDA.NS', 'INDUSTOWER.NS', 
    'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS', 'INOXWIND.NS', 'INDIGO.NS', 'JINDALSTEL.NS', 'JSWENERGY.NS', 
    'JSWSTEEL.NS', 'JIOFIN.NS', 'JUBLFOOD.NS', 'KEI.NS', 'KPITTECH.NS', 'KALYANKJIL.NS', 'KAYNES.NS', 'KFINTECH.NS', 
    'KOTAKBANK.NS', 'LTF.NS', 'LICHSGFIN.NS', 'LTM.NS', 'LT.NS', 'LAURUSLABS.NS', 'LICI.NS', 'LODHA.NS', 
    'LUPIN.NS', 'M&M.NS', 'MANAPPURAM.NS', 'MANKIND.NS', 'MARICO.NS', 'MARUTI.NS', 'MFSL.NS', 'MAXHEALTH.NS', 
    'MAZDOCK.NS', 'MOTILALOFS.NS', 'MPHASIS.NS', 'MCX.NS', 'MUTHOOTFIN.NS', 'NBCC.NS', 'NHPC.NS', 'NMDC.NS', 
    'NTPC.NS', 'NATIONALUM.NS', 'NESTLEIND.NS', 'NAM-INDIA.NS', 'NUVAMA.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 
    'OIL.NS', 'PAYTM.NS', 'OFSS.NS', 'POLICYBZR.NS', 'PGEL.NS', 'PIIND.NS', 'PNBHOUSING.NS', 'PAGEIND.NS', 
    'PATANJALI.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PIDILITIND.NS', 'POLYCAB.NS', 'PFC.NS', 'POWERGRID.NS', 
    'PREMIERENE.NS', 'PRESTIGE.NS', 'PNB.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RADICO.NS', 'RVNL.NS', 'RELIANCE.NS', 
    'SBICARD.NS', 'SBILIFE.NS', 'SHREECEM.NS', 'SRF.NS', 'MOTHERSON.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 
    'SOLARINDS.NS', 'SONACOMS.NS', 'SBIN.NS', 'SAIL.NS', 'SUNPHARMA.NS', 'SUPREMEIND.NS', 'SUZLON.NS', 
    'SWIGGY.NS', 'TATACONSUM.NS', 'TVSMOTOR.NS', 'TCS.NS', 'TATAELXSI.NS', 'TMPV.NS', 'TATAPOWER.NS', 
    'TATASTEEL.NS', 'TECHM.NS', 'FEDERALBNK.NS', 'INDHOTEL.NS', 'PHOENIXLTD.NS', 'TITAN.NS', 'TORNTPHARM.NS', 
    'TRENT.NS', 'TIINDIA.NS', 'UNOMINDA.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UNITDSPR.NS', 
    'VBL.NS', 'VEDL.NS', 'VMM.NS', 'IDEA.NS', 'VOLTAS.NS', 'WAAREEENER.NS', 'WIPRO.NS', 'YESBANK.NS', 'ZYDUSLIFE.NS'
]

if st.button("🚀 RUN SCANNER NOW"):
    results = []
    today_date = datetime.now().strftime("%d-%m-%Y")
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, ticker in enumerate(my_stocks):
        status_text.text(f"Scanning ({idx+1}/{len(my_stocks)}): {ticker}")
        progress_bar.progress((idx + 1) / len(my_stocks))
        
        try:
            data = yf.download(ticker, period="2y", interval="1d", progress=False)
            if data.empty or len(data) < 200:
                continue
            
            close_prices = data['Close'].squeeze()
            dma_30 = close_prices.rolling(window=30).mean().iloc[-1]
            dma_50 = close_prices.rolling(window=50).mean().iloc[-1]
            dma_200 = close_prices.rolling(window=200).mean().iloc[-1]
            cmp = close_prices.iloc[-1]
            dist_200_dma = ((cmp - dma_200) / dma_200) * 100

            last_1y_data = data.tail(252)
            high_date = last_1y_data['High'].squeeze().idxmax()
            car_data = close_prices.loc[high_date:]

            if len(car_data) < 10:
                continue

            car_values = car_data.expanding().mean()
            last_10_car = car_values.tail(10)

            if last_10_car.is_monotonic_increasing:
                car_status = 'Positive'
            else:
                car_status = 'Negative'

            if (cmp > dma_30) and (cmp > dma_50) and (cmp > dma_200) and (car_status == 'Positive'):
                clean_symbol = ticker.replace('.NS', '')
                tv_url = f"https://in.tradingview.com/chart/?symbol=NSE:{clean_symbol}"
                
                results.append({
                    'Stock Chart 🔗': tv_url,
                    'Stock Symbol': clean_symbol,
                    'CMP': round(cmp, 2),
                    '30 DMA': round(dma_30, 2),
                    '50 DMA': round(dma_50, 2),
                    '200 DMA': round(dma_200, 2),
                    '200 DMA Dist %': round(dist_200_dma, 2),
                    'Action': '🟢 Positive Breakout'
                })
        except Exception:
            pass

    status_text.success("✅ Scanning Complete!")
    progress_bar.empty()

    if len(results) > 0:
        df = pd.DataFrame(results)
        df = df.sort_values(by='200 DMA Dist %', ascending=True)

        st.subheader("📊 Breakout Candidates (Click link to open TradingView)")
        
        st.data_editor(
            df,
            column_config={
                "Stock Chart 🔗": st.column_config.LinkColumn(
                    "TradingView Link",
                    display_text="📈 Open Chart"
                )
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning("⚠️ Aaj koi stock breakout condition ko fulfill nahi kar raha.")
