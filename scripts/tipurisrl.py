from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver using WebDriverManager
service = ChromeService(executable_path='C:/Users/Admin/Downloads/chromedriver-win64/chromedriver.exe')  # Use double backslashes or forward slashes
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

# Keep the browser open for inspection indefinitely
print("Script completed. The browser will remain open for manual inspection.")
while True:
    time.sleep(10)
