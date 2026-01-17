from playwright.sync_api import sync_playwright
import random


def on_response(response):
    url = response.url

    # 一级评论
    if 'aweme/v1/web/comment/list/' in url and 'reply' not in url:
        data = response.json()
        for i in range(len(data["comments"])):
            print(data["comments"][i]["text"])

    # 回复
    if 'aweme/v1/web/comment/list/reply/' in url:
        data = response.json()
        for i in range(len(data["comments"])):
            print(data["comments"][i]["text"])

def main(url):
    with sync_playwright() as p:
        # 绕过自动化检测
        browser = p.chromium.launch(headless=False,args=["--start-maximized", "--disable-blink-features=AutomationControlled", "--lang=zh-CN"])
        context = browser.new_context(no_viewport=True,storage_state="dy.json")

        # 监听响应
        context.on("response", on_response)

        # 选择地址
        page = context.new_page()
        page.goto(f'{url}')
        page.wait_for_timeout(2000)
        page.click('xpath=//button[@class="semi-button semi-button-primary k_berzeZ"]')
        page.wait_for_timeout(2000)
        page.click('xpath=//div[@class="I6U7FiE8"]/div[@class="zqe4B9aR WU6dkKao"]/div[3]')

        # 移动鼠标
        page.mouse.move(1300, 650)
        page.wait_for_timeout(1000)

        # 循环抓取
        factor = ''
        while True:
            context = page.locator('xpath=//div[@data-e2e="comment-list"]/div[last()-1]').text_content()
            if factor == context:
                break
            else:
                factor = context
            while True:
                expand = page.locator('xpath=//div[@data-e2e="comment-list"]//span[contains(text(),"展开")]').first
                expand.click()
                page.wait_for_timeout(1000)
                if expand.count() == 0:
                    break

            page.wait_for_timeout(2000)
            page.mouse.wheel(0, random.randint(3000,5000))

        input('enter')

if __name__ == '__main__':
    main('你准备的视频地址')
