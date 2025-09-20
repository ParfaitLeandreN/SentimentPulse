import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from utils.reddit_scraper import get_reddit_posts
from utils.sentiment import analyze_sentiment

st.set_page_config(page_title="SentimentPulse Dashboard", layout="wide")
st.title("📈 SentimentPulse Dashboard")

# ---------------------------
# User Input
# ---------------------------
ticker = st.text_input("Enter a stock ticker (e.g. AAPL, TSLA, MSFT):", value="AAPL")
num_posts = st.sidebar.slider("Number of posts to fetch", min_value=10, max_value=100, value=30)

if st.button("Run Analysis"):
    with st.spinner("Fetching Reddit posts and analyzing sentiment..."):
        posts = get_reddit_posts(ticker, limit=num_posts)

        if posts.empty:
            st.warning("No posts found. Try another ticker.")
            st.stop()

        df = analyze_sentiment(posts)

        # Sidebar: Filter by sentiment
        sentiment_filter = st.sidebar.multiselect(
            "Filter by sentiment", options=df['sentiment'].unique(), default=df['sentiment'].unique()
        )
        filtered_df = df[df['sentiment'].isin(sentiment_filter)]

        # ---------------------------
        # Sentiment Distribution
        # ---------------------------
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x='sentiment', data=filtered_df, order=["positive", "neutral", "negative"], palette="Set2", ax=ax)
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Number of posts")
        st.pyplot(fig)

        # ---------------------------
        # Show top posts
        # ---------------------------
        st.subheader(f"Top {len(filtered_df.head(10))} Reddit Posts")
        for i, row in filtered_df.head(10).iterrows():
            st.markdown(f"**{row['title']}**  \nSentiment: *{row['sentiment']}*  \n[Link]({row['url']})")





























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
