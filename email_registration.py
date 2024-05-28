from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
import subprocess
from time import sleep

"""
Useful XPATH:
//*[@id="usernameInput"]
//*[@id="Password"]
//*[@id="firstNameInput"]
//*[@id="lastNameInput"]
//*[@id="BirthMonth"]
//*[@id="BirthDay"]
//*[@id="BirthYear"]
//*[@id="nextButton"]
//*[@id="root"]/div/div[1]/button
//*[@id="root"]/div/div[1]/div/div/div[1]/img
//*[@id="root"]/div/div[1]/div/button
/html/body
//*[@id="searchBoxColumnContainerId"]/div[1]/button/span/i/span/i
"""

option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])
option.add_argument('--log-level=3')

class ShortenExpression():
    def __init__ (self, browser, wait):
        self._browser = browser
        self._wait = wait

    def Click(self, xpath: str) -> None: self._browser.find_element(By.XPATH, xpath).click()
    def Wait(self, xpath: str) -> None: self._wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    def Enter_value(self, xpath: str, message: str) -> None: self._browser.find_element(By.XPATH, xpath).send_keys(message)
"""
Usage:
-Improve readability 
-Facilitate future maintenance

Arguements:
-xpath: str = XPATH of target elements
-message: str = value that we want to input into target elements

Return: None
"""



def email_registration(name: str, password: str) -> bool:
    """
    Usage:
    Register an email account on Outlook
    
    Arguments:
    -name: str = username.
    -password: str = password.

    Return:
    bool = True for successfully register a Outlook mail account.
    """
    browser = webdriver.Chrome(options=option)
    wait = WebDriverWait(browser, 300)
    s = ShortenExpression(browser, wait)
    try:
        browser.get('https://signup.live.com/signup?cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&id=292841&contextid=02FF363DA32C4670&opid=9A392BC71E4ABF28&bk=1716831026&sru=https://login.live.com/login.srf%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26contextid%3d02FF363DA32C4670%26opid%3d9A392BC71E4ABF28%26mkt%3dEN-US%26lc%3d1033%26bk%3d1716831027%26uaid%3d01784ba60aa04945896f33714908fa42&uiflavor=web&lic=1&mkt=EN-US&lc=1033&uaid=01784ba60aa04945896f33714908fa42')
        s.Wait('//*[@id="liveSwitch"]')
        s.Click('//*[@id="liveSwitch"]')

        s.Wait('//*[@id="MemberName"]')
        s.Enter_value('//*[@id="MemberName"]', name)
        s.Click('//*[@id="iSignupAction"]')
    
        s.Wait('//*[@id="PasswordInput"]')
        s.Enter_value('//*[@id="PasswordInput"]', password)
        s.Click('//*[@id="iSignupAction"]')
        
        s.Wait('//*[@id="FirstName"]')
        s.Enter_value('//*[@id="FirstName"]', name[:int(len(name)//2+1)])
        s.Enter_value('//*[@id="LastName"]', name[int(len(name)//2):])
        s.Click('//*[@id="iSignupAction"]')
        
        s.Wait('//*[@id="BirthMonth"]')
        Select(browser.find_element(By.XPATH, '//*[@id="BirthMonth"]')).select_by_visible_text('April')
        Select(browser.find_element(By.XPATH, '//*[@id="BirthDay"]')).select_by_visible_text('1')
        s.Enter_value('//*[@id="BirthYear"]', '2000')
        s.Click('//*[@id="iSignupAction"]')

        s.Wait('//*[@id="mectrl_headerPicture"]') #We will be directed to home page after successful registration
        return True
    except Exception as e:
        #print(e)
        return False


if __name__ == '__main__':
    name = str(input('Username: '))         #Enter your own test case
    password = str(input('Password: '))
    print(f'TEST: {email_registration(name, password)}. Registering email {name}@outlook.com.')