import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import glob
import time
from datetime import datetime, timedelta
from pymongo import MongoClient
from selenium.common.exceptions import NoAlertPresentException

# Initialize MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = mongo_client["scraping_TM_France_data"]  # Database name
collection = db["TM_France"]  # Collection name

# Initialize the WebDriver using WebDriverManager
service = ChromeService(executable_path='C:\chromedriver-win64/chromedriver.exe')  # Use double backslashes or forward slashes
options = webdriver.ChromeOptions()

# Set the default download directory for Chrome
csv_dir = 'trademark_csvs'
os.makedirs(csv_dir, exist_ok=True)

options.add_experimental_option('prefs', {
    "download.default_directory": os.path.abspath(csv_dir),  # Change default directory for downloads
    "download.prompt_for_download": False,  # Disable download prompt
    "directory_upgrade": True  # For existing directories, don't ask for confirmation
})

# Predefined header for the merged CSV
PREDEFINED_HEADER = [
    "Logo / Image", "Origine", "N° de la marque", "Marque", "Translitération / traduction", 
    "Type de la marque", "Date de dépôt/enregistrement", "Pays de prioritate", "Date de prioritate",
    "n° de prioritate", "Classification des éléments figuratifs (Vienne)", "Classification de Nice",
    "Produits et servicii", "Nom du déposant", "SIREN du déposant", "Département du déposant", 
    "Pays du déposant", "Nom du mandataire", "SIREN du mandataire", "Département du mandataire", 
    "Pays du mandataire", "Statut", "Pays d'ancienneté", "Date d'ancienneté", "n° d'ancienneté", 
    "Pays désignés"
]

driver = webdriver.Chrome(service=service, options=options)

# URL to be opened
base_url = 'https://data.inpi.fr/search?advancedSearch=%257B%2522checkboxes%2522%253A%257B%2522bases_choice%2522%253A%257B%2522order%2522%253A0%252C%2522searchField%2522%253A%255B%2522registrationOfficeCode%2522%255D%252C%2522values%2522%253A%255B%257B%2522value%2522%253A%2522FR%2522%252C%2522checked%2522%253Atrue%257D%252C%257B%2522value%2522%253A%2522EM%2522%252C%2522checked%2522%253Atrue%257D%252C%257B%2522value%2522%253A%2522WO%2522%252C%2522checked%2522%253Atrue%257D%255D%257D%252C%2522brands_validity%2522%253A%257B%2522order%2522%253A1%252C%2522searchField%2522%253A%255B%2522expiryDate%2522%255D%252C%2522values%2522%253A%255B%257B%2522value%2522%253A%2522applicable%2522%252C%2522checked%2522%253Atrue%257D%252C%257B%2522value%2522%253A%2522not_applicable%2522%252C%2522checked%2522%253Afalse%257D%255D%257D%257D%252C%2522texts%2522%253A%257B%257D%252C%2522multipleSelects%2522%253A%257B%257D%252C%2522dates%2522%253A%257B%257D%257D&displayStyle=List&filter=%257B%257D&nbResultsPerPage=100&order=asc&page=1&q=&searchType=advanced&sort=applicationDate&type=brands'

# Function to accept cookies
def accept_cookies():
    try:
        cookie_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/button[1]'))
        )
        cookie_button.click()
        print("Cookies accepted.")
    except Exception as e:
        print(f"Error finding cookie accept button: {e}")
        time.sleep(3)

# Function to click on the date field
def click_date_field():
    try:
        date_field = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[5]/fieldset/div[1]'))
        )
        date_field.click()
        print("Date field clicked.")
    except Exception as e:
        print(f"Error clicking the date field: {e}")

# Function to input the start date
def input_start_date(start_date):
    try:
        start_date_field = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[5]/fieldset/div[2]/div/div[1]/input'))
        )
        start_date_field.clear()
        start_date_field.send_keys(start_date)
        start_date_field.send_keys(Keys.RETURN)
        print(f"Start date set to {start_date}")
    except Exception as e:
        print(f"Error setting start date field: {e}")
 
time.sleep(10)       
    

# Function to verify the start date
def verify_start_date(expected_date):
    try:
        displayed_start_date = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/p[1]/span'))
        ).text
        if displayed_start_date == f"Depuis le {expected_date}":
            print("Start date verification successful.")
            return True
        else:
            print(f"Start date verification failed. Displayed: {displayed_start_date}")
            return False
    except Exception as e:
        print(f"Error verifying start date: {e}")
        return False

