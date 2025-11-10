def sentiment_summary(df):

    sentiments_count = df["sentiment"].value_counts()
    total_comments = len(df)

    percent_pos = (sentiments_count.get("Positive", 0) / total_comments) * 100
    percent_neu = (sentiments_count.get("Neutral", 0) / total_comments) * 100
    percent_neg = (sentiments_count.get("Negative", 0) / total_comments) * 100

    not_neutral = df[df["sentiment"] != "Neutral"]

    if len(not_neutral) > 0:

        avg_compound = not_neutral["compound"].mean()
        general_appreciation = ((avg_compound + 1) / 2) * 100

    else:
        avg_compound = 0
        general_appreciation = 50

    # returns diferent metrics
    return {
        "percent_positive": percent_pos,
        "percent_neutral": percent_neu,
        "percent_negative": percent_neg,
        "avg_compound": avg_compound,
        "general_appreciation": general_appreciation,
        "total_comments": total_comments,
        "non_neutral_comments": len(not_neutral) if len(not_neutral) > 0 else 0,
    }




#VADER appreciation score
def simple_appreciation_score(df):

    if len(df) == 0:
        return None
    
    pos = len(df[df['sentiment'] == 'Positive'])
    neu = len(df[df['sentiment'] == 'Neutral'])
    neg = len(df[df['sentiment'] == 'Negative'])
    total = len(df)
    
    # Weighted score
    score = ((pos * 1.0 + neu * 0.5 + neg * 0.0) / total) * 100
    
    return round(score, 1)



#RoBERTa appreciation score
def summarize_roberta_results(df):

    # summary = df["sentiment"].value_counts(normalize=True) * 100
    # print("\nSentiment Summary (RoBERTa)")
    # for sentiment, pct in summary.items():
    #     print(f"{sentiment}: {pct:.1f}%")
    # print("\nSample results:")
    # print(df.head())
    # return 0.0

    if len(df) == 0:
        return None
    
    pos = len(df[df['sentiment'] == 'positive'])
    neu = len(df[df['sentiment'] == 'neutral'])
    neg = len(df[df['sentiment'] == 'negative'])
    

    score = ((pos * 1.0 + neu * 0.5 + neg * 0.0) / len(df)) * 100
    
    return round(score, 1)

