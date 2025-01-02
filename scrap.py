import re
import pandas as pd
from upd_senti import analyze_sentiment
from dataEda import perform_eda
import chardet


def extract_reviews_from_dataset(dataset):
    def is_review_column(col_data):
        """ Check if a column contains mostly alphabetic characters and spaces. """
        if col_data.dtype == object:
            text_data = ' '.join(col_data.dropna().astype(str))
            alphabetic_ratio = len(re.findall(r'[a-zA-Z\s]', text_data)) / len(text_data)
            if alphabetic_ratio > 0.8:  # Adjust the ratio threshold as needed
                return True
        return False

    def is_date_column(col_data):
        """ Check if a column contains mostly dates. """
        date_pattern1 = re.compile(r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b')  # Standard format
        date_pattern2 = re.compile(r'\b(\w{3,9} \d{1,2}, \d{4})\b')  # Month name, Day, Year
        date_pattern3 = re.compile(r'\b(\d{1,2}[-/]\w{3,9}[-/]\d{2})\b')  # DD-Mon-YY
        date_pattern4 = re.compile(r'\b(\d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2})\b')  # MM/DD/YYYY HH:MM

        if col_data.dtype == object:
            text_data = ' '.join(col_data.dropna().astype(str))
            matches = date_pattern1.findall(text_data) + date_pattern2.findall(text_data) + \
                      date_pattern3.findall(text_data) + date_pattern4.findall(text_data)
            date_ratio = len(matches) / len(col_data.dropna())
            if date_ratio > 0.5:  # Adjust the ratio threshold as needed
                return True
        return False

    review_column = None
    date_column = None
    for column in dataset.columns:
        if is_review_column(dataset[column]):
            review_column = column
        if is_date_column(dataset[column]):
            date_column = column
        if review_column and date_column:
            break

    if review_column and date_column:
        # Check if the column labels already exist
        if "Review" in dataset.columns and "Date" in dataset.columns:
            print("Review and Date columns already exist.")
            return dataset[["Review", "Date"]]
        else:
            extracted_reviews_df = dataset.copy()
            extracted_reviews_df.rename(columns={review_column: "Review", date_column: "Date"}, inplace=True)
            return extracted_reviews_df[["Review", "Date"]]
    else:
        if not review_column:
            print("Error: Review column not found in the dataset.")
        if not date_column:
            print("Error: Date column not found in the dataset.")
        return None

def process_data(df, output_file_path):
    reviews_df = extract_reviews_from_dataset(df)
    if reviews_df is not None:
        reviews_df = perform_eda(reviews_df)
        analyzed_df = analyze_sentiment(reviews_df)
        analyzed_df.to_csv(output_file_path, index=False)
        return analyzed_df
    else:
        print("Failed to extract reviews from dataset.")
        return None

def process_dataframe_from_dashboard(file_path):
    # Detect file encoding
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    encoding = result['encoding']

    # Read the file with the detected encoding
    try:
        df = pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        # Fallback to a common encoding if the detected one fails
        df = pd.read_csv(file_path, encoding='latin1')

    processed_df = process_data(df, file_path)
    if processed_df is not None:
        return processed_df
    else:
        return None

# if __name__ == "__main__":
#     import argparse
# 
#     parser = argparse.ArgumentParser(description="Process a dataset to extract reviews and dates.")
#     parser.add_argument("file_path", type=str, help="Path to the dataset file (CSV format).")
# 
#     args = parser.parse_args()
#     file_path = args.file_path
# 
#     try:
#         processed_df = process_dataframe_from_dashboard(file_path)
#         if processed_df is not None:
#             print("Processed data saved to the same file.")
#         else:
#             print("No processed data to save.")
#     except Exception as e:
#         print(f"Error processing the file: {e}")
