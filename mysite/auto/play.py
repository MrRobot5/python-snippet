from playwright import sync_playwright

with sync_playwright() as p:
    # for browser_type in [p.chromium, p.firefox, p.webkit]:
    browser = p.chromium.launch(headless=False)
    page = browser.newPage()
    page.goto('https://www.tuicool.com/a/')
    page.type("input[name=email]", "1050335971@qq.com")
    page.type("input[name=password]", "tt654321")
    page.click("button[type=submit]")
    page.waitForSelector("span[class=badge]")
    page.screenshot(path=f'example-chromium.png')
    browser.close()


