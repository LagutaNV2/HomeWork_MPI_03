'''
    все объявления: main class = vacancy-serp-content
    одно объявление: div class = vacancy-serp-item-body
    1) a -> href:  tag_name  h3 -> tag_name a
    2) text -> зарплата:
    span class = bloko-header-section-2 data-qa = vacancy-serp__vacancy-compensation
    3) text -> компания: div class = vacancy_serp_item__meta-info_company
    4) text -> город: div class = bloko-text data-qa = vacancy-serp__vacancy-address
'''

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint


def wait_element(browser, delay_second=1, by=By.CLASS_NAME, value=None):

    return WebDriverWait(browser, delay_second).until(
        expected_conditions.presence_of_element_located((by, value))
    )


chrome_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_path)
browser = Chrome(service=browser_service)

browser.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2")
vacancies_tag = browser.find_element(by=By.TAG_NAME, value="main")
vacancies_tag_list = vacancies_tag.find_elements(by=By.CLASS_NAME, value="vacancy-serp-item-body")
print("vacancies_list", vacancies_tag_list)
parsed_data = []
final_data = []
for vacance_tag in vacancies_tag_list:
     h3_tag = wait_element(vacance_tag, 1, By.TAG_NAME, "h3")
     
     title = h3_tag.text
     a_tag = wait_element(h3_tag, 1, By.TAG_NAME, "a")
     link_absolute = a_tag.get_attribute("href")
     describe = vacance_tag.text.strip().split('\n')
     
     vacance_dict = {
         "title": title,
         "link_absolute": link_absolute,
         "describy": describe,
         "text": None,
     }

     parsed_data.append(vacance_dict)
counter = 0
for vacance_dict in parsed_data:
     counter += 1
     if counter % 12 == 0:
         chrome_path = ChromeDriverManager().install()
         browser_service = Service(executable_path=chrome_path)
         browser = Chrome(service=browser_service)
         browser.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2")
         
     link = vacance_dict["link_absolute"]
     browser.get(link)
     skills = browser.find_element(by=By.CLASS_NAME, value="bloko-tag-list")
     vacance_dict["text"] = skills.text.strip().split('\n')
     print(counter, 'title', vacance_dict["title"], 'skils', vacance_dict["text"])
     if "Django" in vacance_dict["text"] and "Flask" in vacance_dict["text"]:
         print('find key_words!')
         if len(vacance_dict["describy"]) > 3:
             salary = vacance_dict["describy"][1]
             company = vacance_dict["describy"][2]
             city = (vacance_dict["describy"][-1].split(',')[0]).strip()
         else:
             salary = None
             company = vacance_dict["describy"][1]
             city = (vacance_dict["describy"][-1].split(',')[0]).strip()
             
             
         final_dict = {
             "link_absolute": link_absolute,
             "company": company,
             "city ": city,
             "salary": salary,
         }
         print(final_dict)
         final_data.append(final_dict)

#pprint(parsed_data)
pprint(final_data)

