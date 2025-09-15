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






def simple_appreciation_score(df):

    #exclude neutral comments
    non_neutral = df[df['sentiment'] != 'Neutral']
    
    if len(non_neutral) == 0:
        return 50.0
    
    positive_count = len(non_neutral[non_neutral['sentiment'] == 'Positive'])
    total_non_neutral = len(non_neutral)
    
    appreciation = (positive_count / total_non_neutral) * 100
    return round(appreciation, 1)