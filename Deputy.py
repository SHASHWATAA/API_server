from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import credentials


def start_shift():
    chrome_options = Options()

    username = credentials.deputy_username
    password = credentials.deputy_password
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://47825117100349.au.deputy.com")
    # driver.get("https://once.deputy.com/my/oauth/login?client_id=1b3cc57e2215a12579ec036f5884b049e61ef4d4&redirect_uri"
    #            "=http://localhost&response_type=code&scope=longlife_refresh_token")

    driver.find_element(By.ID, "login_ctl").send_keys(username)
    driver.find_element(By.ID, "password_ctl").send_keys(password)
    driver.find_element(By.ID, "btnLogin_ctl").click()

    driver.save_screenshot("homepage.png")
    driver.find_element(By.XPATH, '//*[@id="js-MyWeek-PopupShift"]/div[3]/div[2]/div[1]/div[2]').click()
    # driver.find_element(By.XPATH, '//*[@id="js-MyWeek-PopupShift"]/div[3]/div[2]/div[1]/div[2]/button[1]').click()


if __name__ == '__main__':
    start_shift()