# Function to input the end date
def input_end_date(end_date):
    try:
        end_date_field = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[5]/fieldset/div[2]/div/div[2]/input'))
        )
        end_date_field.clear()
        end_date_field.send_keys(end_date)
        end_date_field.send_keys(Keys.RETURN)
        print(f"End date set to {end_date}")
    except Exception as e:
        print(f"Error setting end date field: {e}")
time.sleep(10)
# Function to verify the end date
def verify_end_date(expected_date):
    try:
        displayed_end_date = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/p[2]/span'))
        ).text
        if displayed_end_date == f"Jusqu'au {expected_date}":
            print(f"End date verification successful: {displayed_end_date}")
            return True
        else:
            print(f"End date verification failed. Displayed: {displayed_end_date}")
            return False
    except Exception as e:
        print(f"Error verifying end date: {e}")
        return False

# Function to get the number of results
def get_result_count():
    retries = 3  # Retry a few times if it fails
    for attempt in range(retries):
        try:
            result_count_text = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[3]/span[2]'))
            ).text
            # Extract the total results number from the string
            result_count = int(result_count_text.split('sur')[1].split('résultats')[0].replace(' ', '').replace('.', '').replace(',', ''))
            print(f"Result count retrieved: {result_count}")
            return result_count
        except Exception as e:
            print(f"Error getting result count (attempt {attempt + 1} of {retries}): {e}")
            time.sleep(5)  # Wait and retry
    return None

# Function to adjust end date if results exceed 10,000
def adjust_end_date_if_needed(start_date, end_date, initial_days):
    while True:
        # Set the end date only if it's not already verified
        input_end_date(end_date)
        time.sleep(15)  # Allow time for results to load

        # Verify the end date is set correctly before counting results
        end_date_verified = verify_end_date(datetime.strptime(end_date, "%d/%m/%Y").strftime("%d/%m/%Y"))
        if not end_date_verified:
            print(f"End date {end_date} not verified, retrying...")
            continue
        
        result_count = get_result_count()
        
        if result_count is not None and result_count > 10000:
            print(f"Result count is {result_count}, which exceeds 10,000. Adjusting the end date.")
            # Reduce the timeframe by 1/3
            new_total_days = initial_days * 3 // 4
            end_date = (datetime.strptime(start_date, "%d/%m/%Y") + timedelta(days=new_total_days)).strftime("%d/%m/%Y")
            print(f"New end date set to {end_date}")
            initial_days = new_total_days  # Update the initial_days for the next iteration
        else:
            # When the result count is within acceptable limits, skip setting the end date again.
            if result_count is not None and result_count <= 10000:
                print(f"Result count {result_count} is within limits. Proceeding without changing the end date.")
                return end_date, initial_days

# Function to handle any alert that may appear
def handle_alert():
    try:
        # Switch to the alert
        alert = driver.switch_to.alert
        # Print the alert text if needed for debugging
        print(f"Alert text: {alert.text}")
        # Accept the alert (this is equivalent to pressing "OK")
        alert.accept()
        print("Alert accepted.")
    except NoAlertPresentException:
        print("No alert present.")

# Function to export data
def export_data():
    page_number = 1
    while True:
        try:
            select_all_checkbox = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.ID, 'result-all'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", select_all_checkbox)
            driver.execute_script("arguments[0].click();", select_all_checkbox)
            print(f"Select All checkbox clicked on page {page_number}.")
        except Exception as e:
            print(f"Error finding select all checkbox on page {page_number}: {e}")
            return

        try:
            export_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/button[2]'))
            )
            driver.execute_script("arguments[0].click();", export_button)
            print("Export button clicked.")
        except Exception as e:
            print(f"Error finding export button on page {page_number}: {e}")
            return

        time.sleep(3)

        try:
            save_csv_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[8]/div/div/div[2]/form/div[2]/div[2]/input'))
            )
            driver.execute_script("arguments[0].click();", save_csv_button)
            print("Save CSV button clicked.")
        except Exception as e:
            print(f"Error finding save CSV button: {e}")
            return

        time.sleep(3)

        try:
            final_export_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//html/body/div[1]/main/div[8]/div/div/div[2]/form/div[4]/div/button[2]'))
            )
            driver.execute_script("arguments[0].click();", final_export_button)
            print("Final export button clicked.")
        except Exception as e:
            print(f"Error finding final export button: {e}")
            return
        
        time.sleep(3)

        # Handle any alert that may appear after export
        handle_alert()

        time.sleep(10)
        
        try:
            select_all_checkbox = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.ID, 'result-all'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", select_all_checkbox)
            driver.execute_script("arguments[0].click();", select_all_checkbox)
            print(f"Select All checkbox clicked on page {page_number}.")
        except Exception as e:
            print(f"Error finding select all checkbox on page {page_number}: {e}")
            return

        time.sleep(3)

    

        try:
            next_page_button = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Suivant')]"))
            )
            if next_page_button.is_displayed():
                next_page_button.click()
                print("Next page button clicked.")
                page_number += 1
                time.sleep(1)
            else:
                print("Next page button is not visible.")
                break
        except Exception as e:
            print("No more pages to navigate or next page button not found.")
            break

