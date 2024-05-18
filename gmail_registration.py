from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

browser = webdriver.Chrome()

#https://mail.google.com/mail/u/0/

def gmail_registration(name: str, gmail_address: str, password: str, phone_no: str) -> bool:
    try:
        browser.get('https://mail.google.com/mail/u/0/')

        browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[2]/div/div/div[1]/div/button/span').click()
        browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[2]/div/div/div[2]/div/ul/li[1]').click()

        #Enter name
        browser.find_element(By.XPATH, '//*[@id="firstName"]').send_keys(name)
        browser.find_element(By.XPATH, '//*[@id="collectNameNext"]/div/button').click()
        sleep(5)
        
        #Enter birthday, gender
        Select(browser.find_element(By.ID, 'month')).select_by_visible_text('April')
        browser.find_element(By.XPATH, '//*[@id="day"]').send_keys('1')
        browser.find_element(By.XPATH, '//*[@id="year"]').send_keys('2000')
        Select(browser.find_element(By.ID, 'gender')).select_by_visible_text('Rather not say')
        browser.find_element(By.XPATH, '//*[@id="birthdaygenderNext"]/div/button').click()
        sleep(5)

        #Enter gmail
        browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div/div[1]/div').click()
        browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input').send_keys(name)
        browser.find_element(By.XPATH, '//*[@id="next"]/div/button').click()
        sleep(2)

        #Enter password
        browser.find_element(By.XPATH, '//*[@id="passwd"]/div[1]/div/div[1]/input').send_keys(password)
        browser.find_element(By.XPATH, '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input').send_keys(password)
        browser.find_element(By.XPATH, '//*[@id="createpasswordNext"]/div/button').click()
        sleep(3)

        #Enter phone no., for verification
        browser.find_element(By.XPATH, '//*[@id="phoneNumberId"]').send_keys(phone_no)
        browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[3]/div/div[1]/div/div/button').click()
        sleep(2)

        #Enter verification code
        v_code: str = ''
        while True:
            try:
                v_code = input('Verification code: ')
                break
            except Exception as e:
                print(e, '\e')

        browser.find_element(By.XPATH, '//*[@id="code"]').send_keys(v_code)
        browser.find_element(By.XPATH, '//*[@id="next"]/div/button').click()
        sleep(2)

        #Check
        browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/button').click()
        sleep(2)

        #User agreement 
        browser.find_element(By.XPATH, '//*[@id="next"]/div/button').click()
        sleep(2)

        #End
        browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[1]/div/div/button').click()

        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    name = '4k3ULnBuU1dD'
    gmail = '4k3ULnBuU1dD@gmail.com'
    password = 'R%6lbxlgbxdl'
    phone_no = str(input('Phone number: '))
    print(f'TEST: {gmail_registration(name, gmail, password, phone_no)}')
