from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from PIL import Image
import config
import getpass
import time
import albert
import shutil

email = config.email
password = config.password
# email = input("Enter Email: ")
# password = getpass.getpass("Enter Password: ") 
chrome_options = Options()
chrome_options.add_argument("--window-size=1900,5000")
driver = webdriver.Chrome(config.path, chrome_options=chrome_options)

driver.get("https://www.albert.io/log-in/")

link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "LOG IN WITH GOOGLE"))
)
link = driver.find_element_by_link_text("LOG IN WITH GOOGLE").click()

email_field = driver.find_element_by_id("identifierId")
email_field.send_keys(email)
email_field.send_keys(Keys.RETURN)

password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'password'))
)
password_field = password_field.find_element_by_tag_name('input')
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

calc = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, config.classID))
).click()

finishedTab = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div/div[1]/button[3]"))
).click()

mainTable = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/div"))
).click()

start = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH,"//*[text()='View Questions']"))
).click()
i = 0
nextButton = True
while nextButton:
    try: 
        clickNext = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/button[2]"))
        )
        time.sleep(1)
        element = driver.find_element_by_class_name('practice-view__question-area')
        element.screenshot((f'images/{i}.png'))
        i+=1
        if clickNext.get_property('disabled'):
            nextButton = False
        else:
            clickNext.click()
    finally:
        print(nextButton)
        
albert.analyze()

print("done")

driver.quit()