import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt
import streamlit as st

st.title('StockPrice360')

st.sidebar.write("""
# 株価を可視化します。
# 以下のオプションを指定してください。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 360, 20)

st.write(f"""
### 過去　**{days}** 日の有名株の株価

""")

aapl =yf.Ticker('AAPL')

df = pd.DataFrame()

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr =yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    st.sidebar.write("""
    # 株価の範囲指定
    """)

    ymin, ymax = st.sidebar.slider(
    '範囲を指定してください',
    0.0, 3500.0, (0.0, 3500.0)
    )

    tickers = {
    'apple':'AAPL','facebook':'META','google':'GOOGL','microsoft':'MSFT','netflix':'NFLX','amazon':'AMZN','Tesla':'TSLA','NVIDIA':'NVDA'
    }

    df = get_data(days, tickers)
    companies = st.multiselect(
    '会社名を選択してください。',
    list(df.index),
    ['google', 'amazon', 'facebook', 'apple']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価 (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
    )
    
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )
    st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "おっと！なにかエラーが起きているようです。"
        )
