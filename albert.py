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
import re

def starter():
    email = config.email
    password = config.password
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,10000")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://www.albert.io/log-in/")
    time.sleep(1)
    # login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
    ).send_keys(email)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(password, Keys.RETURN)

    return driver


def topic_copy(link):
    driver = starter()
    time.sleep(2)
    driver.get(link)
    time.sleep(3)
    topic_title = driver.find_element_by_name("og:description").get_attribute("content")
    topic_title = re.search('in topic "(.*)"', str(topic_title)).group(1)

    # do this to be writable in a windows directory
    topic_title = (    
        topic_title.replace(":", "")
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
    # makes a directory for the topic
    try:
        os.mkdir(f"images/{topic_title}")
    except Exception as exception:
        print(exception)

    # Loops through all questions in topic and takes screenshot
    next_button = True
    while next_button:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "a-button--tertiary",
                )
            )
        )
        question_title = driver.find_element_by_name("og:description").get_attribute("content")
        question_title = re.search('Practice question "(.*)" ', question_title).group(1)
        
        # do this to be writable in a windows directory
        question_title = (    
        question_title.replace(":", "")
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
        print(question_title)

        # gets explaination of answer
        driver.find_element_by_class_name("mcq-option__letter").click()
        driver.find_element_by_class_name("a-button--secondary").click()  # submit button
        time.sleep(3)

        # screenshots the question/explaination
        explaination = driver.find_element(by=By.CLASS_NAME, value='question-wrapper')
        explaination.screenshot(f"images/{topic_title}/{question_title}.png")

        # checks if theres a next question
        click_next = driver.find_elements_by_class_name("a-button--tertiary")[1]
        
        if click_next.get_property("disabled"):
            next_button = False
        else:
            click_next.click()
            time.sleep(2)
    print("Finished Copying: " + topic_title + "\n")


if __name__ == "__main__":
    email = config.email
    password = config.password
    chrome_options = Options()
    chrome_options.add_argument("--headless")
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
    courses = driver.find_elements_by_class_name("course-card__title")
    course_names = [course.find_element_by_tag_name("a").text for course in courses]

    # select course
    # answer with 1,2,3 ...

    print("\nCourses: " + str(course_names))
    course_selection = (
        int(input("Which course would you like? (1/2/3...): ")) - 1
    )
    courses[course_selection].find_element_by_tag_name("a").click()

    # get a list of topics
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sgi--topic"))
    )
    topics = driver.find_elements_by_class_name("sgi--topic") # each subunit problem set

    topic_links = [topic.get_attribute("href") for topic in topics]

    for topic_link in topic_links:
        topic_copy(topic_link)
        if input("Do you want to continue? (Y/N): ") != "Y" or "y":
            break
