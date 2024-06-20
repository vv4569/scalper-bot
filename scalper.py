from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time 
import db

# Function to log in using the credentials
def login(email, password):
    # Use the local path of chromedriver for testing in local workspace
    service = Service(executable_path="C:\\Users\\kwchu\\Desktop\\IT\\Coding\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("https://kktix.com/users/sign_in?back_to=https%3A%2F%2Fkktix.com%2F")

        # Find the email and password fields and fill them in using the class names
        email_div = driver.find_element(By.CLASS_NAME, 'control-group.string.required.user_login')
        password_div = driver.find_element(By.CLASS_NAME, 'control-group.password.required.user_password')

        # The actual input fields are likely inside these divs, so find them
        email_field = email_div.find_element(By.TAG_NAME, 'input')
        password_field = password_div.find_element(By.TAG_NAME, 'input')

        email_field.send_keys(email)
        password_field.send_keys(password)

        # Find the login button and click it
        login_button = driver.find_element(By.NAME, 'commit')
        login_button.click()

        # Optionally, wait for some time to observe the result
        time.sleep(5)
    finally:
        driver.quit()

if __name__ == '__main__':
    users = db.get_gmail()
    for user in users:
        print(f"Logging in with: {user.gmail} / {user.password}")
        login(user.gmail, user.password)
