import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)
parse_url = 'https://journal.top-academy.ru/ru/main/library/page/index/5'

while True:
    driver.get('https://journal.top-academy.ru/ru/auth/login/index')
    wait = WebDriverWait(driver, 320)
    user_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'form-control')]")))
    user_field.send_keys('USER_LOGIN')
    password_field = driver.find_element(By.XPATH, "//input[@id='password']")
    password_field.send_keys('USER_PASSWORD')
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                          '/html/body/mystat/ng-component/ng-component/section/div/div/div/div/div[1]/tabset/div/tab[1]/form/button')))
    # добавляем ожидание перед нажатием кнопки вход
    wait.until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/mystat/ng-component/ng-component/section/div/div/div/div/div[1]/tabset/div/tab[1]/form/button')))
    login_button.click()

    time.sleep(10)
    # ожидаем переход на страницу сбора
    try:
        driver.get(parse_url)
        wait.until(EC.url_to_be(parse_url))
    except:
        # если не произошел переход на страницу сбора, то мы пробуем перейти на эту страницу
        print("Failed to redirect to parsing page. Trying again.")
        driver.get(parse_url)
        try:
            wait.until(EC.url_to_be(parse_url))
        except:
            # если этот второй переход не сработал, то просто выходим из цикла
            print("Failed to redirect to parsing page. Exiting loop.")
            break

    # проверка, прошла ли авторизация
    if driver.current_url == parse_url:
        break
    else:
        continue

time.sleep(5)

video_blocks = driver.find_elements(By.CSS_SELECTOR, '.video-block')
for video_block in video_blocks:
    video_block.click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    html = driver.page_source
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    for iframe in iframes:
        src = iframe.get_attribute('src')
        if src:
            with open('iframe_links.txt', 'a') as f:
                f.write(f'{src}\n')


driver.quit()