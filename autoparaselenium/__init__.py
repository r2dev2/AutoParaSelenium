import itertools as it
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from functools import partial, wraps
from typing import Iterable, List, Optional

from autoparaselenium.browsers import chrome, firefox
from autoparaselenium.browser_pool import BrowserPool
from autoparaselenium.models import Conf, Extension


_browser_pool: Optional[BrowserPool] = None
all_ = [chrome, firefox]

_test_count = 0 # manual reference counting since threading borks with destructors


def configure(*_, extensions: List[Extension] = [], headless=True, selenium_dir="drivers"):
    global _browser_pool

    if _browser_pool is not None:
        return

    conf = Conf(extensions=extensions, headless=headless, selenium_dir=selenium_dir)
    for browser in [chrome, firefox]:
        browser.setup_driver(conf.selenium_dir)

    _browser_pool = BrowserPool(conf, __get_threads())


def run_on(*browsers):
    browsers = [*browsers]

    if not browsers:
        raise TypeError("Please specify a browser or browser list to run on")


    if isinstance(browsers[0], Iterable):
        browsers = [*it.chain(*browsers)]

    if len(browsers) == 1:
        return partial(__wrap_test, browsers[0])

    def wrapper(test):
        # Run on both firefox and chrome
        to_run = [*map(partial(__wrap_test, test=test), browsers)]

        def inner():
            if "--tests-per-worker" in sys.argv:
                with ThreadPoolExecutor(max_workers=len(to_run)) as pool:
                    [*pool.map(lambda test_: test_(), to_run)]
            else:
                for test_ in to_run:
                    test_()

        inner.__name__ = test.__name__
        inner.__doc__ = test.__doc__

        return inner

    return wrapper


def __wrap_test(browser, test):
    global _test_count

    _test_count += 1

    if _browser_pool is None:
        raise RuntimeError("Please call autoparaselenium.configure() before creating tests")

    def inner():
        global _test_count

        try:
            _test_count -= 1
            driver = _browser_pool.acquire(browser)
            driver.get("data:,") # initialize driver website
            test(driver)
        finally:
            with suppress(Exception):
                _browser_pool.release(driver)

            if _test_count == 0:
                time.sleep(0.10) # idk but seems like it needs a bit of time before you can close the pool
                _browser_pool.clean_up()


    inner.__name__ = f"{test.__name__}__{'chrome' if browser is chrome else 'firefox'}"
    inner.__doc__ = test.__doc__

    return inner


def __get_threads(args=sys.argv):
    if "--tests-per-worker" not in args:
        return 1
    tests_per_worker_idx = args.index("--tests-per-worker")
    next_arg = "".join(args[tests_per_worker_idx + 1: tests_per_worker_idx + 2])
    if next_arg == "auto":
        return os.cpu_count() // 2 + 1
    try:
        return int("0" + next_arg) // 2 + 1
    except ValueError:
        return 1
