from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time
import os


# Initialize the WebDriver using WebDriverManager
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to be opened
base_url = 'https://data.inpi.fr/search?advancedSearch=%257B%2522checkboxes%2522%253A%257B%2522status%2522%253A%257B%2522order%2522%253A0%252C%2522searchField%2522%253A%255B%2522is_rad%2522%255D%252C%2522values%2522%253A%255B%257B%2522value%2522%253A%2522false%2522%252C%2522checked%2522%253Atrue%257D%252C%257B%2522value%2522%253A%2522true%2522%252C%2522checked%2522%253Afalse%257D%255D%257D%257D%252C%2522texts%2522%253A%257B%257D%252C%2522multipleSelects%2522%253A%257B%257D%252C%2522dates%2522%253A%257B%257D%257D&displayStyle=List&filter=%257B%257D&nbResultsPerPage=100&order=asc&page=1&q=&searchType=advanced&sort=relevance&type=companies'

# Open the URL
driver.get(base_url)
time.sleep(3)

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

# Wait for the field to be clickable and click it
try:
    accept_cookies()
    field_to_business = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[6]/fieldset/div[1]/legend/h3'))
    )
    field_to_business.click()
    print("Field clicked.")
except Exception as e:
    print(f"Error finding and clicking the field: {e}")
time.sleep(3)

# Wait for the checkboxes to be present and check all except the specified one
try:
    checkboxes_business = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[6]/fieldset/div[2]/div/div/div/input'))
    )
    
    for checkbox in checkboxes_business:
        if checkbox.get_attribute('id') != 'Forme_juridique-1000':
            if not checkbox.is_selected():
                checkbox.click()
                print(f"Checkbox with id {checkbox.get_attribute('id')} clicked.")
        else:
            print("Checkbox with id Forme_juridique-1000 skipped.")
except Exception as e:
    print(f"Error finding and checking checkboxes: {e}")


def click_date_field():
    try:
        # Click on the "field data debut"
        date_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[9]/fieldset/div[1]/legend/h3'))
        )
        date_field.click()
        print("Date field clicked.")
    except Exception as e:
        print(f"Error clicking the date field: {e}")

def input_start_date():
    try:
        # Input start date
        start_date_field = WebDriverWait(driver, 10).until(
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
        displayed_start_date = WebDriverWait(driver, 10).until(
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
        end_date = (start_date + timedelta(days=365*4)).strftime("%m/%d/%Y")
        
        # Input end date
        end_date_field = WebDriverWait(driver, 10).until(
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
        displayed_end_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/p[2]/span'))
        ).text
        expected_end_date = "Jusqu'au " + (datetime.strptime("01/01/1948", "%d/%m/%Y") + timedelta(days=365*6)).strftime("%d/%m/%Y")
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

# Input and verify the start date
start_date_verified = False
while not start_date_verified:
    input_start_date()
    time.sleep(2)
    start_date_verified = verify_start_date()

# Input and verify the end date
end_date_verified = False
while not end_date_verified:
    input_end_date()
    time.sleep(2)
    end_date_verified = verify_end_date()

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
