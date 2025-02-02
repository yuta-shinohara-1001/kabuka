import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')

st.sidebar.write("""
# 米国主要株価
米国株可視化ツールです。以下のオプションから表示日数を指定してください。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数',1,1800,900)

st.write(f"""
### 過去　**{days}日間**　の米国主要株価
""")

@st.cache_data
def get_data(days,tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %8 %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df,hist])
    return df

st.sidebar.write("""
## 株価の範囲指定
""")
ymin,ymax = st.sidebar.slider(
    '範囲を指定してください',
    0.0,700.0,(0.0,700.0)
)

tickers = {
    'aaple':'AAPL',
    'meta':'META',
    'google':'GOOGL',
    'microsoft':'MSFT',
    'amazon':'AMZN',
    'nvidia':'NVDA',
}
df = get_data(days,tickers)

companys = st.multiselect(
    '会社名を選択してください',
    list(df.index),
    ['aaple','amazon','google','microsoft','meta','nvidia']
)

if not companys:
    st.error('１社は選択ください')
else:
    data = df.loc[companys]
    st.write("### (USD)",data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=['Date']).rename(
        columns={'value':'Stock Prices(USD)'})
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x='Date:T',
            y=alt.Y('Stock Prices(USD):Q', stack=None, scale=alt.Scale(domain=[ymin, ymax]) ),
            color = 'Name:N'
        )
    )
    st.altair_chart(chart,use_container_width=True)
