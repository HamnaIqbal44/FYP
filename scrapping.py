# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
# import time
# from bs4 import BeautifulSoup
# import re
# import datetime
# from sentiment import analyze_sentiment
# import os
#
# def get_input():
#     choice = input("Enter 'URL' to scrape reviews from a webpage or 'FILE' to extract from a dataset file: ").strip().lower()
#     if choice == 'url':
#         url = input("Enter the URL: ")
#         app_name = input("Enter the app name: ")
#         app_name = re.sub(r'[^a-zA-Z0-9\s]', '', app_name)  # Remove special characters from app name
#         num_reviews = input('Enter the number of reviews to scrape: ')
#         approx_t = (6 + ((int(num_reviews) / 10) + 10) * 3)
#         print(f'Approximate time to scrape: {approx_t} minutes')
#         return url, app_name, num_reviews, None
#     elif choice == 'file':
#         file_path = input("Enter the path to the dataset file: ")
#         return None, None, None, file_path
#     else:
#         print("Invalid choice.")
#         return None, None, None, None
#
# def setup_driver(url):
#     driver = webdriver.Chrome()
#     driver.get(url)
#     time.sleep(3)
#     return driver
#
# def click_see_all_reviews(driver):
#     see_all_reviews_button = driver.find_element(By.CSS_SELECTOR, '''.Jwxk6d > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1) > span:nth-child(4)''')
#     see_all_reviews_button.click()
#     time.sleep(3)
#
# def scroll_to_buttons(driver, while_loop):
#     i = 0
#     n = 0
#     while i < while_loop:
#         buttons = driver.find_elements(By.CSS_SELECTOR, "button.VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.mN1ivc[data-disable-idom='true'][aria-expanded='false'][aria-haspopup='menu']")
#         start = len(buttons)
#         for button in buttons[n:]:
#             for _ in range(5):
#                 driver.execute_script("arguments[0].scrollIntoView();", button)
#         n = start
#         i += 1
#         time.sleep(3)
#
# def scrape_app_reviews(html):
#     if html:
#         soup = BeautifulSoup(html, "html.parser")
#         reviews = []
#         for review_container in soup.find_all("div", class_="RHo1pe"):
#             name_element = review_container.find("div", class_="YNR7H").find("div", class_="X5PpBb")
#             reviewer_name = name_element.text.strip() if name_element else None
#
#             date_element = review_container.find("span", class_="bp9Aid")
#             review_date = date_element.text.strip() if date_element else None
#
#             review_text_element = review_container.find("div", class_="h3YV2d")
#             review_text = review_text_element.text.strip() if review_text_element else None
#
#             review = {
#                 "Name": reviewer_name,
#                 "Date": review_date,
#                 "Review": review_text
#             }
#             reviews.append(review)
#
#         df = pd.DataFrame(reviews)
#         return df
#
#     else:
#         print("Error: No HTML provided.")
#         return None
#
# def save_reviews_to_csv(reviews_df, app_name, num_reviews):
#     if reviews_df is not None:
#         reviews_df = reviews_df.head(int(num_reviews))
#         current_time = datetime.datetime.now()
#         current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
#         file_name = f"{app_name}_{current_time_str}.csv"
#         reviews_df.to_csv(file_name, index=False)
#         print(f"Reviews scraped and saved to {file_name}")
#         return file_name
#     else:
#         print("Failed to scrape reviews.")
#         return None
#
# def call_sentiment_analysis(file_path):
#     if file_path:
#         print("Performing sentiment analysis...")
#         analyze_sentiment(file_path)
#         print("Sentiment analysis completed.")
#     else:
#         print("File path is empty.")
#
# def read_dataset(file_path):
#     try:
#         df = pd.read_csv(file_path)
#         return df
#     except Exception as e:
#         print(f"Error reading dataset: {e}")
#         return None
#
# # def extract_reviews_from_dataset(dataset):
# #     review_columns = [col for col in dataset.columns if 'review' in col.lower()]
# #     date_columns = [col for col in dataset.columns if 'date' in col.lower()]
# #
# #     if review_columns and date_columns:
# #         review_column = review_columns[0]
# #         date_column = date_columns[0]
# #         return dataset[[review_column, date_column]]
# #     else:
# #         print("Error: Review or Date column not found in the dataset.")
# #         return None
#
# def extract_reviews_from_dataset(dataset):
#     review_columns = [col for col in dataset.columns if 'review' in col.lower()]
#     date_columns = [col for col in dataset.columns if 'date' in col.lower()]
#
#     if review_columns and date_columns:
#         review_column = review_columns[0]
#         date_column = date_columns[0]
#         # Rename the review column to "Review" and date column to "Date"
#         extracted_reviews_df = dataset.rename(columns={review_column: "Review", date_column: "Date"})
#         return extracted_reviews_df[["Review", "Date"]]  # Select only the Review and Date columns
#     else:
#         print("Error: Review or Date column not found in the dataset.")
#         return None
# def main():
#     url, app_name, num_reviews, file_path = get_input()
#     if url:
#         driver = setup_driver(url)
#         click_see_all_reviews(driver)
#         while_loop = (int(num_reviews) / 10) + 10
#         scroll_to_buttons(driver, while_loop)
#         review_html = driver.page_source
#         reviews_df = scrape_app_reviews(review_html)
#         saved_file_path = save_reviews_to_csv(reviews_df, app_name, num_reviews)
#         driver.quit()
#         call_sentiment_analysis(saved_file_path)
#     elif file_path:
#         dataset = read_dataset(file_path)
#         if dataset is not None:
#             if not app_name:
#                 app_name = input("Enter the app name: ")
#             reviews_df = extract_reviews_from_dataset(dataset)
#             if reviews_df is not None:
#                 current_time = datetime.datetime.now()
#                 current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
#                 file_name = f"{app_name}_dataset_reviews_{current_time_str}.csv"
#                 reviews_df.to_csv(file_name, index=False)
#                 print(f"Reviews extracted from dataset and saved to {file_name}")
#                 call_sentiment_analysis(file_name)
#             else:
#                 print("Failed to extract reviews from dataset.")
#         else:
#             print("Exiting.")
#
#
# if __name__ == "__main__":
#     main()

