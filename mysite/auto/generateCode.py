from playwright import sync_playwright

def run(playwright):
    """
    python -m playwright codegen
    Playwright can record user interactions in a browser and generate code.

    :param playwright:
    """
    browser = playwright.chromium.launch(headless=False)
    context = browser.newContext()

    # Open new page
    page = context.newPage()

    # Go to http://ssa.jd.com/sso/login?ReturnUrl=http://erp.jd.com/
    page.goto("http://ssa.jd.com/sso/login?ReturnUrl=http://erp.jd.com/")

    # Click input[name="username"]
    page.click("input[name=\"username\"]")

    # Fill input[name="username"]
    page.fill("input[name=\"username\"]", "yangpan23")

    # Fill input[name="password"]
    page.fill("input[name=\"password\"]", "Jetty@192.168")

    # Go to http://ssa.jd.com/sso/fp/register?returnUrl=http://erp.jd.com/
    page.goto("http://ssa.jd.com/sso/fp/register?returnUrl=http://erp.jd.com/")

    # Go to http://erp.jd.com/
    page.goto("http://erp.jd.com/")

    # Click text="领免费书"
    with page.expect_popup() as popup_info:
        page.click("text=\"领免费书\"")
    page1 = popup_info.value

    # Click text="免费领取"
    page1.click("text=\"免费领取\"")

    # Close page
    page1.close()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

