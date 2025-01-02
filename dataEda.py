import pandas as pd
import numpy as np

def fill_missing_values(df):
    """
    Fill missing values with mean for numeric columns.
    """
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
    return df

def basic_eda(df):
    """
    Perform basic exploratory data analysis on the dataframe.
    Fill missing values with mean for numeric columns.
    """
    # Fill missing values with mean for numeric columns
    df = fill_missing_values(df)

    # Example EDA: Display basic information about the dataset
    print("Dataset Information:")
    df.info()

    print("\nStatistical Summary:")
    print(df.describe())

    print("\nMissing Values:")
    print(df.isnull().sum())

    # Example: Adding a column indicating review length
    if 'Review' in df.columns:
        df['Review_Length'] = df['Review'].apply(len)

    # Example: Converting date column to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows with invalid dates
    df = df.dropna(subset=['Date'])

    return df

def perform_eda(df):
    """
    Perform EDA on the dataset and save the processed dataset.
    """
    df = basic_eda(df)
    # Assuming you want to save the changes in the same DataFrame
    # You can remove this step if you don't need to save it
    save_dataset(df)
    return df

def save_dataset(df, file_path=None):
    """
    Save the modified dataframe to the original file or a specified file path.
    """
    if file_path is not None:
        df.to_csv(file_path, index=False)
        print(f"Processed dataset saved to {file_path}")
    else:
        print("No file path provided. Saving changes in the same DataFrame.")
    # Since changes are made in the same DataFrame, there's no need to return anything
