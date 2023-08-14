import asyncio
import time

start_time=time.time()
from playwright.async_api import async_playwright
async def scrape_novel():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('程序开始的网址')

        now=0

        # page.set_default_timeout(30000)
        while True:
            try:
                now += 1
                content = await page.inner_text('爬取的标签内容地址')

                print(content)
                print('--------------------',now)

                with open('请输入你所要保存的文件名','a',encoding='utf-8')as file:
                    file.write(content)

                await page.click('请输入有关跳转网页的标签地址')
                current_url = page.url
                target_url = '程序终止的网址'
                if current_url == target_url:
                    break

            except Exception as e:
                print("ERROR:",e)
                await page.reload()


        await browser.close()

asyncio.run(scrape_novel())

end_time=time.time()
execution_time = end_time-start_time
print("程序执行了:",execution_time,'秒')