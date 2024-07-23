from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Initialize the WebDriver using WebDriverManager
service = ChromeService(executable_path='C:/Users/Admin/Downloads/chromedriver-win64/chromedriver.exe')  # Use double backslashes or forward slashes
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# URL for the first page
base_url = 'https://data.inpi.fr/search?advancedSearch=%257B%2522checkboxes%2522%253A%257B%2522status%2522%253A%257B%2522order%2522%253A0%252C%2522searchField%2522%253A%255B%2522is_rad%2522%255D%252C%2522values%2522%253A%255B%257B%2522value%2522%253A%2522false%2522%252C%2522checked%2522%253Atrue%257D%252C%257B%2522value%2522%253A%2522true%2522%252C%2522checked%2522%253Afalse%257D%255D%257D%257D%252C%2522texts%2522%253A%257B%257D%252C%2522multipleSelects%2522%253A%257B%257D%252C%2522dates%2522%253A%257B%257D%257D&displayStyle=List&filter=%257B%2522denominationOuNomPatronymique.folding%2522%253A%2522efa%2522%257D&nbResultsPerPage=100&order=asc&page={}'

# Directory to save CSVs
csv_dir = 'exported_csvs'
os.makedirs(csv_dir, exist_ok=True)
time.sleep(1)

def accept_cookies():
    try:
        # Wait for the cookie accept button to be clickable and click it
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/button[1]'))
        )
        cookie_button.click()
        print("Cookies accepted.")
    except Exception as e:
        print(f"Error finding cookie accept button: {e}")
        time.sleep(3)

def export_data():
    page_number = 1
    while True:
        accept_cookies()
        # Navigate to the page
        driver.get(base_url.format(page_number))
        
        # Ensure cookies are accepted
        if page_number == 1:
            accept_cookies()
        
        # Wait for the "Select All" checkbox to be clickable
        try:
            select_all_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'result-all'))
            )
            select_all_checkbox.click()
            print(f"Select All checkbox clicked on page {page_number}.")
        except Exception as e:
            print(f"Error finding select all checkbox on page {page_number}: {e}")
            return
        
        # Wait for selection
        time.sleep(1)
        
        # Click the "Export" icon
        try:
            export_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/button[2]'))
            )
            export_button.click()
            print("Export button clicked.")
        except Exception as e:
            print(f"Error finding export button on page {page_number}: {e}")
            return
        
        # Wait for the export dialog
        time.sleep(1)
        
        # Click the confirm export CSV button
        try:
            save_csv_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[2]/div[2]/input'))
            )
            save_csv_button.click()
            print("Save CSV button clicked.")
        except Exception as e:
            print(f"Error finding save CSV button: {e}")
            return

        # Wait for the dialog to process
        time.sleep(1)
        
        # Click the capital input button
        try:
            capital_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[3]/div[2]/div[8]/input'))
            )
            capital_button.click()
            print("Capital input button clicked.")
        except Exception as e:
            print(f"Error finding capital input button: {e}")
            return
        
        # Click the statut input button
        try:
            statut_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[3]/div[2]/div[11]/input'))
            )
            statut_button.click()
            print("Statut input button clicked.")
        except Exception as e:
            print(f"Error finding statut input button: {e}")
            return

        # Click the form juridique input button
        try:
            form_juridique_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[3]/div[2]/div[6]/input'))
            )
            form_juridique_button.click()
            print("Form juridique input button clicked.")
        except Exception as e:
            print(f"Error finding form juridique input button: {e}")
            return

        # Click the final export button
        try:
            final_export_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[4]/div/button[2]'))
            )
            final_export_button.click()
            print("Final export button clicked.")
        except Exception as e:
            print(f"Error finding final export button: {e}")
            return
        
        # Wait for the download to complete
        time.sleep(1)
        
        # Check if the "Next" button is present and visible
        try:
            next_page_button = WebDriverWait(driver, 10).until(
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

# Navigate to the initial page and accept cookies
driver.get(base_url.format(1))
accept_cookies()

# Export data for the current page and navigate to the next pages
export_data()

print("Script completed. The browser will remain open for manual inspection.")
