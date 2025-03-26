from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging
import time
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
EVENT_URL = "https://kkboxhk.kktix.cc/events/laiying-kkbox"
LOGIN_URL = "https://kktix.com/users/sign_in"
MAX_ATTEMPTS = 1000  # Reduced to prevent excessive reloads


def initialize_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    return driver

# Function to log in to KKTIX
def login(driver, email, password):
    driver.get(LOGIN_URL)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "user[login]"))).send_keys(email)
        driver.find_element(By.NAME, "user[password]").send_keys(password)
        driver.find_element(By.NAME, "commit").click()
        WebDriverWait(driver, 5).until(EC.url_changes(LOGIN_URL))
        logger.info("Login successful!")
    except Exception as e:
        logger.error(f"Login failed: {e}")

# Function to handle the event page (look for "Buy Now" or "Next Step" button)
def handle_event_page(driver):
    driver.get(EVENT_URL)
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            logger.info(f"Attempt {attempts + 1}: Searching for buttons...")

            # Try finding 'Buy Now' or 'Next Step' button immediately
            button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/registrations/new')]"))
            )
            logger.info(f"Found button: {button.text.strip()} - Clicking...")
            button.click()
            return True
        except:
            attempts += 1
            driver.refresh()
    logger.error("Failed to find button after max attempts.")
    return False

# Main function to run the ticket buying process
def main():
    email = "kw.chu1965@gmail.com"
    password = "Chu98268775"
    driver = initialize_driver()
    login(driver, email, password)
    if not handle_event_page(driver):
        logger.error("Could not proceed to registration page.")
    else:
        logger.info("Successfully navigated to registration page.")
    # driver.quit()


if __name__ == "__main__":
    main()