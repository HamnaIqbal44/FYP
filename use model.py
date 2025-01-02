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

# Function to process reviews from a CSV file and update predictions
def process_reviews_from_csv(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Display columns and ask for review column
    print("Columns in the CSV file:")
    print(data.columns)
    review_column = input("Enter the name of the column containing review text: ")

    # Check if review column exists
    if review_column not in data.columns:
        print(f"Error: {review_column} column not found in the CSV file.")
        return

    # Iterate over each row
    for index, row in data.iterrows():
        review_input = row[review_column]

        # Predict class and label
        predicted_class, predicted_label = predict_class(review_input)

        # Update the DataFrame with predicted class and label
        data.at[index, 'predicted_class'] = predicted_class
        data.at[index, 'predicted_label'] = predicted_label

    # Save the updated DataFrame back to the CSV file
    data.to_csv(csv_file, index=False)
    print("Predictions updated in the CSV file.")

# Prompt user for CSV file
csv_file_path = input("Enter the path of the CSV file: ")
process_reviews_from_csv(csv_file_path)
