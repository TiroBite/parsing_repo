import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

USER_NAMES = []
TWITTER_LINKS = []
TWITTER_SCORES = []
FOLLOWERS = []
DESCRIPTIONS = []

# options_chrome = webdriver.ChromeOptions()
# options_chrome.add_argument('user-data-dir=C:\\Users\\tirob\\AppData\\Local\\Google\\Chrome\\User Data')


with webdriver.Chrome() as browser:
    browser.get('https://twitterscore.io/topScored/?i=6154')
    twitters = [x.text.replace('@', '') for x in browser.find_elements(By.CSS_SELECTOR, 'h6[class="user-twitter-name"]')]

    for name in twitters[99:]:
        browser.get(f'https://twitterscore.io/twitter/{name}/topFollowers?i=6154')
        infl_btn = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((
            By.ID, 'nav-category-Influencers-tab'))).click()

        #wait div pages
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((
            By.ID, 'InfluencersAllAccountFriendsDetailTable_wrapper')))
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #wait pages buttons
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((
                By.XPATH, '//div[@id="InfluencersAllAccountFriendsDetailTable_paginate"]/span/a')))
        pages = browser.find_elements(By.XPATH, '//div[@id="InfluencersAllAccountFriendsDetailTable_paginate"]/span/a')[-1]
        pages = int(pages.text)
        for _ in range(pages):
            time.sleep(2)
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            influencers_table = browser.find_element(
                By.CSS_SELECTOR, '[aria-describedby="InfluencersAllAccountFriendsDetailTable_info"]')

            # influencers_block = influencers_table.find_elements(By.XPATH, './tbody/tr')
            for influencer in influencers_table.find_elements(By.XPATH, './tbody/tr'):
                name = influencer.find_elements(By.XPATH, './/div[@class="table-name-wrapper p-2"]/h6')[0].text
                USER_NAMES.append(name)

                twitter = influencer.find_element(By.XPATH, './/h6[@class="user-twitter-name"]/a').get_attribute('href')
                TWITTER_LINKS.append(twitter)

                score = influencer.find_element(By.XPATH, './/span[@class="score-color"]').text.replace(' ', '')
                TWITTER_SCORES.append(int(score))

                followers = influencer.find_element(By.CLASS_NAME, 'd-flex-r').text.split('\n')[0]
                FOLLOWERS.append(int(followers))
                try:
                    description = influencer.find_element(By.CLASS_NAME, 'description-text').text.replace('\n', '. ')
                    DESCRIPTIONS.append(description)
                except:
                    DESCRIPTIONS.append(None)

                print(f'{name};{description};{twitter};{score};{followers}')

            next_btn = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((
                By.ID, 'InfluencersAllAccountFriendsDetailTable_next')))
            next_btn.click()


df = pd.DataFrame({
    'name': USER_NAMES,
    'descriptions': DESCRIPTIONS,
    'twitter': TWITTER_LINKS,
    'twitter_score': TWITTER_SCORES,
    'followers': FOLLOWERS,
})

df.dropna(subset='twitter', inplace=True)

df.to_csv('Influencers parsing.csv', index=False, header=False)
