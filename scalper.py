from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 

service = Service(executable_path="C:\\Users\\kwchu\\Desktop\\IT\\Coding\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://google.com")

input = driver.find_element(By.CLASS_NAME, "gLFyf")
input.send_keys("selenium tutorial" + Keys.ENTER)

driver.quit()