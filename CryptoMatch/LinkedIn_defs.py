from selenium.webdriver.common.by import By

# Need level employees
FOUNDERS = ['founder', 'co-founder']
CHIEFS = ['ceo', 'coo', 'cfo', 'cmo', 'cto', 'cio', 'cso', 'chief']
VPS = ['vp', 'vice']

def parse_employee(project, empl):
    try:
        # Получим имя сотрудника
        name_employees = empl.find_element(By.XPATH,
                                           './/a[@class="app-aware-link "]//span[@aria-hidden="true"]'
                                           ).text
        # Получим должность сотрудника
        title_employee = empl.find_element(By.XPATH,
                                           './/div[@class="entity-result__primary-subtitle t-14 t-black '
                                           't-normal"]').text.lower()
    except:
        return None

    # Получим ссылку на профиль сотрудника
    link = empl.find_element(By.XPATH, './/a[@class="app-aware-link "]').get_attribute('href')

    # Проверяем должность сотрудника и добавляем в соответствующие столбцы
    for founder in FOUNDERS:
        if founder in title_employee:
            position = 'Founder'
            break
    else:
        for chief in CHIEFS:
            if chief in title_employee.split() and 'director' not in title_employee:
                position = 'Chief'
                break
        else:
            for vp in VPS:
                if vp in title_employee:
                    position = 'VP'
                    break
            else:
                if 'advisor' in title_employee:
                    position = 'Advisor'
                else:
                    return None

    print(f'{project};{name_employees};{position};{link}')
    return project, name_employees, position, link

