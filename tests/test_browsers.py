from pathlib import Path

import autoparaselenium.browsers.firefox as firefox
import autoparaselenium.browsers.chrome as chrome

pwd = Path.home() / ".web-drivers"

firefox.setup_driver(pwd)
chrome.setup_driver(pwd)

class web:
    firefox = firefox.get_selenium(pwd, True)
    chrome = chrome.get_selenium(pwd, True)
