from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options

# 크롬 드라이버 자동 업데이트

from webdriver_manager.chrome import ChromeDriverManager

import time

import json

url = 'https://ridibooks.com/category/bestsellers/6050?page=1'
req_header_dict = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

chrome_options = Options()

chrome_options.add_experimental_option("detach", True)

service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url)

time.sleep(1)

for i in range(20):
    driver.execute_script("window.scrollBy(0, " + str((i + 1) * 70) + ")")
    time.sleep(1)


html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

items = soup.select(".fig-z0an5g")
thumbs = soup.select_one("fig-1em810c")

book_list = []

for e, item in enumerate(items, 1):
    book_dict = {}

    book_thumb = soup.select_one(
        "#__next > main > div > section > ul > li > div > div > a > div > div > img")["src"]

    book_index = e
    book_dict['index'] = e
    book_dict['title'] = item.text
    book_url = f"https://ridibook.com{item.get('href')}"
    book_dict['thumbs'] = book_thumb
    book_dict['url'] = book_url

    book_list.append(book_dict)


# print(book_list)
with open('ridi_rf_top60.json', 'w', encoding='utf-8') as file:
    json.dump(book_list, file, ensure_ascii=False)

driver.quit()
