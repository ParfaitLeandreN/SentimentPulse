# app/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# import helper functions from utils
from utils.reddit_scraper import get_reddit_posts
from utils.sentiment import analyze_sentiment
from utils.finance import get_stock_price, get_stock_history


st.set_page_config(page_title="SentimentPulse", layout="wide")
st.title("📈 SentimentPulse — Live Reddit Sentiment")

# -----------------------
# Sidebar controls
# -----------------------
st.sidebar.header("Controls")
ticker = st.sidebar.text_input("Ticker (e.g. TSLA, AAPL, MSFT)", value="TSLA", max_chars=8)
num_posts = st.sidebar.slider("Posts to fetch", min_value=10, max_value=200, value=50, step=10)
cache_seconds = st.sidebar.number_input("Cache TTL (seconds)", min_value=60, max_value=3600, value=600, step=60)
run = st.sidebar.button("Run Analysis")

# -----------------------
# Cached fetch + analyze
# -----------------------
@st.cache_data(ttl=600)
def fetch_and_analyze(ticker: str, limit: int):
    # fetch posts
    posts = get_reddit_posts(ticker, limit=limit)
    if posts.empty:
        return pd.DataFrame()
    # add sentiment labels
    df = analyze_sentiment(posts)
    # create datetime column from reddit created_utc (seconds)
    df['created_dt'] = pd.to_datetime(df['created'], unit='s')
    return df

# update cached function's TTL dynamically if user modified cache_seconds
fetch_and_analyze = st.cache_data(ttl=cache_seconds)(fetch_and_analyze.__wrapped__)

# -----------------------
# Main UI
# -----------------------
if not run:
    st.info("Enter a ticker and click **Run Analysis** in the sidebar.")
    st.stop()

with st.spinner("Fetching Reddit posts and analyzing sentiment..."):
    df = fetch_and_analyze(ticker, num_posts)

if df.empty:
    st.warning("No posts found for that ticker. Try a different ticker or increase 'Posts to fetch'.")
    st.stop()

# compute metrics
total = len(df)
counts = df['sentiment'].value_counts().to_dict()
pos = counts.get('positive', 0)
neu = counts.get('neutral', 0)
neg = counts.get('negative', 0)
pos_pct = round(100 * pos / total, 1) if total else 0
neg_pct = round(100 * neg / total, 1) if total else 0
neu_pct = round(100 * neu / total, 1) if total else 0

# KPI row
k1, k2, k3, k4, k5 = st.columns([1.2, 1, 1, 1, 1.2])
k1.metric("Ticker", ticker.upper())
k2.metric("Total posts", total)
k3.metric("Positive %", f"{pos_pct}%")
k4.metric("Negative %", f"{neg_pct}%")

# fetch stock price
price, change = get_stock_price(ticker)
if price is not None:
    k5.metric("Stock Price", f"${price}", f"{change}%")


# two-column layout: charts | top posts
left, right = st.columns([2.2, 1])

