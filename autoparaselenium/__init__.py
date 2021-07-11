from typing import List, Optional

from autoparaselenium.browsers import chrome, firefox
from autoparaselenium.browser_pool import BrowserPool
from autoparaselenium.models import Conf, Extension


_browser_pool: Optional[BrowserPool] = None


def configure(*_, extensions: List[Extension] = [], headless=True, selenium_dir="drivers", threads=1):
    global _browser_pool

    conf = Conf(extensions=extensions, headless=headless, selenium_dir=selenium_dir)
    for browser in [chrome, firefox]:
        browser.setup_driver(conf.selenium_dir)

    _browser_pool = BrowserPool(conf, threads)
