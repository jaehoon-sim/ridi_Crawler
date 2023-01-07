from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options

from webdriver_manager.core.utils import ChromeType
# 크롬 드라이버 자동 업데이트

from webdriver_manager.chrome import ChromeDriverManager

import time

import json

url = 'https://ridibooks.com/bestsellers/romance_fantasy_serial'
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
driver.quit()
rank = 0
books = soup.select(
    "#__next > main > section > ul.fig-1nfc3co > li > div > div.fig-jc2buj > div > h3 > a")
stars = soup.select(".fig-hm7n2o")
authors = soup.select(
    "#__next > main > section > ul.fig-1nfc3co > li > div > div.fig-jc2buj > div > div.fig-1xj8cjq > div > p.fig-bymbz1")
genres = soup.select(
    "#__next > main > section > ul.fig-1nfc3co > li > div > div.fig-jc2buj > div > div.fig-1xj8cjq > div > p.fig-xpukdh")
runtimes = soup.select(
    "#__next > main > section > ul.fig-1nfc3co > li > div > div.fig-jc2buj > div > p.fig-1dnjub6")

book_list = []
for book, star, author, genre, runtime in zip(books, stars, authors, genres, runtimes):
    book_dict = {}
    rank = rank + 1
    book_url_pre = book.get('href')
    book_id = book_url_pre[7:17].replace("?", "")
    book_thumb = f"https://img.ridicdn.net/cover/{book_id}/small?dpi=xxhdpi#1"
    book_url = f"https://ridibooks.com{book_url_pre}"
    book_star = star.text[0:3]
    book_author = author.text
    book_genre = genre.text
    book_runtime = runtime.text

    book_dict['index'] = rank
    book_dict['title'] = book.text
    book_dict['thumbs'] = book_thumb
    book_dict['url'] = book_url
    book_dict['star'] = book_star
    book_dict['author'] = book_author
    book_dict['genre'] = book_genre
    book_dict['runtime'] = book_runtime

    book_list.append(book_dict)

# for e, item in enumerate(items, 1):
#     book_dict = {}

#     book_index = e
#     book_dict['index'] = e
#     book_dict['title'] = item.text
#     book_url_pre = item.get('href')
#     book_id = book_url_pre[7:17].replace("?", "")
#     book_thumb = f"https://img.ridicdn.net/cover/{book_id}/small?dpi=xxhdpi#1"
#     book_url = f"https://ridibooks.com{book_url_pre}"
#     book_star = item.select('.fig-19ywzqz')
#     print(book_star)
#     book_dict['thumbs'] = book_thumb
#     book_dict['url'] = book_url
#     book_dict['star'] = book_star

#     book_list.append(book_dict)


# print(book_list)
with open('ridi_rf_top60.json', 'w', encoding='utf-8') as file:
    json.dump(book_list, file, ensure_ascii=False)
