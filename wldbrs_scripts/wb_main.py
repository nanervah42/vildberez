import re
import sqlite3
import time
from datetime import datetime
from math import ceil

import emoji
import requests
from bs4 import BeautifulSoup
from mysql_to_site import *


class WildBerries:

    def __init__(self, db, base_name, api_token, chat_name, company_name, product_type, product_type_name, p1, p2, p3, categories):
        self.db = db
        self.base_name = base_name
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.api_token = api_token
        self.chat_name = chat_name
        self.company_name = company_name
        self.product_type = product_type
        self.product_type_name = product_type_name
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.categories = categories

    def db_work(self, item_id, brand_name, goods_name, img, url, price_now, b_count, stars, flag=True):
        self.cursor.execute(f"SELECT * FROM {self.base_name} WHERE ITEM_ID={item_id};")
        sql_answer = self.cursor.fetchall()
        if sql_answer == []:
            self.cursor.execute(
                f"INSERT INTO {self.base_name} VALUES ({item_id},'{brand_name}','{goods_name}','{img}','{url}',{price_now},{price_now},{price_now}, 0);")
            self.conn.commit()
        else:
            prices = sql_answer[0]
            price_prev = prices[5]
            min_price = prices[6]
            max_price = prices[7]
            timer = prices[8]
            prcnt = 100 - int(round(((price_now * 100) / price_prev), 0))
            if price_now < price_prev and price_now < min_price:
                self.cursor.execute(
                    f"UPDATE {self.base_name} SET PRICE_NOW={price_now}, PRICE_MIN={price_now}, BRAND_NAME='{brand_name}', GOODS_NAME='{goods_name}', IMG='{img}', URL='{url}', TIMER={ceil(time.time())} WHERE ITEM_ID={item_id}")
                self.conn.commit()
                if flag:
                    self.notification(item_id, prcnt, brand_name, goods_name, img, url, price_now, price_prev,
                                      min_price,
                                      max_price, b_count, stars)
            elif price_now < price_prev and price_now >= min_price:
                self.cursor.execute(
                    f"UPDATE {self.base_name} SET PRICE_NOW={price_now}, BRAND_NAME='{brand_name}', GOODS_NAME='{goods_name}', IMG='{img}', URL='{url}', TIMER={ceil(time.time())} WHERE ITEM_ID={item_id}")
                self.conn.commit()
                if flag and (ceil(time.time()) - timer) > 864000:
                    self.notification(item_id, prcnt, brand_name, goods_name, img, url, price_now, price_prev,
                                      min_price,
                                      max_price, b_count, stars)
            elif price_now > price_prev:
                if price_now > max_price:
                    self.cursor.execute(f"UPDATE {self.base_name} SET PRICE_MAX={price_now} WHERE ITEM_ID={item_id}")
                else:
                    self.cursor.execute(
                        f"UPDATE {self.base_name} SET PRICE_NOW={price_now}, BRAND_NAME='{brand_name}', GOODS_NAME='{goods_name}', IMG='{img}', URL='{url}' WHERE ITEM_ID={item_id}")
                self.conn.commit()

    def notification(self,
                     item_id,
                     prcnt,
                     brand_name,
                     goods_name,
                     img,
                     url,
                     price_now,
                     price_prev,
                     min_price,
                     max_price,
                     b_count,
                     stars):
        if (0 < price_now <= 500 and prcnt > self.p1) or (501 < price_now <= 1000 and prcnt > self.p2) or (
                1001 < price_now and prcnt > self.p3):
            print(f'Товар:  {brand_name} / {goods_name} уменьшился в цене c {price_prev} до {price_now} (-{prcnt}%)')
            print(f'Ссылка: {url}')
            print(f'Картинка: {img}')
            requests.get(f'https://api.telegram.org/bot{self.api_token}/sendMessage', params=dict(
                parse_mode='HTML',
                chat_id=self.chat_name,
                text=f'{self.company_name}\n<a href="{img}">&#8205;</a>\n'
                     f'<a href="{url}">{brand_name} / {goods_name}</a>\n\n'
                     f'{price_prev}р -> {price_now}р <b>(-{prcnt}%)</b>\n\n'
                     f'Амплитуда: от {min_price}р до {max_price}р\n\n'
                     f'{emoji.emojize(":full_moon:") * stars}{emoji.emojize(":new_moon:") * (5 - stars)} {b_count}'))
            try:
                add_on_site(item_id, brand_name, goods_name, img, url, price_now, price_prev, min_price, max_price,
                        b_count, stars, self.company_name, self.product_type, self.product_type_name)
            except:
                print('Ошибка SQL. Запрос не выполнен.')


    def get_data_100(self, lnk):
        HEADERS = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.282'}
        response = requests.get(lnk, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div', class_='product-card j-card-item')
        for i in quotes:
            id_tmp = i.find(class_='product-card__main j-open-full-product-card').get('href')
            id_tmp2 = [m.start() for m in re.finditer('/', id_tmp)]
            item_id = int(id_tmp[id_tmp2[1] + 1:id_tmp2[2]])
            brand_name = i.find('strong', class_="brand-name").text[:-2].strip().replace("'", "`").replace('"', '`')
            goods_name = i.find('span', class_="goods-name").text.strip().replace("'", "`").replace('"', '`')
            if i.find('span', class_='lower-price') is None:
                price_now = int(''.join(j for j in i.find('ins', class_='lower-price').text if j.isdigit()))
            else:
                price_now = int(''.join(j for j in i.find('span', class_='lower-price').text if j.isdigit()))
            # price_now = int(''.join(j for j in i.find('span', class_='price-commission__current-price').text if j.isdigit()))
            url = f'https://www.wildberries.ru/catalog/{item_id}/detail.aspx'
            img_temp1 = i.find(class_='j-thumbnail thumbnail').get('data-original')
            img_temp2 = i.find(class_='j-thumbnail thumbnail').get('src')
            img = f'https:{img_temp1}' if img_temp1 else f'https:{img_temp2}'
            if i.find('span', class_='product-card__count') is None:
                b_count = 0
            else:
                b_count = int(''.join(j for j in i.find('span', class_='product-card__count').text if j.isdigit()))
            if re.findall(r'star\d', str(i)) == []:
                stars = 0
            else:
                stars = int(re.findall(r'star\d', str(i))[0][-1])
            flag = False if i.find('ins',
                                   title='Новый товар, поступил в продажу менее 14 дней назад') is not None else True
            self.db_work(item_id,
                         brand_name,
                         goods_name,
                         img,
                         url,
                         price_now,
                         b_count,
                         stars,
                         flag)
        last_page = soup.find('a', class_='pagination__next')
        return last_page

    def start(self):
        while True:
            for category in self.categories:
                pages = category[:-1]
                for i in range(1, 1001):
                    try:
                        page = pages + str(i)
                        print(str(datetime.now())[:-7], page)
                        page_cheker = self.get_data_100(page)
                        time.sleep(2)
                        if page_cheker is None:
                            print('!')
                            break
                    except Exception as err:
                        print('err: ', err)


# url = 'https://www.wildberries.ru/catalog/elektronika/avtoelektronika?sort=rate&page=1'
# get_data_100(url)