#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

USERNAME = ''
PASSWORD = ''
HEADLESS = False
USE_FIREFOX = True

options = Options()
options.headless = HEADLESS

if USE_FIREFOX:
    driver = webdriver.Firefox
    newtab_page = 'about:newtab'
else:
    driver = webdriver.Chrome
    newtab_page = 'chrome://newtab'


def get_article(browser: webdriver.Firefox):
    browser.get('https://fedoramagazine.org/')
    time.sleep(2)  # wait for page to load
    most_recent_post = browser.find_element_by_css_selector('#posts > div:first-child')
    most_recent_post.click()
    time.sleep(2)  # wait for page to load
    title = browser.find_element_by_css_selector("h1.post-title").text
    url = browser.current_url
    browser.get('about:newtab')
    return title, url


class TwitterBot:
    def __init__(self, username, password):
        self.browser = driver(options=options)
        self.username = username
        self.password = password
        self.logged_in = False

    def login(self, username=None, password=None):
        """Logs into twitter"""
        if not username or not password:
            username,  password = self.username, self.password
        self.browser.get("https://twitter.com/login")
        time.sleep(1)  # wait for page to load
        actions = ActionChains(self.browser)
        actions.send_keys(username, Keys.TAB, password, Keys.TAB, Keys.RETURN)
        actions.perform()
        time.sleep(3)  # wait for login to finish
        self.logged_in = True
        self.browser.get('about:newtab')

    def tweet(self, message):
        """Makes a tweet"""
        if not self.logged_in:  # login if not logged in
            self.login()
        self.browser.get('https://twitter.com/compose/tweet')
        time.sleep(2)  # wait for page to load
        self.browser.find_element_by_class_name("DraftEditor-root").click()
        actions = ActionChains(self.browser)
        actions.send_keys(message)
        actions.perform()
        time.sleep(1)  # wait for links to cache
        self.browser.find_element_by_css_selector('div[data-testid="tweetButton"').click()
        time.sleep(1)  # let post complete
        self.browser.get(newtab_page)


if __name__ == '__main__':
    print("Opening Browser%s." % (' in headless mode' if HEADLESS else ''))
    bot = TwitterBot(USERNAME, PASSWORD)
    print("Logging into twitter.")
    bot.login()
    print("Fetching latest article.")
    article = get_article(bot.browser)
    print('\u001b[32m', article[0], '\n', article[1], '\u001b[0m')
    print("Tweeting.")
    bot.tweet(article[0] + '\n' + article[1])
    print("Done. Exiting in 5s.")
    time.sleep(5)
    bot.browser.quit()
