# 📊 SentimentPulse

**Real-time stock sentiment analyzer** combining Reddit data with stock prices to visualize market mood and trends.

![banner](https://img.shields.io/badge/python-3.10-blue.svg) ![status](https://img.shields.io/badge/status-Active-brightgreen)

---

## 📌 What is SentimentPulse?

**SentimentPulse** is a Streamlit dashboard that lets users pick a stock ticker (like TSLA, AAPL, or MSFT) and instantly view:

- 🔥 Public sentiment from Reddit discussions  
- 📈 How sentiment correlates with live stock prices  
- 🕒 Sentiment distribution over time (daily & hourly trends)  
- ☁️ Word clouds showing the most common words in positive, neutral, and negative posts  

This tool empowers retail investors and analysts to **visualize internet emotion and market behavior** in one place.

---

## 🎯 Features

- ✅ Scrapes Reddit for posts mentioning a stock ticker  
- ✅ Applies NLP sentiment scoring (positive / neutral / negative)  
- ✅ Pulls historical & live stock price data via `yfinance`  
- ✅ Interactive visualizations:
  - KPI metrics
  - Sentiment bar chart & pie chart
  - Daily & hourly sentiment trends
  - Stock price chart
  - Overlay of stock price vs sentiment volume
  - Word clouds by sentiment
- ✅ Export posts + sentiment to CSV  
- ⚡ Cached requests for faster re-runs  

---

## 🧱 Project Structure

```text
SentimentPulse/
│
├── app/
│   ├── dashboard.py          # Main Streamlit dashboard
│   └── utils/
│       ├── reddit_scraper.py # Reddit scraper (PRAW)
│       ├── sentiment.py      # Sentiment analysis (TextBlob)
│       └── finance.py        # Stock price utilities (yfinance)
│
├── notebooks/                # Jupyter notebooks (for experiments, optional)
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore                # Ignore venv, cache, data, etc.
