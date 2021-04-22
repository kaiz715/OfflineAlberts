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


def assignmentLoader(link):
    # assignments = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.CLASS_NAME, "sg-table__tr--link"))
    # )

    # for i in range(len(assignments)):  # works
    #     xpath = '//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[{}]'.format(
    #         i + 1
    #     )
    #     time.sleep(1.25)
    #     assignment = driver.find_element_by_xpath(xpath)
    #     assignment.click()
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

        # print(assignmentTitle)

        # question = input("Do you want to copy this?: (Y/N): ")
        # if question == "Y" or question == "y":
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

                # check if question titles are the same
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
        driver.back()


def pageNavigation():
    try:
        # page = input("Assignment page to begin: (1/2/3...): ")
        # nextAssignmentList = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/div[{page}]'))
        # ).click()
        assignments = {}
        time.sleep(1)
        all_assignments_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "sg-table__tr--link"))
        )

        for assignment_element in all_assignments_elements:
            link = assignment_element.get_attribute("href")
            assignments[
                driver.find_element_by_xpath(f'//tr[@href="{link}"]/td[2]/div').text
            ] = link

        # print(assignments.keys())
        print("Assignments: ")
        for assignment in assignments:
            print(assignment)
        
        # driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.HOME)
        
        to_be_copied = input('Which one do you want to copy? enter "all" if you want to copy all of them: ')
        try: 
            if to_be_copied == 'all':
                for link in assignments.values():
                    assignmentLoader(link)
            else:
                link = assignments[to_be_copied]
                assignmentLoader(link)
        except:
            print("Invalid Assignment Key")
        
    except Exception as exception:
        print(exception)


def masterController():
    continueProgram = "Y"
    while continueProgram == "Y" or continueProgram == "y":
        pageNavigation()
        continueProgram = input(
            "Would you like to continue this program?: (Y/N): "
        )  # any response other than "Y" will end program


if __name__ == "__main__":
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
    # blah
    time.sleep(5)
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_field = password_field.find_element_by_tag_name("input")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    class_wanted = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.ID, config.classID)))
        .click()
    )

    finishedTab = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div/div[1]/button[3]"))
    ).click()


    masterController()

    driver.quit()