from transformers import pipeline
import pandas as pd

model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
analyzer = pipeline("sentiment-analysis", model=model_name)


def analyze_sentiment_nm(comments):
    
    results = []
    for comment in comments:
        try:
            analysis = analyzer(comment[:512])[0]  
            results.append({
                "text": comment,
                "sentiment": analysis["label"],
                "score": analysis["score"]
            })
        except Exception as e:
            results.append({"text": comment, "sentiment": "Error", "score": 0.0})

    return pd.DataFrame(results)