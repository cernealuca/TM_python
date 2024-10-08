# Import necessary libraries
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
import pandas as pd
import os
import glob
import time
from datetime import datetime, timedelta
from pymongo import MongoClient  # Import MongoClient from pymongo

# Initialize MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = mongo_client["scraping_data"]  # Database name
collection = db["companies"]  # Collection name

# Initialize the WebDriver using WebDriverManager
service = ChromeService(executable_path='C:/Users/Admin/Downloads/chromedriver-win64/chromedriver.exe')  # Use double backslashes or forward slashes
options = webdriver.ChromeOptions()

# Set the default download directory for Chrome
csv_dir = 'exported_csvs'
os.makedirs(csv_dir, exist_ok=True)

options.add_experimental_option('prefs', {
    "download.default_directory": os.path.abspath(csv_dir),  # Change default directory for downloads
    "download.prompt_for_download": False,  # Disable download prompt
    "directory_upgrade": True  # For existing directories, don't ask for confirmation
})

# Predefined header for the merged CSV
PREDEFINED_HEADER = [
    "Dénomination / Nom", "Début d'activité", "SIREN", "Représentants",
    "Adresse du siège", "Forme juridique", "Activité", "Département",
    "Etablissements", "Capital", "Statut"
]

driver = webdriver.Chrome(service=service, options=options)

# URL to be opened
base_url = 'https://data.inpi.fr/search?advancedSearch=%257B%2522checkboxes%2522%253A%257B%2522status%2522%253A%257B%2522order%2522%253A0%252C%2522searchField%2522%253A%255B%2522is_rad%2522%255D%252C%2522values%2522%253A%255B%257B%2522value%2522%253A%2522false%2522%252C%2522checked%2522%253Atrue%257D%252C%257B%2522value%2522%253A%2522true%2522%252C%2522checked%2522%253Afalse%257D%255D%257D%257D%252C%2522texts%2522%253A%257B%257D%252C%2522multipleSelects%2522%253A%257B%257D%252C%2522dates%2522%253A%257B%257D%257D&displayStyle=List&filter=%257B%257D&nbResultsPerPage=100&order=asc&page=1&q=&searchType=advanced&sort=idt_date_debut_activ&type=companies'

# Open the URL
driver.get(base_url)
time.sleep(5)

def accept_cookies():
    try:
        # Wait for the cookie accept button to be clickable and click it
        cookie_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/button[1]'))
        )
        cookie_button.click()
        print("Cookies accepted.")
    except Exception as e:
        print(f"Error finding cookie accept button: {e}")
        time.sleep(3)

# Accept cookies
accept_cookies()
time.sleep(10)

def click_date_field():
    try:
        # Click on the "field data debut"
        date_field = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[9]/fieldset/div[1]/legend/h3'))
        )
        date_field.click()
        print("Date field clicked.")
    except Exception as e:
        print(f"Error clicking the date field: {e}")

def input_start_date():
    try:
        # Input start date
        start_date_field = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[9]/fieldset/div[2]/div/div[1]/input'))
        )
        start_date_field.clear()
        start_date_field.send_keys("01/01/1948")
        start_date_field.send_keys(Keys.RETURN)
        print("Start date set to 01/01/1948")
    except Exception as e:
        print(f"Error setting start date field: {e}")

def verify_start_date():
    try:
        # Wait and check if the displayed start date matches the input date
        displayed_start_date = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/p[1]/span'))
        ).text
        if displayed_start_date == "Depuis le 01/01/1948":
            print("Start date verification successful.")
            return True
        else:
            print(f"Start date verification failed. Displayed: {displayed_start_date}")
            return False
    except Exception as e:
        print(f"Error verifying start date: {e}")
        return False

