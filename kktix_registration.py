from selenium import webdriver
from email_registration import ShortenExpression
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep



"""
//*[@id="user_login"]
//*[@id="user_email"]
//*[@id="user_password"]
//*[@id="user_password_confirmation"]
//*[@id="user_birthdate"] 2000-04-01
//*[@id="new_user"]/div[6]/div/div/button
//*[@id="new_user"]/div[6]/div/div/div/ul/li[2]/a/span[1]
//*[@id="user_frequents_regions"]/div/div/button
//*[@id="user_frequents_regions"]/div/div/div/ul/li[8]/label/input
//*[@id="challenge-stage"]/div/label/input
//*[@id="signup-btn"]
"""

option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])
option.add_argument('--log-level=3')

def kktix_registration(name: str, email: str, password: str) -> bool:
    """
    Usage:
    -Register an account on kktix
    
    Arguements:
    -name: str -> username
    -email: str -> Outlook email address
    -password: str -> password
    
    Return:
    -bool -> represent whether kktix 
    """
    browser = webdriver.Chrome(options=option)
    screen_width = browser.execute_script("return screen.width;")
    screen_height = browser.execute_script("return screen.height;")

    browser.set_window_size(screen_width//2, screen_height)
    browser.set_window_position(screen_width//2, 0)

    wait = WebDriverWait(browser, 300)
    s = ShortenExpression(browser, wait)
    try:
        browser.get('https://kktix.com/users/sign_up?back_to=https%3A%2F%2Fkktix.com%2F')

        s.Enter_value(xpath='//*[@id="user_login"]', message=name)
        s.Enter_value(xpath='//*[@id="user_email"]', message=email)
        s.Enter_value(xpath='//*[@id="user_password"]', message=password)
        s.Enter_value(xpath='//*[@id="user_password_confirmation"]', message=password)
        s.Enter_value(xpath='//*[@id="user_birthdate"]', message='2000-04-01')
        s.Enter_value(xpath='//*[@id="user_birthdate"]', message=Keys.TAB)
        s.Click(xpath='//*[@id="new_user"]/div[6]/div/div/button')
        s.Wait(xpath='//*[@id="new_user"]/div[6]/div/div/div/ul/li[2]/a/span[1]')
        s.Click(xpath='//*[@id="new_user"]/div[6]/div/div/div/ul/li[2]/a/span[1]')
        s.Click(xpath='//*[@id="user_frequents_regions"]/div/div/button')
        s.Wait(xpath='//*[@id="user_frequents_regions"]/div/div/div/ul/li[8]/label/input')
        s.Click(xpath='//*[@id="user_frequents_regions"]/div/div/div/ul/li[8]/label/input')
        sleep(30)
        #s.Click(xpath='//*[@id="challenge-stage"]/div/label/input')
        #s.Click(xpath='//*[@id="signup-btn"]')
        #Need to determine whether given informetion are able to register
        return False
    except Exception as e:
        print(e)
        return False
    

if __name__ == '__main__':
    name = 'h5xqQ6LJYDAk'
    email = 'h5xqQ6LJYDAk@outlook.com'
    password = 'E`4ysrkktifh'
    print(kktix_registration(name, email, password)) 

