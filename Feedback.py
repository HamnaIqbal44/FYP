import pandas as pd
import ollama
import streamlit as st

# Read the CSV file
# df = pd.read_csv(r'C:\Users\Hi\PycharmProjects\Hamna_FYP\temp_uploaded_file.csv')

# Function to find the most occurring predicted label
def find_most_common_label(df):
    return df['predicted_label'].mode().iloc[0]

# Function to get reviews for a specific label
def get_reviews_for_label(df, label):
    return df[df['predicted_label'] == label]['Review'].tolist()

# Function to generate suggestions using Ollama
def generate_suggestions(reviews):
    reviews_string = ' '.join(reviews)
    response = ollama.chat(model="phi3", messages=[
        {'role': 'system', 'content': '''Given a set of customer reviews for a product or service, provide suggestions on how to improve based on recurring issues or complaints mentioned in the reviews. Consider aspects such as product features, user experience, customer service, pricing, or any other relevant factors. Your suggestions should aim to address the identified problems and enhance overall satisfaction for customers.'''},
        {'role': 'user', 'content': f'Here are the reviews: {reviews_string}. Please provide suggestions.'},
    ])
    return response["message"]["content"]

# Find the most common predicted label
def suggestions(df):
    most_common_label = find_most_common_label(df)
    st.write(most_common_label)
    print(f"Most common predicted label: {most_common_label}")

    # Get reviews for the most common label
    reviews_for_common_label = get_reviews_for_label(df, most_common_label)
    print(f"Reviews for label {most_common_label}: {reviews_for_common_label}")

    # Generate suggestions for the most common label
    suggestions = generate_suggestions(reviews_for_common_label)
    # print("Suggestions to address the most common issues:")
    # print(suggestions)
    # Save the suggestions to a new CSV file
    suggestions_df = pd.DataFrame({'predicted_label': [most_common_label], 'suggestions': [suggestions]})
    suggestions_df.to_csv('suggestions.csv', index=False)

    # Streamlit code to display the results on a dashboard
    st.title("Customer Reviews Analysis")

    st.write(f"**Most Common Predicted Label:** {most_common_label}")

    st.write(f"**Reviews for Label {most_common_label}:**")
    st.write(reviews_for_common_label)

    st.write("**Suggestions to Address the Most Common Issues:**")
    st.success(suggestions)

    # Load the suggestions from the CSV file and display them
    suggestions_df = pd.read_csv('suggestions.csv')
    st.write("**Saved Suggestions:**")
    st.write(suggestions_df)
