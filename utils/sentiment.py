import nltk
nltk.download('vader_lexicon')

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# Make sure the data folder exists
os.makedirs("data", exist_ok=True)

def add_sentiment(csv_input="data/reddit_posts.csv", csv_output="data/reddit_posts_sentiment.csv"):
    """
    Reads the CSV of Reddit posts, adds a sentiment column (positive/neutral/negative),
    and saves a new CSV.
    """
    df = pd.read_csv(csv_input)
    sia = SentimentIntensityAnalyzer()

    sentiments = []
    for title in df['title']:
        score = sia.polarity_scores(str(title))['compound']
        if score >= 0.05:
            sentiments.append("positive")
        elif score <= -0.05:
            sentiments.append("negative")
        else:
            sentiments.append("neutral")

    df['sentiment'] = sentiments
    df.to_csv(csv_output, index=False, encoding="utf-8")
    print(f"Saved sentiment-labeled CSV to {csv_output}")
    return df

def analyze_sentiment(df):
    """
    Takes a DataFrame of Reddit posts and returns a new DataFrame
    with a sentiment column (positive/neutral/negative).
    """
    sia = SentimentIntensityAnalyzer()

    sentiments = []
    for title in df['title']:
        score = sia.polarity_scores(str(title))['compound']
        if score >= 0.05:
            sentiments.append("positive")
        elif score <= -0.05:
            sentiments.append("negative")
        else:
            sentiments.append("neutral")

    df = df.copy()
    df['sentiment'] = sentiments
    return df

if __name__ == "__main__":
    df = add_sentiment()
    print(df.head())

























# import nltk
# nltk.download('vader_lexicon')

# import pandas as pd
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import os

# # Make sure the data folder exists
# os.makedirs("data", exist_ok=True)

# def add_sentiment(csv_input="data/reddit_posts.csv", csv_output="data/reddit_posts_sentiment.csv"):
#     """
#     Reads the CSV of Reddit posts, adds a sentiment column (positive/neutral/negative),
#     and saves a new CSV.
#     """
#     df = pd.read_csv(csv_input)
#     sia = SentimentIntensityAnalyzer()

#     sentiments = []
#     for title in df['title']:
#         score = sia.polarity_scores(str(title))['compound']
#         if score >= 0.05:
#             sentiments.append("positive")
#         elif score <= -0.05:
#             sentiments.append("negative")
#         else:
#             sentiments.append("neutral")

#     df['sentiment'] = sentiments
#     df.to_csv(csv_output, index=False, encoding="utf-8")
#     print(f"Saved sentiment-labeled CSV to {csv_output}")
#     return df

# if __name__ == "__main__":
#     df = add_sentiment()
#     print(df.head())
