from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time
import random
import db  # Assuming this is your database module (not used in this script)

# Set up logging for better debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kktix_ticket_buyer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
PREFERRED_TICKET_TYPE = "HK$980 VIP"  # Preferred ticket type (e.g., 'HK$980 VIP' or 'HK$780')
TICKET_QUANTITY = "1"  # Number of tickets to purchase (e.g., '1', '2', etc.)
MAX_RELOAD_ATTEMPTS = 350000  # Max reloads (covers 4 days: 350,000 x ~1 second)
EVENT_URL = "https://edproduction.kktix.cc/events/chiaifujikawa-livetour-hk-2025"
LOGIN_URL = "https://kktix.com/users/sign_in?back_to=https%3A%2F%2Fkktix.com%2F"


# Function to initialize the WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Maximize the browser window
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # Uncomment the line below to run in headless mode (no browser UI)
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    # Spoof navigator.webdriver to avoid detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver


# Function to simulate human-like behavior
def simulate_human_behavior(driver):
    # Random scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(0.1, 0.2))
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(random.uniform(0.1, 0.2))

    # Random mouse movement
    action = ActionChains(driver)
    action.move_by_offset(random.randint(100, 500), random.randint(100, 500)).perform()
    time.sleep(random.uniform(0.2, 0.8))


# Function to force page load
def force_page_load(driver):
    # Scroll multiple times to trigger lazy loading
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(0.1, 0.2))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.1, 0.2))

    # Force any remaining JavaScript to execute
    driver.execute_script("window.dispatchEvent(new Event('load'));")
    time.sleep(0.01)


# Function to log in to KKTIX
def login(driver, email, password):
    logger.info("Navigating to login page...")
    driver.get(LOGIN_URL)

    try:
        # Wait for the email and password fields to be visible
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".control-group.string.required.user_login input"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".control-group.password.required.user_password input"))
        )

        # Fill in the email and password
        logger.info("Filling in login credentials...")
        email_field.send_keys(email)
        password_field.send_keys(password)

        # Find and click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "commit"))
        )
        login_button.click()

        # Wait for the login to complete (check for a redirect or a logged-in indicator)
        WebDriverWait(driver, 10).until(
            EC.url_changes(LOGIN_URL)
        )
        logger.info("Login successful!")
    except TimeoutException as e:
        logger.error(f"Login failed: Timeout waiting for elements - {e}")
        raise
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise


# Function to handle the event page (look for "Buy Now" or "Next Step" button)
def handle_event_page(driver):
    logger.info(f"Navigating to event page: {EVENT_URL}")
    driver.get(EVENT_URL)

    reload_attempts = 0
    while reload_attempts < MAX_RELOAD_ATTEMPTS:
        try:
            # Simulate human behavior to avoid bot detection
            simulate_human_behavior(driver)

            # Force page load
            force_page_load(driver)
            logger.info("Event page loaded, searching for buttons...")

            # Check for anti-bot measures (e.g., CAPTCHA)
            if "captcha" in driver.current_url.lower() or "verify" in driver.current_url.lower():
                logger.error(
                    "Anti-bot measure detected (CAPTCHA). Please complete the CAPTCHA manually and then re-run the script.")
                return False
            try:
                captcha_iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'captcha')]")
                logger.error(
                    "Anti-bot measure detected (CAPTCHA iframe). Please complete the CAPTCHA manually and then re-run the script.")
                return False
            except NoSuchElementException:
                pass

            # Try to find the "Buy Now" (立即購票) button
            logger.info("Looking for 'Buy Now' (立即購票) button...")
            buy_now_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#order-no21w a"))
            )
            href = buy_now_button.get_attribute("href")
            logger.info(f"Found 'Buy Now' button with href: {href}")
            driver.get(href)
            logger.info("Navigating to registration page...")
            return True

        except TimeoutException:
            logger.info("'Buy Now' button not found, looking for 'Next Step' (下一步) button...")
            try:
                # Strategy 1: Find any <a> tag with /registrations/new in href
                potential_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((
                        By.XPATH,
                        "//a[contains(@href, '/registrations/new')]"
                    ))
                )
                if potential_buttons:
                    logger.info(f"Found {len(potential_buttons)} potential buttons leading to /registrations/new.")
                    for i, button in enumerate(potential_buttons):
                        href = button.get_attribute("href")
                        text = button.text.strip()
                        logger.info(f"Button {i + 1}: href={href}, text={text}")
                    # Filter for buttons with "Next Step" text
                    target_button = None
                    for button in potential_buttons:
                        text = button.text.strip()
                        if "下一步" in text or "Next" in text:
                            target_button = button
                            break
                    if not target_button:
                        logger.info("No 'Next Step' button found in potential buttons, selecting the first one...")
                        target_button = potential_buttons[0]
                    href = target_button.get_attribute("href")
                    logger.info(f"Selected 'Next Step' button with href: {href}")
                    driver.get(href)
                    logger.info("Navigating to registration page...")
                    return True

                # Strategy 2: Use JavaScript to find the button
                logger.info("URL-based search failed, trying JavaScript...")
                target_button = driver.execute_script("""
                    var buttons = document.querySelectorAll("a");
                    for (var i = 0; i < buttons.length; i++) {
                        if ((buttons[i].textContent.includes('下一步') || buttons[i].textContent.includes('Next')) && buttons[i].href.includes('/registrations/new')) {
                            return buttons[i];
                        }
                    }
                    return null;
                """)
                if target_button:
                    href = target_button.get_attribute("href")
                    logger.info(f"Found 'Next Step' button via JavaScript with href: {href}")
                    driver.get(href)
                    logger.info("Navigating to registration page...")
                    return True

                # Strategy 3: Log all <a> tags for debugging
                logger.info("No buttons found, logging all <a> tags for debugging...")
                all_links = driver.find_elements(By.TAG_NAME, "a")
                for i, link in enumerate(all_links):
                    href = link.get_attribute("href") or "No href"
                    text = link.text.strip() or "No text"
                    logger.info(f"Link {i + 1}: href={href}, text={text}")

                # Strategy 4: Hardcode the href as a last resort
                logger.info("All strategies failed, trying hardcoded href as a last resort...")
                hardcoded_href = "https://kktix.com/events/tangsiuhau-imherelive2025-0405/registrations/new"  # For 5 Apr
                logger.info(f"Navigating to hardcoded href: {hardcoded_href}")
                driver.get(hardcoded_href)
                logger.info("Navigating to registration page...")
                return True

            except TimeoutException:
                reload_attempts += 1
                logger.info(
                    f"Neither 'Buy Now' nor 'Next Step' button found, reloading page (Attempt {reload_attempts}/{MAX_RELOAD_ATTEMPTS})...")
                # Log the page source for debugging
                if reload_attempts % 5 == 0:  # Log every 5 attempts to avoid flooding
                    logger.debug(f"Page source for debugging:\n{driver.page_source[:1000]}...")  # Truncate for brevity
                driver.refresh()
                continue

    logger.error(f"Max reload attempts ({MAX_RELOAD_ATTEMPTS}) reached, stopping.")
    return False


