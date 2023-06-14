import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import numpy as np

USER_NAMES = []
TWITTER_LINKS = []
TWITTER_SCORES = []
FOLLOWERS = []
FOUNDERS_OF = []
DESCRIPTIONS = []

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('user-data-dir=C:\\Users\\tirob\\AppData\\Local\\Google\\Chrome\\User Data')
url = 'https://twitterscore.io/twitter/cointelegraph/topFollowers/?i=6154'


with webdriver.Chrome(options=options_chrome) as browser:
    browser.get(url)
    founders_btn = browser.find_element(By.ID, 'nav-category-Founders-tab')
    ActionChains(browser).move_to_element(founders_btn).click().perform()
    time.sleep(10)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    pages = browser.find_elements(By.XPATH, '//div[@id="FoundersAllAccountFriendsDetailTable_paginate"]/span/a')[
        -1].text
    pages = int(pages) // 10
    for _ in range(pages):
        time.sleep(10)
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        next_btn = browser.find_element(By.ID, 'FoundersAllAccountFriendsDetailTable_next')

        founders_table = browser.find_element(By.CSS_SELECTOR,
                                              '[aria-describedby="FoundersAllAccountFriendsDetailTable_info"]')
        founders_block = founders_table.find_elements(By.XPATH, './tbody/tr')
        for founder in founders_block:

            name = founder.find_elements(By.XPATH, './/div[@class="table-name-wrapper p-2"]/h6')[0].text
            USER_NAMES.append(name)

            twitter = founder.find_element(By.XPATH, './/h6[@class="user-twitter-name"]/a').get_attribute('href')
            TWITTER_LINKS.append(twitter)

            score = founder.find_element(By.XPATH, './/span[@class="score-color"]').text.replace(' ', '')
            TWITTER_SCORES.append(int(score))

            followers = founder.find_element(By.CLASS_NAME, 'd-flex-r').text.split('\n')[0]
            FOLLOWERS.append(int(followers))

            try:
                description = founder.find_element(By.CLASS_NAME, 'description-text').text
                DESCRIPTIONS.append(description)
            except:
                DESCRIPTIONS.append(None)

            try:
                founders_of = [x.get_attribute('title') for x in
                               founder.find_elements(By.XPATH, './/td')[-1].find_elements(By.TAG_NAME, 'a')]
                FOUNDERS_OF.append(founders_of)
            except:
                FOUNDERS_OF.append([None])

            print(name, "-", description, '-',
                  twitter, 'Score:', score, 'Followers:',
                  followers, 'Founders of:', founders_of)
        ActionChains(browser).move_to_element(next_btn).click().perform()
        time.sleep(3)

df = pd.DataFrame({
    'name': USER_NAMES,
    'descriptions': DESCRIPTIONS,
    'twitter': TWITTER_LINKS,
    'twitter_score': TWITTER_SCORES,
    'followers': FOLLOWERS,
    'founders_of': FOUNDERS_OF
})

df.dropna(subset='name', inplace=True)

df.to_csv('twitter parsing.csv', index=False)