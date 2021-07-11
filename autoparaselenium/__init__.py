from functools import partial, wraps
from typing import List, Optional

import pytest

from autoparaselenium.browsers import chrome, firefox
from autoparaselenium.browser_pool import BrowserPool
from autoparaselenium.models import Conf, Extension


_browser_pool: Optional[BrowserPool] = None


def configure(*_, extensions: List[Extension] = [], headless=True, selenium_dir="drivers", threads=1):
    global _browser_pool

    if _browser_pool is not None:
        return

    conf = Conf(extensions=extensions, headless=headless, selenium_dir=selenium_dir)
    for browser in [chrome, firefox]:
        browser.setup_driver(conf.selenium_dir)

    _browser_pool = BrowserPool(conf, threads)


@pytest.mark.skip(reason="this isn't a test")
def test(browser_or_test):
    # if wrapper called with browser argument
    if browser_or_test is firefox or browser_or_test is chrome:
        return partial(__wrap_test, browser_or_test)

    # Run on both firefox and chrome
    to_run = [*map(partial(__wrap_test, test=browser_or_test), [chrome, firefox])]

    def inner():
        for test_ in to_run:
            test_()

    inner.__name__ = browser_or_test.__name__
    inner.__doc__ = browser_or_test.__doc__

    return inner


def __wrap_test(browser, test):
    if _browser_pool is None:
        raise RuntimeError("Please call autoparaselenium.configure() before creating tests")

    def inner():
        try:
            driver = _browser_pool.acquire(browser)
            driver.get("data:,") # initialize driver website
            test(driver)
        finally:
            _browser_pool.release(driver)

    inner.__name__ = f"{test.__name__}__{'chrome' if browser is chrome else 'firefox'}"
    inner.__doc__ = test.__doc__

    return inner
