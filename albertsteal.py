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
    time.sleep(0.5)
    # login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
    ).send_keys(email)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(password, Keys.RETURN)

    return driver


def assignment_scraper(link):
    driver = starter()
    driver.get(link)
    time.sleep(2)
    assignment_title = driver.find_element_by_name("og:description").get_attribute(
        "content"
    )
    assignment_title = re.search('in topic "(.*)"', str(assignment_title)).group(1)
    assignment_title = (
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

    # makes a directory for the assignment
    try:
        os.mkdir(f"images/{assignment_title}")
    except Exception as exception:
        print(exception)
    # Loops through all questions in assignment and takes screenshot
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
        quesiton_title = driver.find_element_by_name("og:description").get_attribute(
            "content"
        )
        quesiton_title = re.search('Practice question "(.*)" ', quesiton_title).group(1)

        # makes title a valid directory name for windows
        quesiton_title = (
            quesiton_title.replace(":", "")
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
        print(quesiton_title)
        # Checks for same question titles to prevent overwritting files
        num = ""
        if os.path.isfile(f"images/{assignment_title}/{quesiton_title}.png"):
            num = 1
        while os.path.isfile(
            f"images/{assignment_title}/{quesiton_title + str(num)}.png"
        ):
            num += 1

            # enters in a junk answer
        driver.find_element_by_class_name("mcq-option__letter").click()
        driver.find_element_by_class_name(
            "a-button--secondary"
        ).click()  # submit button
        time.sleep(0.5)

        # Screenshot code portion
        driver.save_screenshot(
            f"images/{assignment_title}/{quesiton_title + str(num)}.png"
        )

        start_element = driver.find_element_by_class_name("question-wrapper__heading")
        start_location = start_element.location
        start_x = start_location["x"]
        start_y = start_location["y"]

        end_element = driver.find_element_by_class_name("m-banner__content")
        end_size = end_element.size
        end_location = end_element.location
        end_x = end_location["x"] + end_size["width"]
        end_y = end_location["y"]

        img = Image.open(f"images/{assignment_title}/{quesiton_title}.png")
        img = img.crop((start_x, start_y, end_x, end_y))
        img.save(f"images/{assignment_title}/{quesiton_title}.png")

        # checks if theres a next question
        click_next = driver.find_elements_by_class_name("a-button--tertiary")[1]
        if click_next.get_property("disabled"):
            next_button = False
        else:
            click_next.click()
            time.sleep(2)
    print("Finished Copying: " + assignment_title + "\n")


if __name__ == "__main__":
    email = config.email
    password = config.password
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://www.albert.io/log-in/")

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
    course_names = []
    for course in courses:
        course_names.append(course.find_element_by_tag_name("a").text)
    # select course
    # answer with 1,2,3 ...
    course_selection = (
        int(input("which course would you like?:        " + str(course_names))) - 1
    )
    courses[course_selection].find_element_by_tag_name("a").click()

    # get a list of assignments
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sgi__content--topic"))
    )
    assignments = driver.find_elements_by_class_name("sgi__content--topic")

    assignment_links = []
    for assignment in assignments:
        assignment_links.append(
            assignment.find_element_by_class_name(
                "study-guide-heading-wrapper"
            ).get_attribute("href")
        )

    for i in range(len(assignment_links)):
        assignment_scraper(assignment_links[i])
        if input("Do you want to continue? (Y/N)  ") == "N":
            break
