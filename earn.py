
import argparse
import time
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

SLIVKI_URL = 'http://www.slivki.by/'
VK_URL = 'http://vk.com/'
TWITTER_URL = 'https://twitter.com/'


def get_element(driver, css_selector):
    try:
        def find(driver):
            e = driver.find_element_by_css_selector(css_selector)
            if e.get_attribute('disabled') == 'true':
                return False

            return e

        element = WebDriverWait(driver, 10).until(find)

        return element
    except TimeoutException:
        return None


def login_to_vk(driver, login, password):
    driver.get(VK_URL)
    get_element(driver, 'input#quick_email').send_keys(login)
    get_element(driver, 'input#quick_pass').send_keys(password)
    get_element(driver, 'div#quick_login input[type=submit]').submit()


def login_to_twitter(driver, login, password):
    driver.get(TWITTER_URL)
    get_element(driver, 'input#signin-email').send_keys(login)
    get_element(driver, 'input#signin-password').send_keys(password)
    get_element(driver, 'table.password-signin button[type=submit]').click()


def login_to_slivki(driver, login, password):
    driver.get(SLIVKI_URL)
    get_element(driver, '.topUserLoginBox a').click()
    get_element(driver, '.userLoginFormTable input#userRegLoginEmail').send_keys(login)
    get_element(driver, '.userLoginFormTable input#userRegLoginPassword').send_keys(password)
    get_element(driver, '.userLoginFormTable input#userRegLoginBtn').submit()


def go_to_action(driver):
    driver.get(SLIVKI_URL)

    num_actions = len(driver.find_elements_by_css_selector('.marketActionItemImg'))
    num = random.randint(0, num_actions - 1)
    driver.find_elements_by_css_selector('.marketActionItemImg a')[num].click()

    time.sleep(3)
    driver.switch_to_frame(get_element(driver, '#twitter-widget-0'))
    get_element(driver, 'span.label').click()

    current_handle = driver.current_window_handle
    driver.switch_to_window(driver.window_handles[-1])
    get_element(driver, 'form#update-form input[type=submit]').click()
    time.sleep(2)
    driver.switch_to_window(current_handle)

    time.sleep(3)


def remove_tweets(driver):
    driver.get(TWITTER_URL + 'andrei_menkou')
    # get_element(driver, 'li.profile').click()
    remove_buttons = driver.find_elements_by_xpath(
        '//p[contains(@class, js-tweet-text)]//a[contains(@title, \'slivki\')]'
        '/../..//button[contains(@class, \'js-actionDelete\')]')

    if len(remove_buttons) > 0:
        remove_buttons[0].click()
        get_element(driver, 'div.modal-footer button.delete-action').click()

    if len(remove_buttons) > 1:
        return True


def main():
    parser = argparse.ArgumentParser(description='Script for earning money on slivki')
    parser.add_argument('-sl', action='store', dest='slivki_login', help='Slivki user login')
    parser.add_argument('-sp', action='store', dest='slivki_pass', help='Slivki user pass')
    parser.add_argument('-tl', action='store', dest='twitter_login', help='Twitter user login')
    parser.add_argument('-tp', action='store', dest='twitter_pass', help='Twitter user pass')

    args = parser.parse_args()

    driver = webdriver.Firefox()

    driver.maximize_window()
    login_to_twitter(driver, args.twitter_login, args.twitter_pass)
    login_to_slivki(driver, args.slivki_login, args.slivki_pass)
    go_to_action(driver)
    go_to_action(driver)

    time.sleep(20)

    need_remove = remove_tweets(driver)
    while need_remove:
        need_remove = remove_tweets(driver)

    driver.close()


if __name__ == '__main__':
    main()
