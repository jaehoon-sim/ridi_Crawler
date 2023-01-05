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

a = json.loads(books)
rank = 1
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
    list_item['book']['link'] = "https://ridibooks.com/books/" + list_item['book']['bookId']

with open('ridi_rf_top60.json', 'w', encoding='utf-8') as file:
    json.dump(my_list, file, ensure_ascii=False, indent="\t")
