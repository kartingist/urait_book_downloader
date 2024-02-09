import os
import shutil
import time
import img2pdf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from auth import *

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
# options.headless = True
options.add_argument('headless')
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(15)
actions = ActionChains(browser)
book_name = ''

# url = 'https://urait.ru/book/psihologiya-i-pedagogika-igry-438327'
url = input('Вставьте ссылку на книгу из urait: ')
img_list = []


def close_modal():
    browser.find_element(By.CSS_SELECTOR, '#teacher-school-invite > div.ts-invite__footer > button').click()
    time.sleep(0.1)
    global book_name
    book_name = browser.find_element(By.XPATH, '//*[@id="book"]/div[2]/div[1]/div[1]/h1').text


def autorization():
    print('Идет авторизация')
    browser.find_element(By.XPATH, '/html/body/header/div/div/div[5]/div[3]/div[1]/a[1]').click()
    # browser.find_element(By.CLASS_NAME, 'user_info').click()
    # browser.find_element(By.ID, '/html/body/div[5]/div/div/div[2]/a[1]').click()
    time.sleep(1)

    email = browser.find_elements(By.XPATH, '//*[@id="email"]')
    email[1].send_keys(login)
    time.sleep(1)
    password_1 = browser.find_element(By.XPATH, '//*[@id="password"]')
    # password_1.click()
    # password_1.send_keys()
    password_1.send_keys(password)
    # password.send_keys(password)
    browser.find_element(By.CSS_SELECTOR, '#login-form > div > div.content-center-form__submit > button').click()
    # browser.find_element(By.XPATH, '//*[@id="login-form"]/div/div[5]/button').click()
    print('Авторизация пройдена')


def open_book():
    #global book_name
    #book_name = browser.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/h3').text
    print('Открываю книгу...')
    print(book_name)
    js_script = '''\
        document.getElementsByClassName('cookie-policy-promo')[0].setAttribute("hidden","");
                '''
    browser.execute_script(js_script)
    browser.find_element(By.XPATH, '//*[@class="button-white--view button-green button-green--read"]').click()
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    print('Книга открыта')


def get_pages():
    print('Получаем количество страниц')
    count_pages = int(browser.find_element(By.CSS_SELECTOR, '#viewer__bar__pages-scale > span:nth-child(3)').text[2:])
    print(f'Количество страниц: {count_pages}')
    return count_pages


def save_book(get_pages):
    print('Начинается сохранение')
    url_page = browser.current_url
    url_book = url_page[: url_page.rfind('/') + 1]
    link = f'{url_book}1'
    browser.get(link)
    browser.set_window_size(2000, 2000)
    os.mkdir('pages')

    for i in range(1, get_pages + 1):
        if i%20==0:
            time.sleep(10)
        print(f'Сохранено страниц: {i} из {get_pages}')
        page = browser.find_element(By.CSS_SELECTOR, f'#page_{i}')
        page.screenshot(f"pages/page_{i}.png")
        img_list.append(f"pages/page_{i}.png")


def create_file():

    with open(f'{book_name}.pdf', 'wb') as f:
        f.write(img2pdf.convert(img_list))
    print('Книга успешно создана')


try:
    browser.set_window_size(1920, 1080)
    browser.get(url)
    # close_modal()
    autorization()
    open_book()
    save_book(get_pages())
    create_file()

except Exception as ex:
    print(ex)
finally:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'pages')
    shutil.rmtree(path)
    print('Ненужные файлы успешно удалены')
    browser.quit()


