import pandas as pd
from transformers import pipeline

def analyze_sentiment(df, sentiment_column='sentiment', polarity_column='polarity_score'):
    """
    Analyze sentiment of the 'Review' column in the DataFrame.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the reviews.
    - sentiment_column (str): Name of the column to store sentiment labels.
    - polarity_column (str): Name of the column to store sentiment scores.

    Returns:
    - pd.DataFrame: DataFrame with added sentiment and polarity score columns.
    """
    # Check if the 'Review' column exists in the dataset
    if 'Review' not in df.columns:
        raise ValueError("The 'Review' column does not exist in the dataset.")

    # Create an empty list to store sentiment scores
    sentiments = []
    polarity_scores = []

    # Specify the sentiment analysis model
    model_name = "siebert/sentiment-roberta-large-english"

    # Create the sentiment analysis pipeline using the chosen model
    sentiment_analysis = pipeline("sentiment-analysis", model=model_name)

    # Iterate over each review in the DataFrame
    for review_text in df['Review']:
        # Convert review text to string if it's not already
        if not isinstance(review_text, str):
            review_text = str(review_text)

        # Perform sentiment analysis on the review text
        result = sentiment_analysis(review_text)

        # Append the sentiment label to the list
        sentiments.append(result[0]['label'])
        # Append the sentiment score to the list
        polarity_scores.append(result[0]['score'])

    # Add the sentiment scores and polarity scores to the DataFrame
    df[sentiment_column] = sentiments
    df[polarity_column] = polarity_scores

    return df
