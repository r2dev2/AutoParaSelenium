import time

from selenium import webdriver

from autoparaselenium import configure, chrome, firefox, run_on


configure(headless=False)

def log(*args):
    with open("log", "a+") as fout:
        print(*args, file=fout)

beg = time.time()


@run_on(chrome, firefox)
def test_both(web):
    log("Starting both", time.time() - beg)
    web.get("https://stallman.org")

    expected_title = "Richard Stallman's Personal Page"
    expected_header = expected_title.replace("Page", "Site")

    assert web.title == expected_title
    assert web.find_elements_by_css_selector("h3")[0].text == expected_header

    log("Finishing both", time.time() - beg)


@run_on(chrome, firefox)
def test_yt(web):
    log("Starting yt v1", time.time() - beg)
    web.get("https://youtube.com")
    time.sleep(3)

    expected_title = "YouTube"

    assert web.title == expected_title

    log("Finishing yt v1", time.time() - beg)


@run_on(chrome, firefox)
def test_ytv2(web):
    log("Starting yt v2", time.time() - beg)
    web.get("https://youtube.com")
    time.sleep(3)

    expected_title = "YouTube"

    assert web.title == expected_title

    log("Finishing yt v2", time.time() - beg)


@run_on(chrome, firefox)
def test_ytv3(web):
    log("Starting yt v3", time.time() - beg)
    web.get("https://youtube.com")
    time.sleep(3)

    expected_title = "YouTube"

    assert web.title == expected_title

    log("Finishing yt v3", time.time() - beg)


@run_on(firefox)
def test_ff(web):
    assert isinstance(web, webdriver.Firefox)
    assert web.current_url == "data:,"


@run_on(chrome)
def test_chrome(web):
    assert isinstance(web, webdriver.Chrome)
    assert web.current_url == "data:,"