with left:
    # Bar chart (counts)
    st.subheader("Sentiment Distribution")
    bar_df = pd.DataFrame({
        "sentiment": ["positive", "neutral", "negative"],
        "count": [pos, neu, neg]
    })
    fig_bar = px.bar(bar_df, x="sentiment", y="count",
                     title=f"{ticker.upper()} — sentiment counts",
                     labels={"sentiment": "Sentiment", "count": "Number of posts"},
                     text="count")
    fig_bar.update_layout(margin=dict(t=40, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Pie chart
    st.subheader("Sentiment Share")
    fig_pie = px.pie(bar_df, names="sentiment", values="count",
                     title="Share by sentiment", hole=0.35)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Time series (daily stacked area)
    st.subheader("Daily Sentiment Trend")
    # group by day + sentiment
    daily = df.set_index('created_dt').groupby([pd.Grouper(freq='D'), 'sentiment']).size().reset_index(name='count')
    if daily.empty:
        st.write("Not enough data for a daily trend.")
    else:
        pivot = daily.pivot(index='created_dt', columns='sentiment', values='count').fillna(0)
        # ensure columns order
        ycols = [c for c in ["positive", "neutral", "negative"] if c in pivot.columns]
        fig_area = px.area(pivot.reset_index(), x='created_dt', y=ycols,
                           title="Daily counts by sentiment (stacked)",
                           labels={"created_dt": "Date"})
        st.plotly_chart(fig_area, use_container_width=True)


        # Hourly trend (line chart)
    st.subheader("Hourly Sentiment Trend")
    hourly = df.set_index('created_dt').groupby([pd.Grouper(freq='H'), 'sentiment']).size().reset_index(name='count')
    if hourly.empty:
        st.write("Not enough data for an hourly trend.")
    else:
        pivot_h = hourly.pivot(index='created_dt', columns='sentiment', values='count').fillna(0)
        ycols_h = [c for c in ["positive", "neutral", "negative"] if c in pivot_h.columns]
        fig_line = px.line(pivot_h.reset_index(), x='created_dt', y=ycols_h,
                           title="Hourly counts by sentiment",
                           labels={"created_dt": "Time"})
        st.plotly_chart(fig_line, use_container_width=True)

        # Stock price chart
    st.subheader("Stock Price (last 7 days)")
    hist = get_stock_history(ticker)
    if not hist.empty:
        fig_price = px.line(hist, x="Datetime", y="Close",
                        title=f"{ticker.upper()} Stock Price (7d)",
                        labels={"Close": "Price ($)"})
        st.plotly_chart(fig_price, use_container_width=True)


        # Overlay stock price with sentiment trend
    st.subheader("Stock Price vs Sentiment (last 7 days)")

    if not hist.empty and not daily.empty:
        # Merge daily stock price with sentiment
        price_daily = hist.copy()
        price_daily['Date'] = price_daily['Datetime'].dt.date
        sentiment_daily = daily.groupby(daily['created_dt'].dt.date)['count'].sum().reset_index()
        sentiment_daily.rename(columns={'created_dt': 'Date', 'count': 'SentimentCount'}, inplace=True)

        merged = pd.merge(price_daily, sentiment_daily, on='Date', how='inner')

        fig_overlay = px.line(merged, x="Date", y="Close", labels={"Close": "Stock Price ($)"})
        fig_overlay.add_bar(x=merged["Date"], y=merged["SentimentCount"], name="Sentiment volume", opacity=0.4, yaxis="y2")

        fig_overlay.update_layout(
            title=f"{ticker.upper()} Stock Price vs Sentiment Volume",
            yaxis=dict(title="Stock Price ($)"),
            yaxis2=dict(title="Sentiment Count", overlaying="y", side="right"),
            legend=dict(x=0, y=1.1, orientation="h")
        )
        st.plotly_chart(fig_overlay, use_container_width=True)
    else:
        st.write("Not enough data to overlay stock price and sentiment.")



with right:
    st.subheader("Top recent posts")
    # show newest first
    recent = df.sort_values(by='created_dt', ascending=False).head(30)

    # sentiment color map
    sentiment_colors = {
        "positive": "✅",
        "neutral": "⚪",
        "negative": "❌"
    }

    for _, row in recent.iterrows():
        sentiment_icon = sentiment_colors.get(row['sentiment'], "❓")

        st.markdown(f"""
        **{row['title']}**  
        Sentiment: {sentiment_icon} {row['sentiment'].capitalize()}  
        [Open post ↗]({row['url']})
        """)
        st.divider()



# optional: allow saving this run to CSV
save_col1, save_col2 = st.columns([1, 3])
with save_col1:
    if st.button("Save run to CSV"):
        out_path = f"data/{ticker.upper()}_reddit_sentiment.csv"
        os.makedirs("data", exist_ok=True)
        df.to_csv(out_path, index=False, encoding="utf-8")
        st.success(f"Saved {len(df)} rows to {out_path}")





























# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import os

# # ---------------------------
# # Helper Function
# # ---------------------------
# def load_data(csv_path="data/reddit_posts_sentiment.csv"):
#     if not os.path.exists(csv_path):
#         st.warning(f"{csv_path} not found. Run reddit_scraper.py and sentiment.py first!")
#         return pd.DataFrame()
#     return pd.read_csv(csv_path)

# # ---------------------------
# # Streamlit App
# # ---------------------------
# st.set_page_config(page_title="SentimentPulse Dashboard", layout="wide")
# st.title("📈 SentimentPulse Dashboard")

# # Load data
# df = load_data()

# if df.empty:
#     st.stop()

# # Sidebar: Filter by sentiment
# sentiment_filter = st.sidebar.multiselect(
#     "Filter by sentiment", options=df['sentiment'].unique(), default=df['sentiment'].unique()
# )

# filtered_df = df[df['sentiment'].isin(sentiment_filter)]

# # Sidebar: Limit number of posts to display
# num_posts = st.sidebar.slider("Number of posts to display", min_value=5, max_value=50, value=10)

# # ---------------------------
# # Show overall sentiment distribution
# # ---------------------------
# st.subheader("Sentiment Distribution")
# fig, ax = plt.subplots()
# sns.countplot(x='sentiment', data=filtered_df, order=["positive", "neutral", "negative"], palette="Set2", ax=ax)
# ax.set_xlabel("Sentiment")
# ax.set_ylabel("Number of posts")
# st.pyplot(fig)

# # ---------------------------
# # Show top posts
# # ---------------------------
# st.subheader(f"Top {num_posts} Reddit Posts")
# for i, row in filtered_df.head(num_posts).iterrows():
#     st.markdown(f"**{row['title']}**  \nSentiment: *{row['sentiment']}*  \n[Link]({row['url']})")
