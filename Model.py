import pandas as pd
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the tokenizer from the pickle file
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Load the model from the pickle file
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the original labels from the dataset
data = pd.read_csv(r'C:/Users/Hi/PycharmProjects/Hamna_FYP/quality_attributes.csv')
labels = data['label'].unique()

# Function to preprocess new input and make predictions
def predict_class(review_text):
    # Tokenize and pad the input text
    sequence = tokenizer.texts_to_sequences([review_text])
    sequence = pad_sequences(sequence, maxlen=model.input_shape[1])

    # Make prediction
    prediction = model.predict(sequence)

    # Get the predicted class
    predicted_class = prediction.argmax(axis=-1)

    # Get the corresponding label
    predicted_label = labels[predicted_class[0]]

    return predicted_class[0], predicted_label

# Function to process reviews from a DataFrame and update predictions
def process_reviews_from_dataframe(data):
    # Check if the 'Review' column exists in the dataset
    if 'Review' not in data.columns:
        print("Error: 'Review' column not found in the DataFrame.")
        return

    # Check if sentiment column exists
    if 'sentiment' not in data.columns:
        print("Error: Sentiment column not found in the DataFrame.")
        return

    # Filter rows with negative sentiment
    negative_reviews = data[data['sentiment'] == 'NEGATIVE']

    # Iterate over each negative review
    for index, row in negative_reviews.iterrows():
        review_input = row['Review']  # Use 'Review' column directly

        # Predict class and label
        predicted_class, predicted_label = predict_class(review_input)

        # Update the DataFrame with predicted class and label
        data.at[index, 'predicted_class'] = predicted_class
        data.at[index, 'predicted_label'] = predicted_label

    print("Predictions updated in the DataFrame.")
    return data
