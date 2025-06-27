# 📊 SentimentPulse

**Real-time stock sentiment analyzer** combining Reddit, Twitter, and News data with stock prices to visualize market mood and forecast movement.

![banner](https://img.shields.io/badge/python-3.10-blue.svg) ![status](https://img.shields.io/badge/status-WIP-yellow)

---

## 📌 What is SentimentPulse?

**SentimentPulse** is a dashboard that lets users pick a stock (like TSLA or AAPL) and instantly view:
- 🔥 Public sentiment (Reddit, Twitter, News headlines)
- 📈 How sentiment correlates with stock prices
- 🧠 Optional price direction forecast based on recent sentiment

> This tool empowers retail investors and analysts to **visualize internet emotion and market trends** in one place.

---

## 🎯 Features

- ✅ Scrapes Reddit, Twitter (or Twitter alternatives), and News for stock mentions
- ✅ Applies NLP sentiment scoring to text
- ✅ Pulls historical stock price data via `yfinance`
- ✅ Merges & visualizes price vs. sentiment over time
- ✅ Interactive dashboard via Streamlit
- 🔮 (Optional) Basic machine learning to forecast next-day price direction

---

## 🧱 Project Structure

