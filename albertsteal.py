from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import config
import time
import os
import os.path
import csv

getAllAssignments = False

# Opens up Albert.IO
def starter():
    email = config.email
    password = config.password
    chrome_options = Options()
    chrome_options.add_argument("--headless")   #Necessary for screenshots to work
    chrome_options.add_argument("--window-size=1920,10000")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.albert.io/log-in/")
    time.sleep(0.5)
    # login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
    ).send_keys(email)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(password, Keys.RETURN)

    return driver


# Get screenshots and answer IDs
def assignment_scraper(link):
    driver = starter()  # Takes driver from starter and uses that
    driver.get(link)

    # assignment_title = driver.find_element_by_name("og:description").get_attribute(
    #     "content"
    # )
    # assignment_title = re.search(
    #     'in topic "(.*)"', str(assignment_title)).group(1)    
    assignment_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div[1]/div/div[1]/h1'))
    ).text

    assignment_title = (    # goes pew pew to bad bad chars
        assignment_title.replace(":", "")
        .replace("/", " ")
        .replace("?", "")
        .replace("*", "")
        .replace("/", "")
        .replace("<", "")
        .replace(">", "")
        .replace("_", "")
        .replace("|", " ")
        .replace("\n", "")
        .replace("\\", "")
        .strip()
    )

    # View questions button
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
    )[1].click()



    # # makes a directory for the assignment
    try:
        os.mkdir(f"images/{assignment_title}")
    except Exception as exception:
        print(exception)

    # Loops through questions
    next_button = True
    answer_ID_group = []  # Each list contains 5 pieces of data [QuestionTitle, [AnswerA, right/wrong]x4]
    while next_button:
        try:
            question_title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[2]/div/div[2]/div/form/div[1]/div/div/h1/div/div'))
            ).text

            # makes title a valid directory name for windows
            question_title = (
                question_title.replace(":", "")
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
            print(question_title)

            # Screenshots
            time.sleep(2)
            el = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[1]/div/div[3]/div[2]/div/div[2]/div')
            el.screenshot(f"images/{assignment_title}/{question_title}.png")

            # getting answer id
            answers = WebDriverWait(driver, 10).until(     # is stored as a 'list'
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "mcq-option-accessible-wrapper"))
            )
            answer_ID_mini_group = [question_title]
            for answer in answers:
                answer_IDs = []
                answer_IDs.append(answer.find_element(by=By.CLASS_NAME, value="mcq-option__hidden-input").get_attribute("id"))
                try:
                    answer.find_element(by=By.CLASS_NAME, value="correctness-indicator-wrapper__indicator--correct")
                    answer_IDs.append(1)    # if correct answer
                except:
                    answer_IDs.append(0)    # if wrong answer
                answer_ID_mini_group.append(answer_IDs)
            answer_ID_group.append(answer_ID_mini_group)

        except Exception as e:
            print(e)

        click_next = driver.find_element(by=By.XPATH, value='//button[text()="Next"]')
        if click_next.get_property("disabled"):
            next_button = False
        else:
            click_next.click()

    try:
        print("\n--------------------------------------------")
        print("Finished Copying: " + assignment_title)
        print("--------------------------------------------\n")

        # for i in range(len(answer_ID_group)):
        #     print(answer_ID_group[i])
        
        csvFileName = str(f"images/{assignment_title}/{assignment_title}.csv")
        file = open(csvFileName, 'w+', newline ='')
        with file:    
            write = csv.writer(file)
            write.writerows(answer_ID_group)
    except:
        print("dont care")
    driver.close()


# Page navigation
def pageNavigation(driver, i = -1):
    try:
        pageNavigationSelector = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "paginationv2__number"))
        )
        
        if(getAllAssignments == False):
            pageInput = int(input("Which page would you like to go to? (1/2/...): ")) - 1
        else:
            pageInput = i
        pageNavigationSelector[pageInput].click()
    except:
        pass


# Get assignment links
def getAssignmentLinks(driver):
    assignments = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
    )
    assignment_links = []
    for assignment in assignments:
        assignment_links.append(assignment.get_attribute("href"))

    return assignments, assignment_links


if __name__ == "__main__":
    email = config.email
    password = config.password
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://www.albert.io/log-in/")
    time.sleep(2)

    # login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
    ).send_keys(email)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(password, Keys.RETURN)

    # list courses
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "course-card__title"))
    )
    time.sleep(1)
    courses = driver.find_elements(by=By.CLASS_NAME, value="classrooms_viewer__list__item") # of type list
    course_names = []
    for course in courses:
        course_names.append(course.find_element(by=By.CLASS_NAME, value="class-card__inner").text)

    # select course
    # answer with 1,2,3 ...
    print("\nCourses: " + str(course_names))
    try:
        course_selection = (
            int(input("Which course would you like? (1/2/3...): ")) - 1 
        )
        courses[course_selection].find_element(by=By.CLASS_NAME, value="class-card__inner").click()
    except Exception as e:
        print("NOT TODAY MOTHERFUCKERS")

    # go to tab with closed assignments
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sg-tabs-wrapper"))
    )
    driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[1]/button[3]').click()  # I gave up with 'class'

    if getAllAssignments == True:
        i = 0
        pageNavigation(driver, i)

        while True:
            try:
                # Get assignment links
                assignments, assignment_links = getAssignmentLinks(driver)
                
                for i in range(len(assignments)):
                    assignmentLink = "https://www.albert.io" + assignment_links[i+1]
                    assignment_scraper(assignmentLink)    
        
                i = i+1
                pageNavigation(driver, i)
            except:
                driver.quit()
                quit()

    else: 
        # Select page
        pageNavigation(driver)

        # Get a list of assignments 
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]'))   
            )
        except:
            print("No Closed Assignments")
            driver.quit()
            quit()

        # Prints a list of all assignments [MAJOR OPTIMIZATION IS POSSIBLE]
        try: 
            assignmentList = []
            rando_fuck_int = 1
            while rando_fuck_int < 100:
                assignment = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[{}]/td[2]'.format(rando_fuck_int))
                assignmentList.append(assignment.text)
                print(f'{rando_fuck_int} | {assignment.text}')
                rando_fuck_int += 1
        except Exception as e:
            pass

        # Get assignment links
        assignments, assignment_links = getAssignmentLinks(driver)

        # Accessing assignments loop
        condition = True
        while condition:
            try:
                assignmentNumber = int(input("Which assignment do you need the IDs to? "))
                assignmentLink = "https://www.albert.io" + assignment_links[assignmentNumber]
                assignment_scraper(assignmentLink)
                continueThing = input("Would you like to continue? (Y/N): ")
                if(continueThing == "Y" or continueThing == "y"):
                    pass
                else:
                    condition = False
            except Exception as e: 
                print(e)
        driver.quit()