import config as settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random


def get_login_credentials():

    """
    Randomly selects a login credential and return to program.

    :return: If found return username, password. Otherwise Null
    """

    try:

        login_credentials = random.choice(settings.LOGIN_DETAILS)

        username = login_credentials['username']
        password = login_credentials['password']

        return username, password

    except Exception as e:

        return None, None


def open_link(browser, url):

    """
    Open provided url in the browser

    :param browser: webdriver instance
    :param url: url to be opened
    :return: Null
    """

    browser.get(url)


def wait_till(browser, key, value):

    """
    Stop the execution till given element is found in the browser

    :param browser: webdriver instance
    :param key: selector: 'id', 'class', 'xpath'
    :param value: value for the selector
    :return: True if element found, otherwise False
    """

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

    """
    Enter given keys to form elements in webpage

    :param elements: WebElements
    :param submit: submit flag. if True, form will be submitted after entering keys
    :return: None
    """

    final_element = None
    for each_element in elements:
        each_element['element'].send_keys(each_element['value'])
        final_element = each_element

    if submit:
        final_element['element'].submit()


def find_elements(browser, key, value):

    """
    Find the given WebElement in the webpage and return the object

    :param browser: Webdriver instance
    :param key: selector: 'id', 'class', 'xpath'
    :param value: value for the selector
    :return: Element if found, Otherwise Null
    """

    try:

        if key == 'id':

            return browser.find_element_by_id(value)

        elif key == 'class':

            return browser.find_elements_by_class_name(value)

    except Exception as e:

        print "# E: [FIND ELEMENT] {error}".format(error=str(e))
        return None


def get_main_window(browser):

    """
    Returns the current tab in focus

    :param browser: Webdriver Instance
    :return: Current tab in focus
    """

    return browser.current_window_handle


def execute_javascript(browser, script):

    """
    For injecting javascript

    :param browser: Webdriver instance
    :param script: script to be injected
    :return: Null
    """

    browser.execute_script(script)


def get_window_handles(browser):

    """
    Return list of all Tabs currently open in browser

    :param browser: Webdriver instance
    :return: List of all Tabs currently open in browser
    """

    return browser.window_handles


def switch_to_window(browser, window):

    """
    To switch to given Tab

    :param browser: Webdriver instance
    :param window: Tab to switch
    :return: Null
    """

    browser.switch_to_window(window)


def close_tab(browser):

    """
    To close the current tab

    :param browser: Webdriver instance
    :return: Null
    """

    browser.close()


def close_browser(browser):

    """
    To close the browser

    :param browser: Webdriver instance
    :return: Null
    """

    browser.quit()


def login(browser, username_str, password_str):

    """
    To login into indeed using given username and password

    :param browser: Webdriver instance
    :param username_str: username for login
    :param password_str: password for login
    :return: browser in logged in state, if successful login, otherwise Null
    """

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

    """
    Open new webdriver instance and return

    :return: Webdriver instance (Logged in if required)
    """

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
