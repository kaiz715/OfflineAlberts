from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from multiprocessing.dummy import Pool as ThreadPool
from PIL import Image
from tools import divide_chunks
import config
import time
import albert
import os
import os.path

def starter():
    try:
        email = config.email
        password = config.password
        chrome_options = Options()
        chrome_options.add_argument("--window-size=5000,5000")
        driver = webdriver.Chrome(config.path, chrome_options=chrome_options)

        driver.get("https://www.albert.io/log-in/")

        link = (
            WebDriverWait(driver, 10)
            .until(EC.presence_of_element_located((By.LINK_TEXT, "LOG IN WITH GOOGLE")))
            .click()
        )

        email_field = driver.find_element_by_id("identifierId")
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)

        time.sleep(5)
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field = password_field.find_element_by_tag_name("input")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        class_wanted = (
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, config.classID))
            )
        )
    except:
        driver.quit()
    return driver

def assignmentLoader(links):
    driver = starter()
    for link in links:
        driver.get('https://albert.io' + link)
        assignmentTitle = (
            WebDriverWait(driver, 10)
            .until(EC.presence_of_element_located((By.CLASS_NAME, "u-mar-b_1")))
            .text
        )
        assignmentTitle = (
            assignmentTitle.replace(":", "")
            .replace("/", " ")
            .replace("?", "")
            .replace("*", "")
            .replace("/", "")
            .replace("<", "")
            .replace(">", "")
            .replace("\n", "")
            .replace("\\", "")
            .strip()
        )

        try:
            os.mkdir(f"images/{assignmentTitle}")
        except Exception as exception:
            print(exception)

        start = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[text()='View Questions']")
                )
            )
            .click()
        )

        # Loops through all questions in assignment and takes screenshot
        nextButton = True
        k = 2
        while nextButton:
            try:
                clickNext = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//*[@id='app']/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/button[2]",
                        )
                    )
                )
                time.sleep(1)
                title = driver.find_element_by_xpath(
                    "//*[@id='app']/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/div/h1/div/div"
                )
                title = title.text
                title = (
                    title.replace(":", "")
                    .replace("/", " ")
                    .replace("?", "")
                    .replace("*", "")
                    .replace("/", "")
                    .replace("<", "")
                    .replace(">", "")
                    .replace("\n", "")
                    .replace("\\", "")
                    .strip()
                )

                # Checks for same question titles to prevent overwritting files
                if os.path.isfile(f"images/{assignmentTitle}/{title}.png"):
                    title = title + str(k)
                    k += 1

                # Screenshot code portion
                driver.save_screenshot(f"images/{assignmentTitle}/{title}.png")

                start_element = driver.find_element_by_class_name(
                    "question-wrapper__heading"
                )
                start_location = start_element.location
                start_x = start_location["x"]
                start_y = start_location["y"]

                end_element = driver.find_element_by_class_name("m-banner")
                end_size = end_element.size
                end_location = end_element.location
                end_x = end_location["x"] + end_size["width"]
                end_y = end_location["y"]

                img = Image.open(f"images/{assignmentTitle}/{title}.png")
                img = img.crop((start_x, start_y, end_x, end_y))
                img.save(f"images/{assignmentTitle}/{title}.png")

                if clickNext.get_property("disabled"):
                    nextButton = False
                else:
                    clickNext.click()

            finally:
                continue
        print("Finished Copying: " + assignmentTitle + "\n")
    driver.quit()


def pageNavigation():
    try:
        try:    #checks if there is more than 1 assignment page, if so: asks which page to start on.
            page_button_locator = WebDriverWait(driver, 2).until(       # Makes sure presense of more than 1 page as to not prompt if only 1 page
                EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]'))
            )
            try:    #assuming there is more than 1, asks which page to go to
                page = input("Assignment page to begin: (1/2/3...): ")
                page_button_locator = driver.find_element_by_xpath((f'//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/div[{page}]'))
                page_button_locator.click()
                driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.HOME) #scrolls to the top because selenium had issues clicking if the element wasn't on page
            except:
                print("Invalid Page Number. Continuing with page 1")
        except:
            pass

        # Loads all assignments and add to a library
        assignments = {}
        time.sleep(1)
        all_assignments_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "sg-table__tr--link"))
        )

        for assignment_element in all_assignments_elements: # Christian note: 'Assignment Name' is key; 'Link' is value 
            link = assignment_element.get_attribute("href")
            assignments[
                driver.find_element_by_xpath(f'//tr[@href="{link}"]/td[2]/div').text
            ] = link

        print("Assignments: ")
        for assignment in assignments.keys():
            print(assignment)
        driver.get('https://albert.io' + list(assignments.values())[0])

        global cookies
        cookies = driver.get_cookies()

        # Assignment selection
        to_be_copied = input('Which one do you want to copy? enter "all" if you want to copy all of them: ')
        num_threads = int(input('How many threads you you want to run? '))
        links = list(assignments.values())
        split_links = list(divide_chunks(links, num_threads))
        if to_be_copied.casefold() == 'all':
            pool = ThreadPool(num_threads)
            pool.map(assignmentLoader, split_links)
        else:
            assignmentLoader(assignments[to_be_copied])
        
    except Exception as exception:
        print(exception) # <-- have we ever needed this? 


def masterController():
    continueProgram = "Y"
    while continueProgram == "Y" or continueProgram == "y":
        pageNavigation()
        continueProgram = input(
            "Would you like to continue this program?: (Y/N): "
        )  # any response other than "Y" will end program


if __name__ == "__main__":
    check_login = False
    while not check_login:  #this block opens the webdriver and if anything goes wrong, closes it and tries again
        try:
            email = config.email
            password = config.password
            chrome_options = Options()
            chrome_options.add_argument("--window-size=5000,5000")
            driver = webdriver.Chrome(config.path, chrome_options=chrome_options)

            driver.get("https://www.albert.io/log-in/")

            link = (
                WebDriverWait(driver, 10)
                .until(EC.presence_of_element_located((By.LINK_TEXT, "LOG IN WITH GOOGLE")))
                .click()
            )

            email_field = driver.find_element_by_id("identifierId")
            email_field.send_keys(email)
            email_field.send_keys(Keys.RETURN)

            time.sleep(5)
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field = password_field.find_element_by_tag_name("input")
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)

            class_wanted = (
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, config.classID))
                ).click()
            )
            check_login = True
        except:
            driver.quit()

    finished_assignments_tab = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div/div[1]/button[3]"))
    ).click()
    
    cookies = {}

    masterController()

    driver.quit()