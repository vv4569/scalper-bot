from time import sleep
from DrissionPage import ChromiumPage, ChromiumOptions


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
    co = ChromiumOptions()
    co.incognito(True)
    browser = ChromiumPage(addr_or_opts=co)

    try:
        browser.get('https://kktix.com/users/sign_up?back_to=https%3A%2F%2Fkktix.com%2F')

        browser.ele('@id:user_login').input(name)
        browser.ele('@id:user_email').input(email)
        browser.ele('@id:user_password').input(password)
        browser.ele('@id:user_password_confirmation').input(password)
        browser.ele('@id:user_birthdate').input('2000-04-01')
        browser.ele('xpath://*[@id="new_user"]/div[3]/div').click()
        browser.ele('xpath://*[@id="new_user"]/div[6]/div/div/button').click()
        browser.ele('xpath://*[@id="new_user"]/div[6]/div/div/div/ul/li[2]/a/span[1]').click()
        browser.ele('xpath://*[@id="user_frequents_regions"]/div/div/button').click()
        browser.ele('xpath://*[@id="user_frequents_regions"]/div/div/div/ul/li[8]/label/input').click()
        browser.ele('xpath://*[@id="user_frequents_regions"]/div/div/button/span[2]/span').click()

        browser.wait(1)

        browser.ele('xpath://*[@id="signup-btn"]').click()
        try :
            print(email, browser.ele('xpath://*[@id="new_user"]/div[1]/div/span').text)
            return False
        except:
            if browser.ele('xpath://*[@id="stickies"]/div').text != "×System is busy. Please retry later!":
                browser.quit()
                return True
        return False
    except Exception as e:
        print(e)
        return False
    

if __name__ == '__main__':
    name = input('name: ')
    email = input('email: ')
    password = input('password: ')
    print(kktix_registration(name, email, password)) 

