from contextlib import suppress
from functools import partial
from pathlib import Path

from selenium import webdriver

import autoparaselenium.setup_utils as su
from autoparaselenium.models import Conf, Extension


class FirefoxDriver(webdriver.Firefox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_quit = False

    def quit(self):
        if not self.has_quit:
            self.has_quit = True
            super().quit()

    def __del__(self):
        with suppress(Exception):
            self.quit()


def setup_driver(pwd: Path) -> None:
    __setup_driver(pwd)


def get_selenium(pwd: Path, conf: Conf) -> webdriver.Firefox:
    fp = webdriver.FirefoxProfile()
    fp.DEFAULT_PREFERENCES["frozen"]["xpinstall.signatures.required"] = False

    options = webdriver.FirefoxOptions()
    options.headless = conf.headless

    browser = FirefoxDriver(
        executable_path=pwd / __platform_drivers[su.platform],
        firefox_profile=fp,
        options=options,
    )

    for ext in conf.extensions:
        if ext.firefox:
            browser.install_addon(ext.firefox, True)

    return browser


__platform_drivers = {
    "win": "geckodriver.exe",
    "darwin": "geckodriver",
    "linux": "geckodriver",
}


__setup_driver = partial(
    su.setup_driver,
    {
        "win": [
            "https://github.com/mozilla/geckodriver/releases"
            "/download/v0.28.0/geckodriver-v0.28.0-win64.zip",
            su.unzip,
        ],
        "darwin": [
            "https://github.com/mozilla/geckodriver/releases/"
            "download/v0.28.0/geckodriver-v0.28.0-macos.tar.gz",
            su.untar,
        ],
        "linux": [
            "https://github.com/mozilla/geckodriver/releases"
            "/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz",
            su.untar,
        ],
    },
    __platform_drivers,
)