# Function to clean a CSV file
def clean_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    clean_lines = lines[3:]
    from io import StringIO
    clean_data = StringIO(''.join(clean_lines))
    df = pd.read_csv(clean_data, sep=';', header=None)
    return df

# Function to delete all CSV files including the merged CSV
def delete_all_csv_files(directory):
    all_files = glob.glob(os.path.join(directory, "*.csv"))
    for file in all_files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")
    print("All CSV files, including the merged file, have been deleted.")


def merge_csv_files(directory, output_file):
    all_files = glob.glob(os.path.join(directory, "*.csv"))
    all_data = []
    bad_files = []

    if not all_files:
        print("No CSV files found in the directory.")
        return

    for file in all_files:
        try:
            df = clean_csv_file(file)
            df.columns = PREDEFINED_HEADER
            all_data.append(df)
        except pd.errors.ParserError as e:
            print(f"ParserError encountered in file {file}: {e}")
            bad_files.append(file)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            bad_files.append(file)

    if bad_files:
        print("The following files had issues and were skipped:")
        for bad_file in bad_files:
            print(bad_file)

    if all_data:
        merged_df = pd.concat(all_data, ignore_index=True)
        merged_df.to_csv(output_file, sep=';', index=False, quoting=csv.QUOTE_ALL)
        print(f"All CSV files merged into {output_file}")
        records = merged_df.to_dict('records')
        collection.insert_many(records)
        print(f"Data inserted into MongoDB collection '{collection.name}'.")

        # After merging and inserting, delete all CSV files including the merged one
        delete_all_csv_files(directory)
    else:
        print("No data to merge.")


# Continuous loop to execute the process
start_date = "10/04/2006"  # Initial start date
initial_days = 90  # Define the initial number of days

while True:
    driver.get(base_url)
    time.sleep(10)
    
    accept_cookies()
    time.sleep(10)
    
    click_date_field()
    time.sleep(5)
    
    # Initialize end date
    end_date = (datetime.strptime(start_date, "%d/%m/%Y") + timedelta(days=initial_days)).strftime("%d/%m/%Y")
    
    start_date_verified = False
    while not start_date_verified:
        input_start_date(datetime.strptime(start_date, "%d/%m/%Y").strftime("%d/%m/%Y"))
        time.sleep(15)
        start_date_verified = verify_start_date(datetime.strptime(start_date, "%d/%m/%Y").strftime("%d/%m/%Y"))
    
    end_date_verified = False
    while not end_date_verified:
        time.sleep(15)

        # Adjust end date only if necessary
        new_end_date, initial_days = adjust_end_date_if_needed(start_date, end_date, initial_days)
    
        # Only verify the end date if it was actually adjusted
        if new_end_date != end_date:
            end_date_verified = verify_end_date(datetime.strptime(new_end_date, "%d/%m/%Y").strftime("%d/%m/%Y"))
            end_date = new_end_date
        else:
            end_date_verified = True
            print(f"End date {end_date} retained as no adjustment was necessary.")

    
    export_data()

    time.sleep(3)
     # Handle any alert that may appear after export
    handle_alert()
    time.sleep(10)
    
    merge_csv_files(csv_dir, os.path.join(csv_dir, "mergedTM_data.csv"))
    
    # Update the start date for the next iteration
    start_date = datetime.strptime(end_date, "%d/%m/%Y").strftime("%d/%m/%Y")