# import pandas as pd
# import time
# from bs4 import BeautifulSoup
# import re
# import datetime
# from sentiment import analyze_sentiment
# from dataEda import main as perform_eda  # Import the EDA function
# import os
#
# def get_input():
#     choice = input("Enter 'URL' to scrape reviews from a webpage or 'FILE' to extract from a dataset file: ").strip().lower()
#     if choice == 'url':
#         url = input("Enter the URL: ")
#         app_name = input("Enter the app name: ")
#         app_name = re.sub(r'[^a-zA-Z0-9\s]', '', app_name)  # Remove special characters from app name
#         num_reviews = input('Enter the number of reviews to scrape: ')
#         approx_t = (6 + ((int(num_reviews) / 10) + 10) * 3)
#         print(f'Approximate time to scrape: {approx_t} minutes')
#         return url, app_name, num_reviews, None
#     elif choice == 'file':
#         file_path = input("Enter the path to the dataset file: ")
#         df = pd.read_csv(file_path)
#         print(df.dtypes)
#         return None, None, None, file_path
#     else:
#         print("Invalid choice.")
#         return None, None, None, None
#
# def setup_driver(url):
#     driver = webdriver.Chrome()
#     driver.get(url)
#     time.sleep(3)
#     return driver
#
# def click_see_all_reviews(driver):
#     see_all_reviews_button = driver.find_element(By.CSS_SELECTOR, '''.Jwxk6d > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1) > span:nth-child(4)''')
#     see_all_reviews_button.click()
#     time.sleep(3)
#
# def scroll_to_buttons(driver, while_loop):
#     i = 0
#     n = 0
#     while i < while_loop:
#         buttons = driver.find_elements(By.CSS_SELECTOR, "button.VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.mN1ivc[data-disable-idom='true'][aria-expanded='false'][aria-haspopup='menu']")
#         start = len(buttons)
#         for button in buttons[n:]:
#             for _ in range(5):
#                 driver.execute_script("arguments[0].scrollIntoView();", button)
#         n = start
#         i += 1
#         time.sleep(3)
#
# def scrape_app_reviews(html):
#     if html:
#         soup = BeautifulSoup(html, "html.parser")
#         reviews = []
#         for review_container in soup.find_all("div", class_="RHo1pe"):
#             name_element = review_container.find("div", class_="YNR7H").find("div", class_="X5PpBb")
#             reviewer_name = name_element.text.strip() if name_element else None
#
#             date_element = review_container.find("span", class_="bp9Aid")
#             review_date = date_element.text.strip() if date_element else None
#
#             review_text_element = review_container.find("div", class_="h3YV2d")
#             review_text = review_text_element.text.strip() if review_text_element else None
#
#             review = {
#                 "Name": reviewer_name,
#                 "Date": review_date,
#                 "Review": review_text
#             }
#             reviews.append(review)
#
#         df = pd.DataFrame(reviews)
#         return df
#
#     else:
#         print("Error: No HTML provided.")
#         return None
#
# def save_reviews_to_csv(reviews_df, app_name, num_reviews):
#     if reviews_df is not None:
#         reviews_df = reviews_df.head(int(num_reviews))
#         current_time = datetime.datetime.now()
#         current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
#         file_name = f"{app_name}_{current_time_str}.csv"
#         reviews_df.to_csv(file_name, index=False)
#         print(f"Reviews scraped and saved to {file_name}")
#         return file_name
#     else:
#         print("Failed to scrape reviews.")
#         return None
#
# def call_sentiment_analysis(file_path):
#     if file_path:
#         print("Performing sentiment analysis...")
#         analyze_sentiment(file_path)
#         print("Sentiment analysis completed.")
#     else:
#         print("File path is empty.")
#
# def read_dataset(file_path):
#     try:
#         df = pd.read_csv(file_path)
#         return df
#     except Exception as e:
#         print(f"Error reading dataset: {e}")
#         return None
#
# def extract_reviews_from_dataset(dataset):
#     review_columns = [col for col in dataset.columns if any(word in col.lower() for word in ['review', 'feedback', 'comment', 'description'])]
#     date_columns = [col for col in dataset.columns if any(word in col.lower() for word in ['date', 'posted', 'created'])]
#
#     # If no columns are identified using keywords, try a more generic approach
#     if not review_columns or not date_columns:
#         # Analyze content of each column to identify potential review and date columns
#         for col in dataset.columns:
#             # Check if the column contains mostly text with some punctuation and varying lengths
#             # This is a heuristic to identify potential review content
#             if dataset[col].dtype == object:
#                 text_ratio = sum(len(str(x)) > 20 and re.search(r'[^\w\s]', str(x)) for x in dataset[col]) / len(dataset[col])
#                 if text_ratio > 0.7:
#                     review_columns.append(col)
#                     break  # Add only the first column identified as potential review content
#
#             # Check if the column contains mostly dates in a consistent format (e.g., YYYY-MM-DD HH:MM:SS)
#             try:
#                 # Try converting the column to datetime format with specific format string '%Y-%m-%d %H:%M:%S'
#                 pd.to_datetime(dataset[col], format='%Y-%m-%d %H:%M:%S')
#                 date_columns.append(col)
#                 break  # Add only the first column identified with valid dates
#             except (ValueError, pd.errors.OutOfBoundsDatetime):
#                 pass  # Ignore exceptions if the column doesn't contain valid dates in the expected format
#
#     # Raise an error if no suitable columns are found
#     if not review_columns or not date_columns:
#         raise ValueError("Could not identify review or date columns in the dataset.")
#
#     # Select and rename the identified columns
#     review_column = review_columns[0]
#     date_column = date_columns[0]
#     extracted_reviews_df = dataset.rename(columns={review_column: "Review", date_column: "Date"})
#     return extracted_reviews_df[["Review", "Date"]]
# def main():
#     url, app_name, num_reviews, file_path = get_input()
#     if url:
#         driver = setup_driver(url)
#         click_see_all_reviews(driver)
#         while_loop = (int(num_reviews) / 10) + 10
#         scroll_to_buttons(driver, while_loop)
#         review_html = driver.page_source
#         reviews_df = scrape_app_reviews(review_html)
#         saved_file_path = save_reviews_to_csv(reviews_df, app_name, num_reviews)
#         driver.quit()
#         call_sentiment_analysis(saved_file_path)
#     elif file_path:
#         dataset = read_dataset(file_path)
#         if dataset is not None:
#             # Perform EDA
#             updated_dataset = perform_eda(file_path)
#             if updated_dataset is not None:
#                 # Save the updated dataset
#                 dataset = updated_dataset
#             else:
#                 print("Failed to perform EDA.")
#                 return
#             # Continue with scraping or other operations
#             if not app_name:
#                 app_name = input("Enter the app name: ")
#             reviews_df = extract_reviews_from_dataset(dataset)
#             if reviews_df is not None:
#                 current_time = datetime.datetime.now()
#                 current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
#                 file_name = f"{app_name}_dataset_reviews_{current_time_str}.csv"
#                 reviews_df.to_csv(file_name, index=False)
#                 print(f"Reviews extracted from dataset and saved to {file_name}")
#                 call_sentiment_analysis(file_name)
#             else:
#                 print("Failed to extract reviews from dataset.")
#         else:
#             print("Exiting.")
#
# if __name__ == "__main__":
#     main()
