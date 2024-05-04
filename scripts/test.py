from selenium import webdriver
from selenium.webdriver.common.by import By
import time

print("Launching the INPI website")

# Initialize the WebDriver
driver = webdriver.Chrome()
driver.get('https://www.inpi.fr/en/')

# Allow some time for the page to load
time.sleep(15)  # Adjust based on your internet speed and website response

# try:
#     # Find the button by its text "Anglais" and click it
#     english_button = driver.find_element(By.LINK_TEXT, 'Anglais')
#     english_button.click()
#     print("Language changed to English")

# except Exception as e:
#     print(f"An error occurred: {e}")

# finally:
#     # Allow time to observe changes (optional)
#     time.sleep(5)

#     # Close the browser
#     driver.quit()
