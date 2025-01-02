import pandas as pd
from transformers import pipeline

def analyze_sentiment(df, sentiment_column='sentiment', polarity_column='polarity_score'):
       # Create an empty list to store sentiment scores
       sentiments = []
       polarity_scores = []

       # Specify the sentiment analysis model
       model_name = "siebert/sentiment-roberta-large-english"

       # Create the sentiment analysis pipeline using the chosen model
       sentiment_analysis = pipeline("sentiment-analysis", model=model_name)

       # Iterate over each row in the DataFrame
       for index, row in df.iterrows():
              # Try to find the column containing review text
              review_column = find_review_column(row)

              if review_column is None:
                     raise ValueError("Unable to detect the review column.")

              # Extract the text from the current row
              text = row[review_column]

              # Perform sentiment analysis on the text
              result = sentiment_analysis(text)

              # Append the sentiment label to the list
              sentiments.append(result[0]['label'])
              # Append the sentiment score to the list
              polarity_scores.append(result[0]['score'])

       # Add the sentiment scores and polarity scores to the DataFrame
       df[sentiment_column] = sentiments
       df[polarity_column] = polarity_scores

       return df

def find_review_column(row):
       # Search for columns likely to contain review text
       for col in row.index:
              # Check if the column contains text data
              if isinstance(row[col], str):
                     # Use heuristics to identify review-like columns
                     if len(row[col]) > 20:  # Assume review text is longer than 20 characters
                            return col
       return None

def main():
       # Input the file path of the CSV file
       file_path = input("Enter the file path of the CSV file: ")

       # Read the CSV file
       df = pd.read_csv(file_path)

       # Analyze sentiment and add sentiment scores to the DataFrame
       df = analyze_sentiment(df)

       # Print the DataFrame with sentiment scores
       print(df.head(300))

       # Save the modified DataFrame back to the CSV file
       df.to_csv(file_path, index=False)

       # Display success message
       print("Sentiment analysis results successfully added to the CSV file.")

if __name__ == "__main__":
       main()
