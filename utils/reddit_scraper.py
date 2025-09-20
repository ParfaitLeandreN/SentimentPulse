import praw
import pandas as pd
import os

# Make sure the data folder exists
os.makedirs("data", exist_ok=True)

def get_reddit_posts(query="AAPL", limit=50):
    """
    Fetch recent Reddit posts mentioning a given stock ticker.
    Returns a pandas DataFrame with titles, scores, and timestamps.
    """
    reddit = praw.Reddit(
        client_id="zS8doQVSRqupisA0rjktIg",
        client_secret="aZbvH8v5Zam_evEdwuPPSN9rUOZV3g",
        user_agent="SentimentPulse (by u/Altruistic-Pomelo540)"
    )

    posts = []
    subreddit = reddit.subreddit("wallstreetbets")  # finance-heavy subreddit
    for post in subreddit.search(query, limit=limit):
        posts.append({
            "title": post.title,
            "score": post.score,
            "created": post.created_utc,
            "url": post.url
        })

    return pd.DataFrame(posts)


if __name__ == "__main__":
    df = get_reddit_posts("TSLA", 10)
    
    # Save to CSV safely with UTF-8 encoding
    csv_path = "data/reddit_posts.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved {len(df)} posts to {csv_path}")

    # Safe printing (ignore problematic characters)
    print("\nSample Titles:")
    for title in df['title']:
        print(title.encode('utf-8', errors='ignore').decode())





















# if __name__ == "__main__":
#     df = get_reddit_posts("TSLA", 10)
    
#     # Save to CSV safely with UTF-8 encoding
#     csv_path = "data/reddit_posts.csv"
#     df.to_csv(csv_path, index=False, encoding="utf-8")
#     print(f"Saved {len(df)} posts to {csv_path}")

#     # Optional: print only basic info (no emojis or arrows)
#     print("\nSample Titles (truncated):")
#     for title in df['title']:
#         # remove non-ASCII characters for safe display
#         safe_title = title.encode('ascii', errors='ignore').decode()
#         print(safe_title[:80])  # first 80 characters only





