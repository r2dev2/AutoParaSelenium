# AutoParaSelenium

A library to make parallel selenium tests that automatically download and setup webdrivers

## Usage

### Installation

```
pip install autoparaselenium
```

### Code

The API is very simple

```python
from typing import Union

from selenium import webdriver

from autoparaselenium import configure, chrome, firefox, run_on, all_, Extension

# All parameters are optional, but still call it once before everything
configure(
    extensions=[
        Extension(chrome="path to chrome extension to install"),
        Extension(firefox="path to firefox extension to install"),
        Extension(chrome="chrome path", firefox="firefox path")
    ],
    headless=True, # if there are chrome extensions, chrome will not be headless as a selenium limitation
    selenium_dir="./drivers"
)

@run_on(all_)
def test_both_firefox_and_chrome(web: Union[webdriver.Firefox, webdriver.Chrome]):
    ...

@run_on(firefox)
def test_firefox_only(web: webdriver.Firefox):
    ...

@run_on(chrome)
def test_chrome_only(web: webdriver.Chrome):
    ...
```

### Running 

Use `pytest --tests-per-worker PROC` where `PROC` is the number of parallel threads

## Credits

* [pytest-parallel python3.9 support fork](https://github.com/andni233/pytest-parallel/tree/python39-support)
