from pathlib import Path

import autoparaselenium.browsers.firefox as firefox
import autoparaselenium.browsers.chrome as chrome
from autoparaselenium.models import Conf, Extension

pwd = Path.home() / ".web-drivers"

firefox.setup_driver(pwd)
chrome.setup_driver(pwd)

# Assumes LiveTL repo installed in ../LiveTL/LiveTL
class web:
    firefox = firefox.get_selenium(pwd, Conf(headless=False, extensions=[
        Extension(firefox=str(Path("../LiveTL/LiveTL/dist/LiveTL-Firefox.xpi").resolve()))
    ]))
    chrome = chrome.get_selenium(pwd, Conf(headless=False, extensions=[
        Extension(chrome=str(Path("../LiveTL/LiveTL/dist/LiveTL-Chrome.zip").resolve()))
    ]))
