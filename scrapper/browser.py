import config as settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random


def get_login_credentials():

    try:

        login_credentials = random.choice(settings.LOGIN_DETAILS)

        username = login_credentials['username']
        password = login_credentials['password']

        return username, password

    except Exception as e:

        return None, None


def open_link(browser, url):
    browser.get(url)


def wait_till(browser, key, value):
    try:
        wait = WebDriverWait(browser, 10)

        if key == 'id':
            wait.until(EC.visibility_of_element_located((By.ID, value)))

        elif key == 'class':
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, value)))

        elif key == 'xpath':
            wait.until(EC.visibility_of_element_located((By.XPATH, value)))

        return True
    except TimeoutException as e:
        print "# E: [FIND ELEMENT] {error}".format(error=str(e))
        return False


def send_keys(elements, submit=False):

    final_element = None
    for each_element in elements:
        each_element['element'].send_keys(each_element['value'])
        final_element = each_element

    if submit:
        final_element['element'].submit()


def find_elements(browser, key, value):

    try:

        if key == 'id':

            return browser.find_element_by_id(value)

        elif key == 'class':

            return browser.find_elements_by_class_name(value)

    except Exception as e:
        print "# E: [FIND ELEMENT] {error}".format(error=str(e))
        return None


def get_main_window(browser):
    return browser.current_window_handle


def execute_javascript(browser, script):
    browser.execute_script(script)


def get_window_handles(browser):
    return browser.window_handles


def switch_to_window(browser, window):
    browser.switch_to_window(window)


def close_tab(browser):
    browser.close()


def close_browser(browser):
    browser.quit()


def login(browser, username_str, password_str):

    open_link(browser, settings.LOGIN_URL)

    found = wait_till(browser, 'xpath', '//*[@id="signin_email"]')
    if found:

        username = find_elements(browser, 'id', 'signin_email')
        password = find_elements(browser, 'id', 'signin_password')

        send_keys([
            {
                'element': username,
                'value': username_str
            },
            {
                'element': password,
                'value': password_str
            }
        ], submit=True)

        logged_in = wait_till(browser, 'id', 'userOptionsLabel')

        if logged_in:
            return browser
        else:
            return None

    else:
        print "Timed out waiting for page to load"
        browser.quit()
        return None


def get_browser():

    browser = webdriver.PhantomJS(executable_path=settings.WEBDRIVER_EXECUTABLE_PATH)

    if settings.LOGIN_REQUIRED:

        username, password = get_login_credentials()

        if username and password:

            print "##################################################"
            print "Execution Running with login"
            print
            print "Username: {username}".format(username=username)
            print "Password: {password}".format(password=password)
            print "##################################################"

            logged_in_browser = login(browser, username, password)

            if logged_in_browser:
                return logged_in_browser

            else:
                print "Problem in logging in (Check your username and password or internet connection)"
                return None

        else:
            print "Login Credentials not provided."
            return None

    else:

        print "##################################################"
        print "Execution Running without login"
        print "##################################################"

        return browser
