import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import numpy as np

#Заводим необходимые списки
ROUNDS = []
DATES = []
AMOUNTS = []
WEBSITES = []
DESCRIPTIONS = []
CATEGORIES = []


options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('user-data-dir=C:\\Users\\tirob\\AppData\\Local\\Google\\Chrome\\User Data')
url = 'https://airtable.com/embed/shrX5Q7HqIo7hrljW/tblaqYnoeg5wjGxqB/viwnUA3uhNurmtgNj?backgroundColor=grayLight'

with webdriver.Chrome(options=options_chrome) as browser:
    browser.get(url)
    time.sleep(15)
#===================================================================================================
    #Выбираем нужные фильтры
    button_filter = browser.find_element(By.CSS_SELECTOR, '[aria-label="Filter rows"]')
    ActionChains(browser).move_to_element(button_filter).click().perform()
    add_condition_button = browser.find_element(By.CSS_SELECTOR, '[aria-label="Add condition"]')
    for _ in range(2):
        ActionChains(browser).move_to_element(add_condition_button).click().perform()
    select_filters = browser.find_elements(By.CSS_SELECTOR, '[data-testid="autocomplete-button"]')
    for i in [0, 2]:
        ActionChains(browser).move_to_element(select_filters[i]).click().send_keys('Date').send_keys(Keys.RETURN).perform()
    time.sleep(2)
    dates_filters = browser.find_elements(By.CLASS_NAME, 'truncate flex-auto left-align')
    ActionChains(browser).move_to_element(select_filters[1]).click().send_keys('after', Keys.RETURN).perform()
    ActionChains(browser).move_to_element(select_filters[3]).click().send_keys('before', Keys.RETURN).perform()
    time.sleep(20)
#===================================================================================================
    #Отображаем нужные столбцы
    fields_button = browser.find_element(By.CSS_SELECTOR, '[aria-label="Hide fields"]')
    ActionChains(browser).move_to_element(fields_button).click().perform()
    time.sleep(1)
    hide_all_btn = browser.find_element(By.XPATH,
                 '//div[@class="my1"]//div[@class="col-6 mx1 focus-visible quiet link-unquiet pointer rounded center darken1 py-half block"]')
    ActionChains(browser).move_to_element(hide_all_btn).click().perform()
    fields_btns = browser.find_elements(By.XPATH, '//div[@class="flex-auto truncate"]')
    for i in [0, 1, 3, 6, 7, 10]:
        ActionChains(browser).move_to_element(fields_btns[i]).click().perform()
    ActionChains(browser).move_to_element(fields_button).click().perform()
    time.sleep(5)
#===================================================================================================
    records = browser.find_element(By.XPATH, '//div[@class="selectionCount summaryCell flex-auto"]')
    records = records.text.split(' ')[0].replace(',', '').strip()
    records = int(records)
    for j in range(1, 7):
        for i in range(records):
            row_col = browser.find_element(By.CSS_SELECTOR, f'[data-columnindex="{j}"][data-rowindex="{i}"]')
#===================================================================================================
            #Парсим даты (date)
            if j == 1:
                ActionChains(browser).move_to_element(row_col).click().perform()
                date = row_col.text
                if not date:
                    DATES.append(np.nan)
                else:
                    DATES.append(date)
#===================================================================================================
            #Парсим сумму (amount)
            elif j == 2:
                ActionChains(browser).move_to_element(row_col).click().perform()
                amount = row_col.text
                if not amount:
                    AMOUNTS.append(np.nan)
                else:
                    AMOUNTS.append(amount)
#===================================================================================================
            #Парсим сайты (website)
            elif j == 3:
                ActionChains(browser).move_to_element(row_col).click().perform()
                website = row_col.text
                if not website:
                    WEBSITES.append(np.nan)
                else:
                    WEBSITES.append(website)
# ===================================================================================================
            # Парсим анонсы (categories)
            elif j == 4:
                ActionChains(browser).move_to_element(row_col).click().perform()
                categories = row_col.text
                if not categories:
                    CATEGORIES.append(np.nan)
                else:
                    CATEGORIES.append(categories)
#===================================================================================================
            #Парсим описания (description)
            elif j == 5:
                ActionChains(browser).move_to_element(row_col).click().perform()
                description = row_col.text
                if not description:
                    DESCRIPTIONS.append(np.nan)
                else:
                    DESCRIPTIONS.append(description)
#===================================================================================================
            #Парсим проекты (project)
            elif j == 6:
                ActionChains(browser).move_to_element(row_col).click().perform()
                project = row_col.text
                if not project:
                    ROUNDS.append(np.nan)
                    print(project)
                else:
                    ROUNDS.append(project)
        row_col.send_keys(Keys.CONTROL + Keys.UP)
#===================================================================================================

#Формируем таблицу для выгрузки, удаляем дубликаты
tb = pd.DataFrame({'company': ROUNDS,
                   'date': DATES,
                   'amount': AMOUNTS,
                   'categories': CATEGORIES,
                   'website': WEBSITES,
                   'description': DESCRIPTIONS
                  })
tb = tb.drop_duplicates(subset='company')

#Выгружаем таблицу
tb.to_csv('Fundraising 2021-2023.csv', index=False, encoding='utf-8-sig')
