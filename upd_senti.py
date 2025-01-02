import pandas as pd
from transformers import pipeline
from Model import process_reviews_from_dataframe

def analyze_sentiment(df, sentiment_column='sentiment', polarity_column='polarity_score'):
    # Display the list of columns to the user
    print("Columns in the dataset:")
    for col in df.columns:
        print(col)

    # Check if the 'Review' column exists in the dataset
    if 'Review' not in df.columns:
        raise ValueError("Review column not found in the DataFrame.")

    # Create an empty list to store sentiment scores
    sentiments = []
    polarity_scores = []

    # Specify the sentiment analysis model
    model_name = "siebert/sentiment-roberta-large-english"

    # Create the sentiment analysis pipeline using the chosen model
    sentiment_analysis = pipeline("sentiment-analysis", model=model_name)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract the text from the 'Review' column
        text = row['Review']

        # Convert text to string if it's not already
        if not isinstance(text, str):
            text = str(text)

        # Perform sentiment analysis on the text
        result = sentiment_analysis(text)

        # Append the sentiment label to the list
        sentiments.append(result[0]['label'])
        # Append the sentiment score to the list
        polarity_scores.append(result[0]['score'])

    # Add the sentiment scores and polarity scores to the DataFrame
    df[sentiment_column] = sentiments
    df[polarity_column] = polarity_scores

    # Call process_reviews_from_csv function to process the DataFrame
    process_reviews_from_dataframe(df)

    return df
