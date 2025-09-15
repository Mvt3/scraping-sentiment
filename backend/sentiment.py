import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

analyzer = SentimentIntensityAnalyzer()


# recives a list of comments and returns a dataframe with sentiment analysis
def analyze_sentiment(comments):

    data = []
    for comment in comments:
        scores = analyzer.polarity_scores(comment)
        compound = scores["compound"]

        # Strict thresholds for sentiment classification
        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        data.append(
            {
                "comment": comment,
                "compound": compound,
                "sentiment": sentiment,
                "positive": scores["pos"],
                "negative": scores["neg"],
                "neutral": scores["neu"],
            }
        )

    return pd.DataFrame(data)


def export_to_csv(df, filename="sentiment_results.csv"):
    save_dir = os.path.expanduser("./data/")
    df.to_csv(os.path.join(save_dir, filename), index=False)
    filepath = os.path.join(save_dir, filename)
    return filepath
