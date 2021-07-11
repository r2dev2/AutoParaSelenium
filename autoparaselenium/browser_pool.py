from concurrent.futures import ThreadPoolExecutor

from autoparaselenium.models import Conf
from autoparaselenium.browsers import chrome, firefox

class BrowserPool:
    def __init__(self, conf: Conf, threads: int):
        self._conf = conf
        self._threads = threads

        with ThreadPoolExecutor(max_workers=threads) as pool:
            self._chromes = pool.map(self.__open_browser, [chrome] * threads)
            self._firefoxes = pool.map(self.__open_browser, [firefox] * threads)


    def acquire(self, browser):
        ...


    def __open_browser(self, browser):
        return browser.get_selenium(self._conf.pwd, self._conf)
