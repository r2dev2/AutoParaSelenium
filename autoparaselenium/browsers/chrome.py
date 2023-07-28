import atexit
import os
import stat
import subprocess as sb
import sys
from contextlib import suppress
from functools import partial
from pathlib import Path
from typing import Optional

import requests
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
        atexit.register(self.quit)

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


def setup_driver(pwd: Path) -> None:
    chrome_version = __get_chrome_version()
    driver_version = __get_chromedriver_version(pwd)
    if driver_version is None or driver_version < chrome_version:
        # chromedriver changed its LATEST_RELEASE_{version} api and download link
        # for chrome >= 115
        if chrome_version < 115:
            r = requests.get(
                "https://chromedriver.storage.googleapis.com"
                f"/LATEST_RELEASE_{chrome_version}"
            )
            version = r.text.strip()
            if (pwd / "chromedriver").exists():
                os.remove(pwd / "chromedriver")
            __setup_driver_old(version)(pwd)
        else:
            r = requests.get(
                "https://googlechromelabs.github.io/chrome-for-testing/"
                "latest-versions-per-milestone-with-downloads.json"
            )
            supported_platforms = {
                "linux64": "linux",
                "mac-x64": "darwin",
                "win64": "win",
            }
            downloads = {
                supported_platforms.get(entry["platform"]): [
                    entry["url"],
                    su.unzip,
                ]
                for entry in (
                    r.json()["milestones"][str(chrome_version)]["downloads"][
                        "chromedriver"
                    ]
                )
            }
            if (pwd / "chromedriver").exists():
                os.remove(pwd / "chromedriver")
            su.setup_driver(downloads, __platform_drivers, pwd)
        os.chmod(pwd / "chromedriver", stat.S_IEXEC)


def __get_chromedriver_version(pwd: Path) -> Optional[int]:
    with suppress(Exception):
        # version returned will be the major version
        p = sb.Popen([str(pwd / "chromedriver"), "--version"], stdout=sb.PIPE)
        atexit.register(p.terminate)

        # output of cmd will be lik
        # ChromeDriver 108.0.5359.71 (1e0e3868ee06e91ad6...
        version = p.communicate()[0].decode().split(" ")[1]
        major, *_ = version.split(".")

        # will raise ValueError if major version isn't a proper number
        return int(major)


def __get_chrome_version() -> int:
    p = sb.Popen([__platform_binaries[su.platform], "--version"], stdout=sb.PIPE)
    atexit.register(p.terminate)

    # output of cmd will be lik
    # Google Chrome 108.0.5359.124
    major = p.communicate()[0].decode().split(".")[0].split(" ")[-1]

    # will raise ValueError if major version isn't a proper number
    return int(major)


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

__platform_binaries = {
    "darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "win": os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    "linux": "/usr/bin/google-chrome",
}

__setup_driver_old = lambda version: partial(
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