# Function to handle the registration page (select ticket type and quantity)
def handle_registration_page(driver):
    logger.info("On registration page, selecting ticket type and quantity...")

    try:
        # Find all ticket units
        ticket_units = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ticket-unit"))
        )
        if not ticket_units:
            logger.error("Ticket units not found on registration page.")
            return False

        # Find the preferred ticket type
        target_ticket_unit = None
        available_ticket_types = []
        for unit in ticket_units:
            ticket_name = unit.find_element(By.CSS_SELECTOR, ".ticket-name").text.strip()
            available_ticket_types.append(ticket_name)
            if PREFERRED_TICKET_TYPE in ticket_name:
                target_ticket_unit = unit
                break

        if not target_ticket_unit:
            logger.error(
                f"Preferred ticket type '{PREFERRED_TICKET_TYPE}' not found. Available ticket types: {available_ticket_types}")
            return False

        logger.info(f"Found preferred ticket type: {PREFERRED_TICKET_TYPE}")

        # Select the quantity
        quantity_select = target_ticket_unit.find_element(By.CSS_SELECTOR, 'select[name="ticket[quantity]"]')
        quantity_select.click()
        quantity_option = quantity_select.find_element(By.XPATH, f"//option[@value='{TICKET_QUANTITY}']")
        quantity_option.click()
        logger.info(f"Selected ticket quantity: {TICKET_QUANTITY}")

        # Find and click the "Next" button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '下一步') or contains(text(), 'Next')]"))
        )
        next_button.click()
        logger.info("Clicked 'Next' button to proceed with ticket purchase.")
        logger.info(
            "Script stopped. Please manually complete any CAPTCHA or additional steps required to finalize the purchase.")
        return True

    except TimeoutException as e:
        logger.error(f"Error on registration page: Timeout waiting for elements - {e}")
        return False
    except NoSuchElementException as e:
        logger.error(f"Error on registration page: Element not found - {e}")
        return False
    except Exception as e:
        logger.error(f"Error on registration page: {e}")
        return False


# Main function to run the ticket buying process
def main():
    email = "wongkelvin962@gmail.com"
    password = "qwer1234"
    driver = None

    try:
        # Initialize the WebDriver
        driver = initialize_driver()

        # Step 1: Log in to KKTIX
        login(driver, email, password)

        # Step 2: Handle the event page (find "Buy Now" or "Next Step" button)
        if not handle_event_page(driver):
            logger.error("Failed to navigate to registration page.")
            return

        # Step 3: Handle the registration page (select ticket type and quantity)
        if not handle_registration_page(driver):
            logger.error("Failed to complete ticket selection on registration page.")
            return

    except Exception as e:
        logger.error(f"Script failed: {e}")
    finally:
        if driver:
            # Keep the browser open for manual intervention (e.g., CAPTCHA, payment)
            logger.info("Browser will remain open for manual intervention. Close it when done.")
            # Uncomment the line below to close the browser automatically
            # driver.quit()


if __name__ == "__main__":
    main()