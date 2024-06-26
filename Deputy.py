import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import credentials


def login():
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

    return driver


def start_shift():
    try:
        driver = login()
        driver.save_screenshot("homepage.png")
        driver.find_element(By.XPATH, '//*[@id="js-MyWeek-PopupShift"]/div[3]/div[2]/div[1]/div[2]').click()
        time.sleep(5)
        driver.quit()
    except Exception as e:
        requests.get(f"http://api.shash.win/discord-bot/send-message?message=start shift failed {e}&channel_id=1187345577235730466")


def end_shift(end_time):
    try:
        driver = login()
        driver.find_element(By.XPATH, '//*[@id="js-MyWeek-PopupShift"]/div[3]/div[2]/div[3]/div/div[2]/button').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="myweek-modal-endShift"]/div/div/div[2]/div/div[1]/div[3]/div/input').send_keys(Keys.LEFT_CONTROL + "a")
        driver.find_element(By.XPATH, '//*[@id="myweek-modal-endShift"]/div/div/div[2]/div/div[1]/div[3]/div/input').send_keys(end_time)
        driver.find_element(By.XPATH, '//*[@id="myweek-modal-endShift"]/div/div/div[3]/button[3]').click()
        time.sleep(5)
        driver.save_screenshot("end_shift_modal.png")
        driver.quit()
    except Exception as e:
        requests.get(f"http://api.shash.win/discord-bot/send-message?message=end shift failed {e}&channel_id=1187345577235730466")

    pass


if __name__ == '__main__':
    start_shift()
    # end_shift("05:19 PM")
