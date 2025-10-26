"""
Stock Analysis Dashboard - Streamlit app
Usage: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")

# -------------------------
# Indicator functions
# -------------------------
def sma(series, window):
    return series.rolling(window=window, min_periods=1).mean()

def ema(series, window):
    return series.ewm(span=window, adjust=False).mean()

def rsi(series, window=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/window, adjust=False).mean()
    ma_down = down.ewm(alpha=1/window, adjust=False).mean()
    rs = ma_up / (ma_down + 1e-9)
    return 100 - (100 / (1 + rs))

# -------------------------
# Streamlit UI
# -------------------------
st.title("📈 Stock Analysis Dashboard")
st.markdown("Enter a ticker and date range to fetch historical data and view indicators (SMA, EMA, RSI).")

with st.sidebar:
    st.header("Inputs")
    ticker = st.text_input("Ticker", value="AAPL").upper()
    col1, col2 = st.columns(2)
    start = st.date_input("Start date", value=pd.to_datetime("2023-01-01"))
    end = st.date_input("End date", value=pd.to_datetime("today"))
    sma_win = st.number_input("SMA window", min_value=2, max_value=200, value=20)
    ema_win = st.number_input("EMA window", min_value=2, max_value=200, value=50)
    rsi_win = st.number_input("RSI window", min_value=5, max_value=50, value=14)
    fetch_btn = st.button("Fetch & Analyze")

# default message
if not fetch_btn:
    st.info("Enter inputs in the sidebar and click **Fetch & Analyze**.")
    st.stop()

# -------------------------
# Fetch data
# -------------------------
try:
    with st.spinner(f"Fetching {ticker} data..."):
        data = yf.download(ticker, start=pd.to_datetime(start), end=pd.to_datetime(end) + pd.Timedelta(days=1), progress=False)
except Exception as e:
    st.error(f"Error fetching data for {ticker}: {e}")
    st.stop()

if data.empty:
    st.warning("No data returned for that ticker / date range. Try another ticker or date range.")
    st.stop()

data = data.reset_index().rename(columns={"Date":"Date"})
data["Date"] = pd.to_datetime(data["Date"])

# -------------------------
# Compute indicators
# -------------------------
data["SMA"] = sma(data["Close"], sma_win)
data["EMA"] = ema(data["Close"], ema_win)
data["RSI"] = rsi(data["Close"], rsi_win)

# -------------------------
# Top row info
# -------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"{ticker} — {data['Date'].iloc[0].date()} to {data['Date'].iloc[-1].date()}")
    latest = data.iloc[-1]
    st.write(f"Latest Close: **{latest['Close']:.2f}**  |  Volume: **{int(latest['Volume']):,}**")

with col2:
    st.download_button(
        "Download CSV",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name=f"{ticker}_history.csv",
        mime="text/csv"
    )

# -------------------------
# Plotly Chart: Price + SMA/EMA
# -------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="Close", line=dict(width=1.5)))
fig.add_trace(go.Scatter(x=data["Date"], y=data["SMA"], name=f"SMA ({sma_win})", line=dict(width=1)))
fig.add_trace(go.Scatter(x=data["Date"], y=data["EMA"], name=f"EMA ({ema_win})", line=dict(width=1)))
fig.update_layout(title=f"{ticker} Price with SMA/EMA", xaxis_title="Date", yaxis_title="Price")
fig.update_xaxes(rangeslider_visible=True)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# RSI subplot
# -------------------------
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=data["Date"], y=data["RSI"], name=f"RSI ({rsi_win})"))
fig2.add_hline(y=70, line_dash="dash", line_color="red")
fig2.add_hline(y=30, line_dash="dash", line_color="green")
fig2.update_layout(title="RSI", xaxis_title="Date", yaxis_title="RSI")
st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Data preview and indicators
# -------------------------
st.markdown("### Data preview")
st.dataframe(data.tail(20).reset_index(drop=True))

st.markdown("### Latest Indicators")
latest_table = pd.DataFrame({
    "Indicator": ["Close", f"SMA({sma_win})", f"EMA({ema_win})", f"RSI({rsi_win})"],
    "Value": [f"{latest['Close']:.2f}", f"{latest['SMA']:.2f}", f"{latest['EMA']:.2f}", f"{latest['RSI']:.2f}"]
})
st.table(latest_table)

st.success("Analysis complete. Use the CSV download to export historical data.")