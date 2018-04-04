import config as settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def login(browser, username_str, password_str):

    browser.get(settings.LOGIN_URL)

    try:

        wait = WebDriverWait(browser, 30)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signin_email"]')))

        username = browser.find_element_by_id('signin_email')
        password = browser.find_element_by_id('signin_password')

        username.send_keys(username_str)
        password.send_keys(password_str)
        password.submit()

        return browser

    except TimeoutException:

        print "Timed out waiting for page to load"
        browser.quit()

        return None


def get_browser():

    browser = webdriver.PhantomJS(executable_path=settings.WEBDRIVER_EXECUTABLE_PATH)

    if settings.LOGIN_REQUIRED:

        username = settings.LOGIN_USERNAME
        password = settings.LOGIN_PASSWORD

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

        print "Execution Running without login"
        return browser


def closeBrowser(browser):
    browser.quit()
