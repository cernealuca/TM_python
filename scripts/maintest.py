from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time

def main():
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

    # Accept cookies
    accept_cookies()

    # Script 1 functionality
    # Wait for the field to be clickable and click it
    try:
        field_to_click = WebDriverWait(driver, 10).until(
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
            parent_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, parent_xpath))
            )
            
            checkboxes = parent_element.find_elements(By.XPATH, './/div/div/input')
            
            for checkbox in checkboxes:
                if checkbox.get_attribute('id') != 'Forme_juridique-1000' and not checkbox.is_selected():
                    checkbox.click()
                    print(f"Checkbox with id {checkbox.get_attribute('id')} clicked.")
        except Exception as e:
            print(f"Error finding and checking checkboxes: {e}")

    # First pass to click all checkboxes except 'Forme_juridique-1000'
    click_all_checkboxes('/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[6]/fieldset/div[2]/div')

    # Check and uncheck 'Forme_juridique-1000' if necessary
    try:
        specific_checkbox = driver.find_element(By.ID, 'Forme_juridique-1000')
        if specific_checkbox.is_selected():
            specific_checkbox.click()
            print("Checkbox with id Forme_juridique-1000 deselected.")
    except Exception as e:
        print(f"Error finding and deselecting the specific checkbox: {e}")

    # Second pass to ensure all checkboxes are clicked
    click_all_checkboxes('/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[6]/fieldset/div[2]/div')

    # Final check and uncheck 'Forme_juridique-1000' if necessary
    try:
        specific_checkbox = driver.find_element(By.ID, 'Forme_juridique-1000')
        if specific_checkbox.is_selected():
            specific_checkbox.click()
            print("Checkbox with id Forme_juridique-1000 deselected.")
    except Exception as e:
        print(f"Error finding and deselecting the specific checkbox: {e}")

    # Script 2 functionality
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

    def input_end_date():
        try:
            # Calculate end date (4 years after the start date)
            start_date = datetime.strptime("01/01/1948", "%d/%m/%Y")
            end_date = (start_date + timedelta(days=365*4)).strftime("%d/%m/%Y")
            
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

    # Click the date field
    click_date_field()

    # Input the start and end dates
    input_start_date()
    input_end_date()

    print("Script completed. The browser will remain open for manual inspection.")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
