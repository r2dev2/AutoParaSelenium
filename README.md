# AutoParaSelenium

A library to make parallel selenium tests that automatically download and setup webdrivers

This is a WIP

## Usage

### Installation

```
pip install autoparaselenium
```

### Code

The API is very simple

```python
from autoparaselenium import configure, chrome, firefox, test, Extension

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

@test
def test_both_firefox_and_chrome(web):
    ...

@test(firefox)
def test_firefox_only(web):
    ...

@test(chrome)
def test_chrome_only(web):
    ...
```

### Running 

Use `pytest -n PROC` where `PROC` is the number of parallel threads
