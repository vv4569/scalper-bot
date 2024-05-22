from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def Click(xpath: str) -> None: browser.find_element(By.XPATH, xpath).click()
def Wait(xpath: str) -> None: wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
def Enter_value(xpath: str, message: str) -> None: browser.find_element(By.XPATH, xpath).send_keys(message)
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

    try:
        browser.get('https://signup.live.com/signup?cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&id=292841&contextid=5DFEE81AF74CA019&opid=F02668710CDC4605&bk=1716244622&sru=https://login.live.com/login.srf%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26contextid%3d5DFEE81AF74CA019%26opid%3dF02668710CDC4605%26mkt%3dEN-US%26lc%3d1033%26bk%3d1716244622%26uaid%3d950d68cedbbd4eb6a285dfaf78db2f2e&uiflavor=web&lic=1&mkt=EN-US&lc=1033&uaid=950d68cedbbd4eb6a285dfaf78db2f2e')
        Click('//*[@id="liveSwitch"]')

        Wait('//*[@id="MemberName"]')
        Enter_value('//*[@id="MemberName"]', name)
        Click('//*[@id="iSignupAction"]')
    
        Wait('//*[@id="PasswordInput"]')
        Enter_value('//*[@id="PasswordInput"]', password)
        Click('//*[@id="iSignupAction"]')
        
        Wait('//*[@id="FirstName"]')
        Enter_value('//*[@id="FirstName"]', name[:int(len(name)//2+1)])
        Enter_value('//*[@id="LastName"]', name[int(len(name)//2):])
        Click('//*[@id="iSignupAction"]')
        
        Wait('//*[@id="BirthMonth"]')
        Select(browser.find_element(By.XPATH, '//*[@id="BirthMonth"]')).select_by_visible_text('April')
        Select(browser.find_element(By.XPATH, '//*[@id="BirthDay"]')).select_by_visible_text('1')
        Enter_value('//*[@id="BirthYear"]', '2000')
        Click('//*[@id="iSignupAction"]')

        Wait('//body')
        return True
    except Exception as e:
        #print(e)
        return False


if __name__ == '__main__':
    name = str(input('Username: '))         #Enter your own test case
    password = str(input('Password: '))
    print(f'TEST: {email_registration(name, password)}. Registering email {name}@outlook.com.')
