import asyncio
import re
import shutil
from playwright.async_api import async_playwright
import time


class to_scrape:
    def copy_file(self,source_path, role_path):
        shutil.copy2(source_path, r'C:\Users\87373\PycharmProject1\novel')
        print('已移动到合集')

        shutil.copy2(source_path, role_path)
        print('已移动到角色合集')

    def strip(self,file_name, role_path):
        with open(fr'C:\Users\87373\PycharmProject1\utils\{file_name}.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        modified_lines = [line.lstrip() for line in lines]

        with open(fr'C:\Users\87373\PycharmProject1\utils\{file_name}.txt', 'w', encoding='utf-8') as file:
            file.writelines(modified_lines)
            print("处理完毕")

        self.copy_file(file.name, role_path)

    def clear(self,file_name,name):
        def filter_dialogue(dialogue_file, protagonist):
            qa_pairs = []
            previous_line = None

            with open(dialogue_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                for line in lines:
                    line = line.strip()

                    if protagonist in line:
                        dialogue = re.findall(r'“(.+?)”', line)
                        if dialogue:
                            if previous_line:
                                qa_pairs.append({'question': previous_line, 'answer': dialogue[0]})

                    previous_line = line

            return qa_pairs

        dialogue_file = fr'C:\Users\87373\PycharmProject1\utils\{file_name}.txt'
        protagonist = f'{name}'
        qa_pairs = filter_dialogue(dialogue_file, protagonist)

        for pair in qa_pairs:
            question = re.findall(r'“(.+?)”', pair['question'])
            answer = pair['answer']
            paragraphs = answer.split("\n")
            for str_item, list_item in zip(paragraphs, question):
                print(list_item, '  >>  ', str_item.strip())

        with open(fr'C:\Users\87373\PycharmProject1\utils\{file_name}主角对话.txt', 'w', encoding='utf-8') as file:
            for pair in qa_pairs:
                question = re.findall(r'“(.+?)”', pair['question'])
                answer = pair['answer']
                paragraphs = answer.split("\n")
                for str_item, list_item in zip(paragraphs, question):
                    file.write(str(list_item) + str('  >>  ') + str(str_item.strip() + "\n\n\n"))

    def deep_clear(self,file_name, name):
        def filter_dialogue(dialogue_file, protagonist):
            qa_pairs = []
            previous_line = None

            with open(dialogue_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                for line in lines:
                    line = line.strip()

                    if line.startswith(protagonist):
                        dialogue = re.findall(r'“(.+?)”', line)
                        if dialogue and len(" ".join(dialogue).strip()) < 30:
                            if previous_line and not previous_line.startswith(protagonist) and len(
                                    previous_line.strip()) < 30:
                                qa_pairs.append({'question': previous_line, 'answer': dialogue[0]})

                    previous_line = line

            return qa_pairs

        dialogue_file = fr'C:\Users\87373\PycharmProject1\utils\{file_name}.txt'
        protagonist = f'{name}'
        qa_pairs = filter_dialogue(dialogue_file, protagonist)

        for pair in qa_pairs:
            question = re.findall(r'“(.+?)”', pair['question'])
            answer = pair['answer']
            paragraphs = answer.split("\n")
            for str_item, list_item in zip(paragraphs, question):
                print(list_item, '  >>  ', str_item.strip())

        with open(fr'C:\Users\87373\PycharmProject1\utils\{file_name}主角对话.txt', 'w', encoding='utf-8') as file:
            for pair in qa_pairs:
                question = re.findall(r'“(.+?)”', pair['question'])
                answer = pair['answer']
                paragraphs = answer.split("\n")
                for str_item, list_item in zip(paragraphs, question):
                    file.write(str(list_item) + str('  >>  ') + str(str_item.strip() + "\n\n\n"))

    async def scrape(self,file_name, name, role, select, start, text, next, sleep, end):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()

                await page.goto(f'{start}')

                now = 0

                while True:
                    time.sleep(sleep)
                    try:
                        now += 1
                        content = await page.inner_text(f'{text}')

                        # print(content)
                        # print('--------------------', now)

                        with open(fr'C:\Users\87373\PycharmProject1\utils\{file_name}.txt', 'a',
                                  encoding='utf-8') as file:
                            file.write(content)

                        await page.click(f'{next}')
                        current_url = page.url
                        target_url = f'{end}'
                        if current_url == target_url:
                            break

                    except Exception as e:
                        print("ERROR:", e)
                        await page.reload()

                await browser.close()

        except Exception as e:
            print(e)

        if role == 0:
            role_path = r'C:\Users\87373\Desktop\对话\novel\yujie'

        elif role == 1:
            role_path = r'C:\Users\87373\Desktop\对话\novel\luoli'

        elif role == 2:
            role_path = r'C:\Users\87373\Desktop\对话\novel\zhanv'

        else:
            role_path = r'C:\Users\87373\Desktop\对话\novel\gaoxiaonan'

        self.strip(file_name, role_path)

        if select == 0:
            self.clear(file_name, name)
        elif select == 1:
            self.deep_clear(file_name,name)
        else:
            print('未清洗!')

    async def main(self):
        i = int(input('爬取次数'))
        tasks = []
        for _ in range(i):
            loop = asyncio.get_event_loop()
            file_name = await loop.run_in_executor(None, input, '书名：')
            name = await loop.run_in_executor(None, input, '角色名：')
            role = await loop.run_in_executor(None, input, '角色类型(0御姐 1萝莉 2渣女 3搞笑男)：')
            select = int(await loop.run_in_executor(None, input, '清洗类型(0普通清洗 1深度清洗)：'))
            start = await loop.run_in_executor(None, input, '起始网址：')
            text = await loop.run_in_executor(None, input, '内容：')
            next = await loop.run_in_executor(None, input, '下一页：')
            sleep = float(await loop.run_in_executor(None, input, '间隔时长：'))
            end = await loop.run_in_executor(None, input, '结束网址：')
            parameters = [
                (file_name, name, role, select, start, text, next, sleep, end)
            ]
            for params in parameters:
                task = asyncio.create_task(self.scrape(*params))
                tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    instance = to_scrape()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(instance.main())




