from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options

from webdriver_manager.core.utils import ChromeType
# 크롬 드라이버 자동 업데이트

from webdriver_manager.chrome import ChromeDriverManager

import time

import json

url = 'https://ridibooks.com/category/bestsellers/6050?page=1'
req_header_dict = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

chrome_service = Service(ChromeDriverManager(
    chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.get(url)

time.sleep(1)

for i in range(20):
    driver.execute_script("window.scrollBy(0, " + str((i + 1) * 70) + ")")
    time.sleep(1)


html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

items = soup.select(".fig-z0an5g")

book_list = []

for e, item in enumerate(items, 1):
    book_dict = {}

    book_index = e
    book_dict['index'] = e
    book_dict['title'] = item.text
    book_url_pre = item.get('href')
    book_id = book_url_pre[7:17].replace("?", "")
    book_thumb = f"https://img.ridicdn.net/cover/{book_id}/small?dpi=xxhdpi#1"
    book_url = f"https://ridibook.com{book_url_pre}"
    book_dict['thumbs'] = book_thumb
    book_dict['url'] = book_url

    book_list.append(book_dict)


# print(book_list)
with open('ridi_rf_top60.json', 'w', encoding='utf-8') as file:
    json.dump(book_list, file, ensure_ascii=False)

driver.quit()
