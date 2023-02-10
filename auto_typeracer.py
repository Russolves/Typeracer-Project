#First import the necessary modules for the task
import time
import keyboard
import requests
import sys
import pyautogui as pa
from scrapy import Selector
# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# Function that gets the url content and then returns a Selector object
def html():
    url = 'https://play.typeracer.com/'
    html = requests.get(url).content
    sel = Selector(text = html)
    return sel

# Function that extracts the elements from the desired Xpath
def xpath_extractor(sel):
    time.sleep(1)
    selector_list = sel.xpath('//table[@id="themeHeader"]//*').extract()
    print(selector_list)

# Creating a Method that takes in as argument the website you want to navigate to (and whether you want to use incognito)
def navigate(website, incognito = True, fullscreen = True):
    # Program in option so that the web browser does not immediately close after program execution
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    # browser = webdriver.ChromeOptions()
    # String the url together with the argument entered into the method
    url = "https://"+website+"/"
    # If incognito mode is requested
    if incognito == True:
        chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(chrome_options = chrome_options)
    # If fullscreen is desired
    if fullscreen == True:
        driver.maximize_window()
    driver.get(url)
    return driver

#Method for user commands
def user_commands(driver):
    time.sleep(3)
    timer = driver.find_element(By.CSS_SELECTOR, 'span.time')
    #Timer is 0:58 at 8 seconds left before race
    print("Countdown of "+timer.text[-1]+" seconds")
    
    # Typing speed
    speed = 0.02
    #Start the first letter
    letter = driver.find_element(By.CSS_SELECTOR, 'table.inputPanel>tbody>tr>td>table>tbody>tr>td>div>div>span:nth-of-type(1)')
    print("Commencing utter destruction of opponents")
    # Locate the Input bar while making sure that the typing space can be 'clickable' before we start typing
    userinput = WebDriverWait(driver, int(timer.text[-1])+30).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'table.inputPanel>tbody>tr:nth-of-type(2)>td>input'))
    )
    second = driver.find_element(By.CSS_SELECTOR, 'table.inputPanel>tbody>tr>td>table>tbody>tr>td>div>div>span:nth-of-type(2)')
    word = list(second.text)
    if ' ' in second.text:
        phrase = second.text
        userinput.send_keys(letter.text)
        time.sleep(speed)
    else:
        rest = driver.find_element(By.CSS_SELECTOR, 'table.inputPanel>tbody>tr>td>table>tbody>tr>td>div>div>span:nth-of-type(3)')
        phrase = rest.text
        first_word = driver.find_element(By.CSS_SELECTOR, 'table.inputPanel>tbody>tr>td>table>tbody>tr>td>div>div>span:nth-of-type(2)')
        first_word = first_word.text
        userinput.send_keys(letter.text)
        time.sleep(speed)
        # For loop to enter the rest of the words
        for i in range(len(word)):
            userinput.send_keys(word[i])
            time.sleep(speed)
    
    # Processing the rest of the words through turning them into a list and then typing them out
    words = list(phrase)
    if words[0].isalpha() or words[0] == "-" or words[0].isdigit():
        words.insert(0, " ")
    for x in range(len(words)):
        userinput.send_keys(words[x])
        time.sleep(speed)

#Method that asks if the ad window is present and races again
def race_again(driver):
    again = WebDriverWait(driver, 30).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'a.raceAgainLink'))
    )
    again.click()

    try:
        driver.find_element(By.CSS_SELECTOR, 'div.popupContent').is_displayed()
    except NoSuchElementException:
        pass
    else:
        try:
            driver.find_element(By.CSS_SELECTOR, 'div.xButton').is_displayed()
        except NoSuchElementException:
            pass
        else:
            close = driver.find_element(By.CSS_SELECTOR, 'div.xButton')
            print("Closing ad window now")
            close.click()
    
#Method to automate the typing challenge
def challenge(driver):
    button = driver.find_element(By.XPATH, '//button[@class="gwt-Button"]')
    button.click()
    print("Entering the typing challenge")
    time.sleep(2)
    #Grabbing the image url of the typing challenge
    image_url = driver.find_element(By.XPATH, '//img[@class="challengeImg"]').get_attribute('src')

    #Using the Action Chain to select all and then cut and paste
    actions = ActionChains(driver)
    challenge_input = driver.find_element(By.XPATH, '//textarea[@class="challengeTextArea"]')
    challenge_input.send_keys(image_url)
    #Control A then control x
    actions.key_down(Keys.CONTROL)
    actions.send_keys("a")
    actions.key_up(Keys.CONTROL)
    actions.perform()
    actions.key_down(Keys.CONTROL)
    actions.send_keys("x")
    actions.key_up(Keys.CONTROL)
    actions.perform()
    #Saving the window_handle
    original_window = driver.window_handles[0]

    #Opening a new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    #URL of website for automating image to text converter https://www.imagetotext.info/
    driver.get('https://www.imagetotext.info/')
    url_input = driver.find_element(By.XPATH, '//input[@class="file-url"]')
    url_input.click()
    #Paste the URL
    actions.key_down(Keys.CONTROL)
    actions.send_keys("v")
    actions.key_up(Keys.CONTROL)
    actions.perform()

    url_inputsubmit = driver.find_element(By.XPATH, '//div[@id="jsShadowRoot"]')
    url_inputsubmit.click()
    time.sleep(2)
    #Close any pop-up ads
    close_ad = driver.find_element(By.XPATH, '//div[@id="adngin-bottom_adhesive-0-adhesive-close"]')
    close_ad.click()
    time.sleep(7)
    #Copy to clipboard
    response = driver.find_element(By.XPATH, '//div[@class="tool-result"]/div[1]/div[3]/button[1]')
    response.click()
    driver.close()
    driver.switch_to.window(original_window)
    challenge_input = driver.find_element(By.XPATH, '//textarea[@class="challengeTextArea"]')
    challenge_input.click()
    #Paste the text copied on the clipboard
    actions.key_down(Keys.CONTROL)
    actions.send_keys("v")
    actions.key_up(Keys.CONTROL)
    actions.perform()
    button = driver.find_element(By.XPATH, '//button[@class="gwt-Button"]')
    button.click()
    time.sleep(3)
    button = driver.find_element(By.XPATH, '//div[@class="xButton"]')
    button.click()
    

# Writing the mainline function for the program
def main():
    print("Program executing...")
    driver = navigate("play.typeracer.com")
    time.sleep(3)
    # Method that inputs user commands and whatever you want to do at the website
    start = driver.find_element(By.CSS_SELECTOR, 'div#gwt-uid-1>a')
    #print("This is the thing you are looking for \n", start)
    start.click()
    #Number of times the user wants to play the game
    n = 5
    for j in range(n-1):
        user_commands(driver)
        try:
            time.sleep(3)
            driver.find_element(By.XPATH, '//button[@class="gwt-Button"]').is_displayed()
        except NoSuchElementException:
            print("Challenge not found")
        else:
            challenge(driver)
        finally:
            race_again(driver)
    user_commands(driver)


if __name__ == "__main__":
    main()
