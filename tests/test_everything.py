import time

from selenium import webdriver

from autoparaselenium import configure, chrome, firefox, run_on

configure(headless=False)

@run_on(chrome, firefox)
def test_both(web):
    web.get("https://stallman.org")

    expected_title = "Richard Stallman's Personal Page"
    expected_header = expected_title.replace("Page", "Site")

    assert web.title == expected_title
    assert web.find_elements_by_css_selector("h3")[0].text == expected_header
    assert False


@run_on(firefox)
def test_ff(web):
    assert isinstance(web, webdriver.Firefox)
    assert False

@run_on(chrome)
def test_chrome(web):
    assert isinstance(web, webdriver.Chrome)
    assert False
