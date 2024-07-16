from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time

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
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/button[1]'))
        )
        cookie_button.click()
        print("Cookies accepted.")
    except Exception as e:
        print(f"Error finding cookie accept button: {e}")

def click_and_wait(element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element)).click()

# Accept cookies
accept_cookies()

# Click the business type field
try:
    field_to_business = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[6]/fieldset/div[1]/legend/h3'))
    )
    click_and_wait(field_to_business)
    print("Field clicked.")
except Exception as e:
    print(f"Error finding and clicking the field: {e}")
time.sleep(3)

# Click checkboxes except the specified one
try:
    checkboxes_business = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[6]/fieldset/div[2]/div/div/div/input'))
    )
    
    for checkbox in checkboxes_business:
        if checkbox.get_attribute('id') != 'Forme_juridique-1000':
            if not checkbox.is_selected():
                try:
                    click_and_wait(checkbox)
                    print(f"Checkbox with id {checkbox.get_attribute('id')} clicked.")
                except Exception as e:
                    print(f"Error clicking checkbox {checkbox.get_attribute('id')}: {e}")
        else:
            print("Checkbox with id Forme_juridique-1000 skipped.")
except Exception as e:
    print(f"Error finding and checking checkboxes: {e}")

def click_date_field():
    try:
        date_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[1]/div/fieldset/div[9]/fieldset/div[1]/legend/h3'))
        )
        click_and_wait(date_field)
        print("Date field clicked.")
    except Exception as e:
        print(f"Error clicking the date field: {e}")

def input_start_date():
    try:
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
        start_date = datetime.strptime("01/01/1948", "%m/%d/%Y")
        end_date = (start_date + timedelta(days=365*4)).strftime("%m/%d/%Y")
        
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
        displayed_end_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/p[2]/span'))
        ).text
        expected_end_date = "Jusqu'au " + (datetime.strptime("01/01/1948", "%m/%d/%Y") + timedelta(days=365*4)).strftime("%d/%m/%Y")
        if displayed_end_date == expected_end_date:
            print("End date verification successful.")
            return True
        else:
            print(f"End date verification failed. Displayed: {displayed_end_date}")
            return False
    except Exception as e:
        print(f"Error verifying end date: {e}")
        return False

click_date_field()

start_date_verified = False
while not start_date_verified:
    input_start_date()
    time.sleep(2)
    start_date_verified = verify_start_date()

end_date_verified = False
while not end_date_verified:
    input_end_date()
    time.sleep(2)
    end_date_verified = verify_end_date()

print("Script completed. The browser will remain open for manual inspection.")
while True:
    time.sleep(1000)
