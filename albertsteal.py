from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from PIL import Image
import config
import time
import albert
import os
import os.path

email = config.email
password = config.password
chrome_options = Options()
chrome_options.add_argument("--window-size=5000,5000")
driver = webdriver.Chrome(config.path, chrome_options=chrome_options)

driver.get("https://www.albert.io/log-in/")

link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "LOG IN WITH GOOGLE"))
).click()

email_field = driver.find_element_by_id("identifierId")
email_field.send_keys(email)
email_field.send_keys(Keys.RETURN)
#blah
time.sleep(5)
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

assignments = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "sg-table__tr--link"))
)

#make folders: data/classname/assignments

for i in range(len(assignments)):                   #works
    xpath = '//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[{}]'.format(i+1)
    time.sleep(1.25)
    assignment = driver.find_element_by_xpath(xpath) 
    assignment.click()
    
    assignmentTitle = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "u-mar-b_1"))
    ).text
    assignmentTitle = assignmentTitle.replace(":","").replace('/',' ').replace("?","").replace("*","").replace("/","").replace("<","").replace(">","").replace('\n' ,"").replace('\\', '').strip()
    
    print(assignmentTitle)

    question = input("Do you want to copy this?: (Y/N): ")
    if question == "Y" or question == "y":
        try:
            os.mkdir(f'images/{assignmentTitle}')
        except Exception as exception:
            print(exception)
               
        start = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[text()='View Questions']"))
        ).click()
        
        titleList = []
        nextButton = True
        while nextButton:
            try: 
                clickNext = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/button[2]"))
                )
                time.sleep(1)
                title = driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/div/h1/div/div")
                title = title.text
                title = title.replace(":","").replace('/',' ').replace("?","").replace("*","").replace("/","").replace("<","").replace(">","").replace('\n' ,"").replace('\\', '').strip()

                titleList.append(title)
                for titles in titleList:
                    if titleList.count(title) > 1:
                        titleList[len(titleList) - 1] = title + str(i)
                        title = title + str(i)

                # if os.path.isfile(f'//images/{assignmentTitle}/{title}.png'):
                #     title = title + str(i)
                #     i += 1

                driver.save_screenshot(f'images/{assignmentTitle}/{title}.png')

                start_element = driver.find_element_by_class_name('question-wrapper__heading')
                start_location = start_element.location
                start_x = start_location['x']
                start_y = start_location['y']
                
                end_element = driver.find_element_by_class_name('m-banner')
                end_size = end_element.size
                end_location = end_element.location
                end_x = end_location['x'] + end_size['width']
                end_y = end_location['y']

                #check if question titles are the same
                img = Image.open(f'images/{assignmentTitle}/{title}.png')
                img = img.crop((start_x, start_y, end_x, end_y))
                img.save(f'images/{assignmentTitle}/{title}.png')


                if clickNext.get_property('disabled'):
                    nextButton = False
                else:
                    clickNext.click()

            finally:
                print(nextButton)
    elif question == "N" or question == "n":
        pass
    else:
        break
    driver.back()

driver.quit()
