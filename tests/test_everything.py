import time

from selenium import webdriver

from autoparaselenium import configure, chrome, firefox, test

configure(headless=False)

@test
def test_both(web):
    web.get("https://stallman.org")

    expected_title = "Richard Stallman's Personal Page"
    expected_header = expected_title.replace("Page", "Site")

    assert web.title == expected_title
    assert web.find_elements_by_css_selector("h3")[0].text == expected_header


@test(firefox)
def test_ff(web):
    assert isinstance(web, webdriver.Firefox)

@test(chrome)
def test_chrome(web):
    assert isinstance(web, webdriver.Chrome)
