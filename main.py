import requests
from bs4 import BeautifulSoup
import json

url = 'https://api.ridibooks.com/v2/bestsellers?category_includes=6050&period=DAILY&limit=100'

res = requests.get(url)

data = json.loads(res.text)

my_data = data['data']['items']

rank = 1

for list_item in my_data:
    list_item['book']['rank'] = rank
    rank = rank + 1
    list_item['book']['link'] = "https://ridibooks.com/books/" + \
        list_item['book']['book_id']

with open('ridi.json', 'w', encoding='utf-8') as file:
    json.dump(my_data, file, ensure_ascii=False, indent="\t")

# rank = 1
# book_list = []

# book_list.append(a)

# with open('ridi_rf_top60.json', 'w', encoding='utf-8') as file:
#     json.dump(book_list, file, ensure_ascii=False, indent="\t")

# with open('ridi_rf_top60.json', 'rt', encoding='UTF8') as f:
#     # Load the JSON data into a Python dictionary
#     data = json.load(f)

# # Extract the list from the dictionary
# my_list = data[0]["props"]["pageProps"]["dehydratedState"]["queries"][2]["state"]["data"]
# # print(len(my_list))
# for list_item in my_list:
#     list_item['book']['rank'] = rank
#     rank = rank + 1
#     list_item['book']['link'] = "https://ridibooks.com/books/" + \
#         list_item['book']['bookId']

# with open('ridi_rf_top60.json', 'w', encoding='utf-8') as file:
#     json.dump(my_list, file, ensure_ascii=False, indent="\t")