def input_end_date():
    try:
        # Calculate end date (4 years after the start date)
        start_date = datetime.strptime("01/01/1948", "%m/%d/%Y")
        end_date = (start_date + timedelta(days=365*10)).strftime("%m/%d/%Y")
        
        # Input end date
        end_date_field = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[9]/fieldset/div[2]/div/div[2]/input'))
        )
        end_date_field.clear()
        end_date_field.send_keys(end_date)
        end_date_field.send_keys(Keys.RETURN)
        print(f"End date set to {end_date}")
    except Exception as e:
        print(f"Error setting end date field: {e}")

def verify_end_date():
    try:
        # Wait and check if the displayed end date matches the input date
        displayed_end_date = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/p[2]/span'))
        ).text
        expected_end_date = "Jusqu'au " + (datetime.strptime("01/01/1948", "%m/%d/%Y") + timedelta(days=365*10)).strftime("%d/%m/%Y")
        if displayed_end_date == expected_end_date:
            print("End date verification successful.")
            return True
        else:
            print(f"End date verification failed. Displayed: {displayed_end_date}")
            return False
    except Exception as e:
        print(f"Error verifying end date: {e}")
        return False

# Click the date field
click_date_field()
time.sleep(5)

# Input and verify the start date
start_date_verified = False
while not start_date_verified:
    input_start_date()
    time.sleep(15)
    #aici mai trebuie faceut ceva sa ne asiguram ca apuca sa se seteze data inainte sa se mai schimbe pagina
    #si apoi sa treaca la verificare
    start_date_verified = verify_start_date()

# Input and verify the end date
end_date_verified = False
while not end_date_verified:
    input_end_date()
    time.sleep(15)
    #aici mai trebuie faceut ceva sa ne asiguram ca apuca sa se seteze data inainte sa se mai schimbe pagina
    #si apoi sa treaca la verificare
    end_date_verified = verify_end_date()
    
time.sleep(10)
# Wait for the field to be clickable and click it
try:
    field_to_click = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[6]/fieldset/div[1]/legend/h3'))
    )
    field_to_click.click()
    print("Field clicked.")
except Exception as e:
    print(f"Error finding and clicking the field: {e}")
time.sleep(3)

# Function to click all checkboxes within the specified parent element
def click_all_checkboxes(parent_xpath):
    try:
        parent_element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, parent_xpath))
        )
        
        checkboxes = parent_element.find_elements(By.XPATH, './/div/div/input')
        remaining_checkboxes = [checkbox for checkbox in checkboxes if checkbox.get_attribute('id') != 'Forme_juridique-1000' and not checkbox.is_selected()]
        
        while remaining_checkboxes:
            for checkbox in remaining_checkboxes:
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", checkbox)
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f'//*[@id="{checkbox.get_attribute("id")}"]'))
                    ).click()
                    print(f"Checkbox with id {checkbox.get_attribute('id')} clicked.")
                except Exception as e:
                    print(f"Error clicking checkbox with id {checkbox.get_attribute('id')}: {e}")
                    continue
            
            checkboxes = parent_element.find_elements(By.XPATH, './/div/div/input')
            remaining_checkboxes = [checkbox for checkbox in checkboxes if checkbox.get_attribute('id') != 'Forme_juridique-1000' and not checkbox.is_selected()]
        
        print("All required checkboxes clicked.")
    except Exception as e:
        print(f"Error finding and checking checkboxes: {e}")

# Check and uncheck 'Forme_juridique-1000' if necessary
try:
    specific_checkbox = driver.find_element(By.ID, 'Forme_juridique-1000')
    if specific_checkbox.is_selected():
        specific_checkbox.click()
        print("Checkbox with id Forme_juridique-1000 deselected.")
except Exception as e:
    print(f"Error finding and deselecting the specific checkbox: {e}")

# Ensure all checkboxes are clicked
click_all_checkboxes('/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[6]/fieldset/div[2]/div')

# Final check and uncheck 'Forme_juridique-1000' if necessary
try:
    specific_checkbox = driver.find_element(By.ID, 'Forme_juridique-1000')
    if specific_checkbox.is_selected():
        specific_checkbox.click()
        print("Checkbox with id Forme_juridique-1000 deselected.")
