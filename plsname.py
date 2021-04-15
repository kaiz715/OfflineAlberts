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
).click()

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

# mainTable = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/div"))
# ).click()

# mainTable = WebDriverWait(driver, 10).until(              #doesnt fucking work
#     EC.presence_of_element_located((By.CLASS_NAME,"sg-table__tbody"))
# )
# assignments = mainTable.find_elements_by_tag_name("tr")
# for assignment in assignments:
#     time.sleep(2)
#     clickey = assignment.find_element_by_tag_name("td")
#     clickey.click()
#     time.sleep(2)
#     driver.back()

for i in range(1,26):                   #works
    # xpath = '//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[{}]'.format(i)
    # assignment = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, xpath))
    # ).click()

    xpath = '//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[{}]'.format(i)
    time.sleep(1)
    assignment = driver.find_element_by_xpath(xpath)
    assignment.click()
    
    assignmentTitle = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "u-mar-b_1"))
    )
    print(assignmentTitle.text)

    question = input("Do you want to copy this?: (Y/N): ")
    if question == "Y":
        start = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[text()='View Questions']"))
        ).click()
        nextButton = True
        while nextButton:
            try: 
                clickNext = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/button[2]"))
                 )
                time.sleep(2)
                title = driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/div/h1/div/div")
                title = title.text
                title = title.replace(":","").replace("?","").replace("*","").replace("/","").replace("<","").replace(">","").strip()

                element = driver.find_element_by_class_name('practice-view__question-area')
                element.screenshot((f'images/{title}.png'))

                # i+=1
                if clickNext.get_property('disabled'):
                    nextButton = False
                else:
                    clickNext.click()
            finally:
                print(nextButton)
    elif question == "N":
        pass
    else:
        driver.quit()
    time.sleep(2)
    driver.back()

# start = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH,"//*[text()='View Questions']"))
# ).click()

# nextButton = True
# while nextButton:
#     try: 
#         clickNext = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/button[2]"))
#         )
        
#         time.sleep(2)
#         title = driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/div/h1/div/div")
#         title = title.text
#         title = title.replace(":","").replace("?","").replace("*","").replace("/","").replace("<","").replace(">","").strip()


#         element = driver.find_element_by_class_name('practice-view__question-area')
#         element.screenshot((f'images/{title}.png'))

#         # i+=1
#         if clickNext.get_property('disabled'):
#             nextButton = False
#         else:
#             clickNext.click()
#     finally:
#         print(nextButton)
        
# # albert.analyze()

# print("done")

driver.quit()