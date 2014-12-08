
import argparse
import time
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

SLIVKI_URL = 'http://www.slivki.by/'
VK_URL = 'http://vk.com/'
TWITTER_URL = 'https://twitter.com/'

DRIVER_FIREFOX = 'firefox'
DRIVER_CHROME = 'chrome'


def sleep(seconds):
    time.sleep(seconds)


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
    sleep(1)
    get_element(driver, 'input#signin-password').send_keys(password)
    sleep(1)
    get_element(driver, 'table.password-signin button[type=submit]').submit()
    sleep(3)


def login_to_slivki(driver, login, password):
    driver.get(SLIVKI_URL)
    get_element(driver, '.topUserLoginBox a').click()
    get_element(driver, '.userLoginFormTable input#userRegLoginEmail').send_keys(login)
    get_element(driver, '.userLoginFormTable input#userRegLoginPassword').send_keys(password)
    get_element(driver, '.userLoginFormTable input#userRegLoginBtn').submit()
    sleep(3)


def go_to_action(driver):
    driver.get(SLIVKI_URL)

    num_actions = len(driver.find_elements_by_css_selector('.marketActionItemImg'))
    num = random.randint(0, num_actions - 1)
    driver.find_elements_by_css_selector('.marketActionItemImg a')[num].click()

    sleep(3)
    driver.switch_to_frame(get_element(driver, '#twitter-widget-0'))
    get_element(driver, 'span.label').click()

    current_handle = driver.current_window_handle
    driver.switch_to_window(driver.window_handles[-1])
    get_element(driver, 'form#update-form input[type=submit]').click()
    sleep(3)
    driver.switch_to_window(current_handle)

    sleep(3)


def remove_tweets(driver, load_page=False):
    if load_page:
        driver.get(TWITTER_URL + 'andrei_menkou')
        sleep(3)

    remove_buttons = driver.find_elements_by_xpath(
        '''//*[starts-with(@id,'stream-item-tweet-')]/div/div[2]/
        p/a[contains(@data-expanded-url, 'slivki')]/
        ../..//div[contains(@class, 'more')]/div/button''')

    if len(remove_buttons) > 0:
        remove_buttons[0].click()
        remove_buttons[0].find_element_by_xpath('..')\
            .find_element_by_css_selector('li.js-actionDelete button').click()
        get_element(driver, 'div.modal-footer button.delete-action').click()

    if len(remove_buttons) > 1:
        return True


def init_driver(driver_name):
    if driver_name == DRIVER_FIREFOX:
        return webdriver.Firefox()
    elif driver_name == DRIVER_CHROME:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches",
                                        ["ignore-certificate-errors"])

        return webdriver.Chrome(chrome_options=options)
    else:
        raise RuntimeError('Unknown driver option')


def main():
    driver = None

    try:
        parser = argparse.ArgumentParser(
            description='Script for earning money on slivki')

        parser.add_argument('-sl', action='store', dest='slivki_login',
                            help='Slivki user login')
        parser.add_argument('-sp', action='store', dest='slivki_pass',
                            help='Slivki user pass')
        parser.add_argument('-tl', action='store', dest='twitter_login',
                            help='Twitter user login')
        parser.add_argument('-tp', action='store', dest='twitter_pass',
                            help='Twitter user pass')
        parser.add_argument('-d', action='store', dest='driver',
                            default=DRIVER_CHROME,
                            choices=[DRIVER_CHROME, DRIVER_FIREFOX],
                            help='Web driver to use')

        args = parser.parse_args()

        driver = init_driver(args.driver)

        driver.maximize_window()
        login_to_twitter(driver, args.twitter_login, args.twitter_pass)
        login_to_slivki(driver, args.slivki_login, args.slivki_pass)
        go_to_action(driver)
        go_to_action(driver)

        sleep(10)

        i = 0
        need_remove = remove_tweets(driver, True)
        while need_remove:
            i += 1
            i %= 10
            sleep(2)
            need_remove = remove_tweets(driver, i == 0)
    except Exception as e:
        print e
    finally:
        driver.close()


if __name__ == '__main__':
    main()