except Exception as e:
    print(f"Error finding and deselecting the specific checkbox: {e}")

time.sleep(10)

def export_data():
    page_number = 1
    while True:
        # Wait for the "Select All" checkbox to be clickable and click it
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
        
        # Wait for selection
        # time.sleep(10)
        
        # Click the "Export" icon
        try:
            export_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/button[2]'))
            )
            export_button.click()
            print("Export button clicked.")
        except Exception as e:
            print(f"Error finding export button on page {page_number}: {e}")
            return
        
        # Wait for the export dialog
        time.sleep(3)
        # Click the confirm export CSV button
        try:
            save_csv_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[2]/div[2]/input'))
            )
            save_csv_button.click()
            print("Save CSV button clicked.")
        except Exception as e:
            print(f"Error finding save CSV button: {e}")
            return

        # Wait for the dialog to process
        time.sleep(3)
        # Function to check and click the "Select All" checkbox in the CSV export dialog
        def check_and_click_select_all():
            try:
                select_all_csv_checkbox = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[3]/div[1]/div[1]/input'))
                )
                time.sleep(3)
                if not select_all_csv_checkbox.is_selected():
                    select_all_csv_checkbox.click()
                    print("Select All CSV checkbox clicked.")
                else:
                    print("Select All CSV checkbox was already clicked.")
            except Exception as e:
                print(f"Error finding and clicking Select All CSV checkbox: {e}")

        # Call the function to check and click the "Select All" checkbox
        check_and_click_select_all()

        # Click the final export button
        try:
            final_export_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[4]/div/button[2]'))
            )
            final_export_button.click()
            print("Final export button clicked.")
        except Exception as e:
            print(f"Error finding final export button: {e}")
            return
        
        # Wait for the download to complete
        time.sleep(3)
        try:
            select_all_checkbox = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.ID, 'result-all'))
            )
            driver.execute_script("arguments[0].click();", select_all_checkbox)
            print(f"Select All checkbox clicked on page {page_number}.")
        except Exception as e:
            print(f"Error finding select all checkbox on page {page_number}: {e}")
            return
        time.sleep(3)
        # Check if the "Next" button is present and visible
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

# Export data for the current page and navigate to the next pages
export_data()
time.sleep(10)

# Function to clean each CSV file by removing the first three rows
def clean_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove the first three rows
    clean_lines = lines[3:]

    # Convert the cleaned lines back to a DataFrame
    from io import StringIO
    clean_data = StringIO(''.join(clean_lines))
    df = pd.read_csv(clean_data, sep=';', header=None)

    return df

# Merge all cleaned CSV files into a single CSV and insert into MongoDB
def merge_csv_files(directory, output_file):
    all_files = glob.glob(os.path.join(directory, "*.csv"))
    all_data = []
    bad_files = []

    # Ensure the directory contains CSV files
    if not all_files:
        print("No CSV files found in the directory.")
        return

    # Iterate over all files
    for file in all_files:
        try:
            # Clean the CSV file and get the DataFrame
            df = clean_csv_file(file)

            # Assign the predefined header to each dataframe
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
        # Concatenate all dataframes
        merged_df = pd.concat(all_data, ignore_index=True)

        # Write the merged data to CSV with the predefined header
        merged_df.to_csv(output_file, sep=';', index=False, quoting=csv.QUOTE_ALL)
        print(f"All CSV files merged into {output_file}")

        # Insert data into MongoDB
        records = merged_df.to_dict('records')  # Convert dataframe to list of dictionaries
        collection.insert_many(records)  # Insert records into MongoDB
        print(f"Data inserted into MongoDB collection '{collection.name}'.")
    else:
        print("No data to merge.")

# Call the merge function
merge_csv_files(csv_dir, os.path.join(csv_dir, "merged_data.csv"))

print("Script completed. The browser will remain open for manual inspection.")
while True:
    time.sleep(10)
