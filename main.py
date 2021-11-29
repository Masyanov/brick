from typing import Text
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
import requests
from requests.api import request
import xml.etree.ElementTree as ET
import re

root = ET.Element('Товары')

lkd_color = ['Информация отсутствует']

oppp = ["Описание отсутствует!"]

all_links_index = []
dict = {}

bad_chars = ['<a>', '</a>', '<u>', '</u>', '<strong>', '<b>']

url = "https://voronezh.brick24.ru/catalog/brick/"
domen = 'https://voronezh.brick24.ru'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

ik = 0
id = 1

massiv_item_links = []
all_link_items_products = soup.find('div', class_='catalog__items-items').find_all('div', class_='catalog__item-block')
for link_id_item in all_link_items_products:
    fin_all_links_item_products = domen + link_id_item.find('a').get('href')
    massiv_item_links.append(fin_all_links_item_products)

for link_index in massiv_item_links:

    req = requests.get(link_index)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    massive_h1 = []
    dict[id] = {}

    try:
        items_pages_name_detail = soup.find('h1', class_='item-block__name').text
        rem_items_pages_name_detail = re.sub("[$|@|&|#|_|-|'|”|“|\|/|]", '', items_pages_name_detail)
        massive_h1.append(items_pages_name_detail)
    except Exception as ex:
        pass

    all_massive_img = []
    try:
        cart_img_link = soup.find_all('div', class_='detail__info')
        all_massive_img = []
        for all_cart_ijm in cart_img_link:
            f_all_cart = all_cart_ijm.find_all('div', class_='detail__specific-row')
            detail_img_link = f_all_cart
        for i in f_all_cart:
            print(i.get_text(strip=True))

            all_massive_img.append(detail_img_link)
    except Exception as e:
        pass
