import os
import stat
import subprocess as sb
import sys
from contextlib import suppress
from functools import partial
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import autoparaselenium.setup_utils as su
from autoparaselenium.models import Conf


class Popen(sb.Popen):
    """
    Suppress chromedriver output on winblows
    """

    def __init__(self, *args, **kwargs):
        # Flags needed to suppress chromedriver output on winblows
        if sys.platform[:3] == "win":
            kwargs = {
                "stdin": sb.PIPE,
                "stdout": sb.PIPE,
                "stderr": sb.PIPE,
                "shell": False,
                "creationflags": 0x08000000,
            }
        super().__init__(*args, **kwargs)


class ChromeDriver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        old_popen = sb.Popen
        sb.Popen = Popen
        super().__init__(*args, **kwargs)
        sb.Popen = old_popen
        self.has_quit = False

    def quit(self):
        if not self.has_quit:
            self.has_quit = True
            super().quit()

    def __del__(self):
        with suppress(Exception):
            self.quit()


def get_selenium(pwd: Path, conf: Conf) -> webdriver.Chrome:
    options = __get_options(conf)
    browser = ChromeDriver(
        executable_path=pwd / __platform_drivers[su.platform], options=options
    )
    return browser


def setup_driver(pwd) -> None:
    __setup_driver(pwd)
    if (pwd / "chromedriver").exists():
        os.chmod(pwd / "chromedriver", stat.S_IEXEC)


def __get_options(conf: Conf) -> Options:
    options = Options()
    if conf.headless and all(ext.chrome is None for ext in conf.extensions):
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")

    for ext in conf.extensions:
        if ext.chrome is not None:
            options.add_extension(ext.chrome)

    return options


__platform_drivers = {
    "win": "chromedriver.exe",
    "darwin": "chromedriver",
    "linux": "chromedriver",
}

version = "91.0.4472.101"

__setup_driver = partial(
    su.setup_driver,
    {
        "win": [
            "https://chromedriver.storage.googleapis.com"
            f"/{version}/"
            "chromedriver_win32.zip",
            su.unzip,
        ],
        "darwin": [
            "https://chromedriver.storage.googleapis.com"
            f"/{version}/"
            "chromedriver_mac64.zip",
            su.untar,
        ],
        "linux": [
            "https://chromedriver.storage.googleapis.com"
            f"/{version}/"
            "chromedriver_linux64.zip",
            su.unzip,
        ],
    },
    __platform_drivers,
)
