import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from LinkedIn_defs import parse_employee


# Необходимые линкедины для парсинга
df = pd.read_csv('C:\\Users\\tirob\\Downloads\\Parsing Data - Companies.csv')
df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
sites_2022 = df[(df['date'] >= '01.01.22') & (df['date'] < '01.01.23')]['LinkedIn']
sites_2022 = sites_2022[836:]


# Создаем списки под проекты
PROJECTS = []
EMPLOYEES = []
POSITION = []
PERSON_LINKS = []

# Импортируем данные пользователя
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('user-data-dir=C:\\Users\\tirob\\AppData\\Local\\Google\\Chrome\\User Data')

with webdriver.Chrome(options=options_chrome) as browser:
# ===================================================================================================
    # Подключаемся к страничкам компании, вбиваем название компании, и переключаемся на сотрудников
    for url in sites_2022:
        browser.get(url)
        try:
            project = browser.find_element(By.TAG_NAME, 'h1').find_element(By.TAG_NAME, 'span').text
            button_employees = browser.find_element(
                By.CLASS_NAME, 'org-top-card-secondary-content__see-all-independent-link').find_element(
                By.CLASS_NAME, 'ember-view')
        except NoSuchElementException:
            try:
                project = browser.find_element(By.TAG_NAME, 'h1').find_element(By.TAG_NAME, 'span').text
                button_employees = browser.find_element(
                    By.XPATH, '//a[@class="ember-view org-top-card-summary-info-list__info-item"]')
            except:
                continue
        webdriver.ActionChains(browser).move_to_element(button_employees).click().perform()
        time.sleep(5)
# ===================================================================================================
        # Определяем блоки с сотрудниками
        try:
            block_employees = \
                browser.find_elements(By.XPATH, '//ul[@class="reusable-search__entity-result-list list-style-none"]')[1]
        except:
            continue
        employees_div = block_employees.find_elements(By.XPATH, '//div[@class="entity-result"]')

# ===================================================================================================
        # Проходим по страницам с сотрудниками и выписываем инфомарцию об них
        for empl in employees_div:
            employee_info = parse_employee(project, empl)
            if employee_info is not None:
                PROJECTS.append(employee_info[0])
                EMPLOYEES.append(employee_info[1])
                POSITION.append(employee_info[2])
                PERSON_LINKS.append(employee_info[3])

# ===================================================================================================
        # Определяем если страниц с сотрудниками больше одной
        pages_emlpoyees = browser.find_elements(By.CSS_SELECTOR, '[data-test-pagination-page-btn]')
        if len(pages_emlpoyees) > 0:
            pages_emlpoyees = int(pages_emlpoyees[-1].text)
        else:
            pages_emlpoyees = 0

        # Делаем теже самые действия в случае если страниц с сотрудниками больше 1
        if pages_emlpoyees > 0:
            for _ in range(pages_emlpoyees-1):
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                btn_next = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, '[aria-label="Next"]'))).click()
                time.sleep(2)
                try:
                    block_employees = browser.find_element(By.XPATH,
                                                           '//ul[@class="reusable-search__entity-result-list '
                                                           'list-style-none"]')
                except:
                    continue
                employees_div = block_employees.find_elements(By.XPATH, '//div[@class="entity-result"]')

                # Проходим по страницам с сотрудниками и выписываем инфомарцию об них
                for empl in employees_div:
                    employee_info = parse_employee(project, empl)
                    if employee_info is not None:
                        PROJECTS.append(employee_info[0])
                        EMPLOYEES.append(employee_info[1])
                        POSITION.append(employee_info[2])
                        PERSON_LINKS.append(employee_info[3])
# ===================================================================================================
table = pd.DataFrame({'project': PROJECTS,
                      'employee': EMPLOYEES,
                      'position': POSITION,
                      'link': PERSON_LINKS})

table = table.drop_duplicates(subset='employee')

table.to_csv('c-level.csv', index=False, encoding='utf-8-sig', header=False)
