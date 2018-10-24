import bs4
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pickle


browser = webdriver.Chrome()
browser.wait = WebDriverWait(browser, 5)
browser.get("https://twitter.com/login")


username_field = browser.find_element_by_class_name("js-username-field")
password_field = browser.find_element_by_class_name("js-password-field")

username_field.send_keys("ABC@gmail.com")
browser.implicitly_wait(1)

password_field.send_keys("ABC123")
browser.implicitly_wait(1)
browser.find_element_by_class_name("EdgeButtom--medium").click()


box = browser.wait.until(EC.presence_of_element_located((By.NAME, "q")))
browser.find_element_by_name("q").clear()
TOPIC = "NBA"
box.send_keys(TOPIC)
box.submit()
wait = WebDriverWait(browser, 10)

try:
    # wait until the first search result is found. Search results will be tweets, which are html list items and have the class='data-item-id':
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

    # scroll down to the last tweet until there are no more tweets:
    i = 0

    context = browser.find_element_by_tag_name("body")
    no_of_pageDowns = 2000
    while no_of_pageDowns:
        context.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.6)
        no_of_pageDowns -= 1
        tweets = browser.find_elements_by_css_selector("li[data-item-id]")



    page_source = browser.page_source
    soup = bs4.BeautifulSoup(page_source,"lxml")
    MYTWEETS=[]
    for li in soup.find_all("li", class_='js-stream-item'):

        # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
        if 'data-item-id' not in li.attrs:
            continue

        else:
            TWEET = {

                'text': None,
                'type': TOPIC
            }
            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                TWEET['text'] = text_p.get_text()

            MYTWEETS.append(TWEET)
except:
    pass


print(len(MYTWEETS))

for i in MYTWEETS:
    print(i)