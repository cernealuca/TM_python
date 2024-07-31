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

def retry_on_failure(action, *args, **kwargs):
    while True:
        try:
            action(*args, **kwargs)
            break
        except Exception as e:
            print(f"Retrying due to: {e}")
            time.sleep(2)

def accept_cookies():
    def action():
        # Wait for the cookie accept button to be clickable and click it
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/button[1]'))
        )
        cookie_button.click()
        print("Cookies accepted.")
    
    retry_on_failure(action)

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
        def select_all_checkbox_action():
            select_all_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'result-all'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", select_all_checkbox)
            driver.execute_script("arguments[0].click();", select_all_checkbox)
            print(f"Select All checkbox clicked on page {page_number}.")

        retry_on_failure(select_all_checkbox_action)
        
        # Wait for selection
        time.sleep(1)
        
        # Click the "Export" icon
        def export_button_action():
            export_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/button[2]'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", export_button)
            driver.execute_script("arguments[0].click();", export_button)
            print("Export button clicked.")
        
        retry_on_failure(export_button_action)
        
        # Wait for the export dialog
        time.sleep(1)
        
        # Click the confirm export CSV button
        def save_csv_button_action():
            save_csv_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[2]/div[2]/input'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", save_csv_button)
            driver.execute_script("arguments[0].click();", save_csv_button)
            print("Save CSV button clicked.")
        
        retry_on_failure(save_csv_button_action)
        
        # Wait for the dialog to process
        time.sleep(1)
        
        # Click the capital input button
        def capital_button_action():
            capital_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[3]/div[2]/div[8]/input'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", capital_button)
            driver.execute_script("arguments[0].click();", capital_button)
            print("Capital input button clicked.")
        
        retry_on_failure(capital_button_action)
        
        # Click the statut input button
        def statut_button_action():
            statut_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[3]/div[2]/div[11]/input'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", statut_button)
            driver.execute_script("arguments[0].click();", statut_button)
            print("Statut input button clicked.")
        
        retry_on_failure(statut_button_action)
        
        # Click the form juridique input button
        def form_juridique_button_action():
            form_juridique_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[3]/div[2]/div[6]/input'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", form_juridique_button)
            driver.execute_script("arguments[0].click();", form_juridique_button)
            print("Form juridique input button clicked.")
        
        retry_on_failure(form_juridique_button_action)
        
        # Click the final export button
        def final_export_button_action():
            final_export_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[9]/div/div/div[2]/form/div[4]/div/button[2]'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", final_export_button)
            driver.execute_script("arguments[0].click();", final_export_button)
            print("Final export button clicked.")
        
        retry_on_failure(final_export_button_action)
        
        # Wait for the download to complete
        time.sleep(1)
        
        # Check if the "Next" button is present and visible
        def next_page_button_action():
            next_page_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Suivant')]"))
            )
            if next_page_button.is_displayed():
                next_page_button.click()
                print("Next page button clicked.")
                return True
            else:
                print("Next page button is not visible.")
                return False

        if not retry_on_failure(next_page_button_action):
            print("No more pages to navigate or next page button not found.")
            break

# Navigate to the initial page and accept cookies
driver.get(base_url.format(1))
accept_cookies()

# Export data for the current page and navigate to the next pages
export_data()

print("Script completed. The browser will remain open for manual inspection.")
while True:
    time.sleep(10)
