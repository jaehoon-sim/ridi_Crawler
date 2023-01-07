import requests
from bs4 import BeautifulSoup
import json

url = 'https://ridibooks.com/category/bestsellers/6050?page=1'
req_header_dict = {
    # 요청헤더 : 브라우저정보
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
res = requests.get(url, headers=req_header_dict)
rost = []
html = res.text

soup = BeautifulSoup(html, 'html.parser')

books = soup.select_one("#__NEXT_DATA__")
books = books.text

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

book_list.append(a)

with open('ridi_rf_top60.json', 'w', encoding='utf-8') as file:
    json.dump(book_list, file, ensure_ascii=False, indent="\t")

with open('ridi_rf_top60.json', 'rt', encoding='UTF8') as f:
    # Load the JSON data into a Python dictionary
    data = json.load(f)

# Extract the list from the dictionary
my_list = data[0]["props"]["pageProps"]["dehydratedState"]["queries"][2]["state"]["data"]
# print(len(my_list))
for list_item in my_list:
    list_item['book']['rank'] = rank
    rank = rank + 1
    list_item['book']['link'] = "https://ridibooks.com/books/" + \
        list_item['book']['bookId']

with open('ridi_rf_top60.json', 'w', encoding='utf-8') as file:
    json.dump(my_list, file, ensure_ascii=False, indent="\t")
