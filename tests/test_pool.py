from pathlib import Path

import autoparaselenium as aps
from autoparaselenium import firefox, chrome, configure

pwd = str(Path.home() / ".web-drivers")

configure(selenium_dir=pwd, headless=False)

pool = aps._browser_pool
