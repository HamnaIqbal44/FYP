from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from bs4 import BeautifulSoup
import re
import datetime

def get_input():
    choice = input("Enter 'URL' to scrape reviews from a webpage or 'FILE' to extract from a dataset file: ").strip().lower()
    if choice == 'url':
        url = input("Enter the URL: ")
        app_name = input("Enter the app name: ")
        app_name = re.sub(r'[^a-zA-Z0-9\s]', '', app_name)  # Remove special characters from app name
        num_reviews = input('Enter the number of reviews to scrape: ')
        approx_t = (6 + ((int(num_reviews) / 10) + 10) * 3)
        print(f'Approximate time to scrape: {approx_t} minutes')
        return url, app_name, num_reviews, None
    elif choice == 'file':
        file_path = input("Enter the path to the dataset file: ")
        return None, None, None, file_path
    else:
        print("Invalid choice.")
        return None, None, None, None

def setup_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    return driver

def click_see_all_reviews(driver):
    see_all_reviews_button = driver.find_element(By.CSS_SELECTOR, '''.Jwxk6d > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1) > span:nth-child(4)''')
    see_all_reviews_button.click()
    time.sleep(3)

def scroll_to_buttons(driver, while_loop):
    i = 0
    n = 0
    while i < while_loop:
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.mN1ivc[data-disable-idom='true'][aria-expanded='false'][aria-haspopup='menu']")
        start = len(buttons)
        for button in buttons[n:]:
            for _ in range(5):
                driver.execute_script("arguments[0].scrollIntoView();", button)
        n = start
        i += 1
        time.sleep(3)

def scrape_app_reviews(html):
    if html:
        soup = BeautifulSoup(html, "html.parser")
        reviews = []
        for review_container in soup.find_all("div", class_="RHo1pe"):
            name_element = review_container.find("div", class_="YNR7H").find("div", class_="X5PpBb")
            reviewer_name = name_element.text.strip() if name_element else None

            date_element = review_container.find("span", class_="bp9Aid")
            review_date = date_element.text.strip() if date_element else None

            review_text_element = review_container.find("div", class_="h3YV2d")
            review_text = review_text_element.text.strip() if review_text_element else None

            review = {
                "Name": reviewer_name,
                "Date": review_date,
                "Review": review_text
            }
            reviews.append(review)

        df = pd.DataFrame(reviews)
        return df

    else:
        print("Error: No HTML provided.")
        return None

def save_reviews_to_csv(reviews_df, app_name, num_reviews):
    if reviews_df is not None:
        reviews_df = reviews_df.head(int(num_reviews))
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{app_name}_{current_time_str}.csv"
        reviews_df.to_csv(file_name, index=False)
        print(f"Reviews scraped and saved to {file_name}")
    else:
        print("Failed to scrape reviews.")

def read_dataset(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading dataset: {e}")
        return None

# def extract_reviews_from_dataset(dataset):
#     review_columns = [col for col in dataset.columns if 'review' in col.lower()]
#     date_columns = [col for col in dataset.columns if 'date' in col.lower()]
#
#     if review_columns and date_columns:
#         review_column = review_columns[0]
#         date_column = date_columns[0]
#         return dataset[[review_column, date_column]]
#     else:
#         print("Error: Review or Date column not found in the dataset.")
#         return None

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
        date_pattern1 = re.compile(r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b')
        date_pattern2 = re.compile(r'\b(\w{3,9} \d{1,2}, \d{4})\b')  # Month name, Day, Year
        if col_data.dtype == object:
            text_data = ' '.join(col_data.dropna().astype(str))
            matches = date_pattern1.findall(text_data) + date_pattern2.findall(text_data)
            date_ratio = len(matches) / len(col_data.dropna())
            if date_ratio > 0.5:  # Adjust the ratio threshold as needed
                return True
        return False
        # if col_data.dtype == object:
        #     text_data = ' '.join(col_data.dropna().astype(str))
        #     matches = date_pattern.findall(text_data)
        #     date_ratio = len(matches) / len(col_data.dropna())
        #     if date_ratio > 0.5:  # Adjust the ratio threshold as needed
        #         return True
        # return False

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
        extracted_reviews_df = dataset.rename(columns={review_column: "Review", date_column: "Date"})
        return extracted_reviews_df[["Review", "Date"]]
    else:
        if not review_column:
            print("Error: Review column not found in the dataset.")
        if not date_column:
            print("Error: Date column not found in the dataset.")
        return None

def main():
    url, app_name, num_reviews, file_path = get_input()
    if url:
        driver = setup_driver(url)
        click_see_all_reviews(driver)
        while_loop = (int(num_reviews) / 10) + 10
        scroll_to_buttons(driver, while_loop)
        review_html = driver.page_source
        reviews_df = scrape_app_reviews(review_html)
        save_reviews_to_csv(reviews_df, app_name, num_reviews)
        driver.quit()
    elif file_path:
        dataset = read_dataset(file_path)
        if dataset is not None:
            if not app_name:
                app_name = input("Enter the app name: ")
            reviews_df = extract_reviews_from_dataset(dataset)
            if reviews_df is not None:
                current_time = datetime.datetime.now()
                current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                file_name = f"{app_name}_dataset_reviews_{current_time_str}.csv"
                reviews_df.to_csv(file_name, index=False)
                print(f"Reviews extracted from dataset and saved to {file_name}")
            else:
                print("Failed to extract reviews from dataset.")
        else:
            print("Exiting.")


if __name__ == "__main__":
    main()
