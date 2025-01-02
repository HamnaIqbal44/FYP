# import pandas as pd
# from transformers import AutoTokenizer
# from transformers import AutoModelForSequenceClassification
# from scipy.special import softmax
#
# def find_review_column(df):
#     # Look for common column names that might contain reviews
#     possible_review_columns = ['review', 'description', 'text', 'content']
#     for column in df.columns:
#         if column.lower() in possible_review_columns:
#             return column
#     # If no matching column is found, prompt the user to enter the column name
#     print("No standard review column found. Please enter the name of the column containing reviews.")
#     print("Available columns:", df.columns.tolist())
#     review_column = input("Review column name: ")
#     return review_column
#
# def calculate_sentiment_scores(df, model_name, review_column):
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     MODEL = AutoModelForSequenceClassification.from_pretrained(model_name)
#
#     sentiment_scores = []
#
#     for review in df[review_column]:
#         encoded_text = tokenizer(review, return_tensors='pt')
#         output = MODEL(**encoded_text)
#         scores = output[0][0].detach().numpy()
#         scores = softmax(scores)
#         scores_dict = {
#             'neg': scores[0],
#             'neu': scores[1],
#             'pos': scores[2]
#         }
#         sentiment_scores.append(scores_dict)
#
#     return sentiment_scores
#
# def main():
#     csv_path = input("Enter the path to the CSV file: ")
#     df = pd.read_csv(csv_path)
#
#     model_name = "cardiffnlp/twitter-roberta-base-sentiment"
#
#     review_column = find_review_column(df)
#
#     sentiment_scores = calculate_sentiment_scores(df, model_name, review_column)
#
#     df['sentiment'] = sentiment_scores
#
#     df.to_csv(csv_path, index=False)
#     print("Sentiment scores saved to the CSV file.")
#
# if __name__ == "__main__":
#     main()


import pandas as pd
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

def find_review_column(df):
    print("Available columns:", df.columns.tolist())
    review_column = input("Enter the name of the column containing reviews: ")
    while review_column not in df.columns:
        print("Column not found. Please enter a valid column name.")
        review_column = input("Enter the name of the column containing reviews: ")
    return review_column

def calculate_sentiment_scores(df, model_name, review_column):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    MODEL = AutoModelForSequenceClassification.from_pretrained(model_name)

    sentiment_scores = []
    polarities = []
    sentiments = []

    for review in df[review_column]:
        encoded_text = tokenizer(review, return_tensors='pt')
        output = MODEL(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # Determine overall sentiment
        sentiment = "neutral"
        if scores[0] > scores[2]:
            sentiment = "negative"
        elif scores[2] > scores[0]:
            sentiment = "positive"
        sentiments.append(sentiment)

        # Store polarity scores
        polarities.append({
            'neg': scores[0],
            'neu': scores[1],
            'pos': scores[2]
        })

    return polarities, sentiments

def main():
    csv_path = input("Enter the path to the CSV file: ")
    df = pd.read_csv(csv_path)

    model_name = "cardiffnlp/twitter-roberta-base-sentiment"

    review_column = find_review_column(df)

    polarities, sentiments = calculate_sentiment_scores(df, model_name, review_column)

    df['polarity_scores'] = polarities
    df['sentiment'] = sentiments

    df.to_csv(csv_path, index=False)
    print("Sentiment scores and sentiments saved to the CSV file.")

if __name__ == "__main__":
    main()
