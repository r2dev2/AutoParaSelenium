from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from queue import Queue
from threading import Lock

from selenium import webdriver

from autoparaselenium.browsers import chrome, firefox
from autoparaselenium.models import Conf


class BrowserPool:
    def __init__(self, conf: Conf, threads: int):
        self._conf = conf
        self._threads = threads

        self._chromes = Queue()
        self._firefoxes = Queue()

        with ThreadPoolExecutor(max_workers=threads) as pool:
            for driver in pool.map(self.__open_browser, [chrome] * threads):
                self._chromes.put(driver)

            for driver in pool.map(self.__open_browser, [firefox] * threads):
                self._firefoxes.put(driver)

    def acquire(self, browser):
        return self.__get_queue(browser).get(browser)

    def release(self, driver):
        browser = chrome if isinstance(driver, webdriver.Chrome) else firefox
        self.__get_queue(browser).put(driver)

    def __get_queue(self, browser):
        return self._chromes if browser is chrome else self._firefoxes

    def __open_browser(self, browser):
        driver = browser.get_selenium(self._conf.selenium_dir, self._conf)
        with suppress(Exception):
            driver.switch_to.window("1")
        return driver

    def clean_up(self):
        for q in [self._chromes, self._firefoxes]:
            while not q.empty():
                driver = q.get()
                driver.quit()
