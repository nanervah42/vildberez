import sqlite3


sqlite_connection = sqlite3.connect('wb.db')
cursor = sqlite_connection.cursor()

cursor.execute(f"SELECT * FROM main_table WHERE ITEM_ID=5952542;")
sql_answer = cursor.fetchall()
print(sql_answer)
print(sql_answer)
print(sql_answer[0][5])
print(sql_answer[0][6])
print(sql_answer[0][7])
print(sql_answer[0][8])
cursor.close()


def db_work(self, item_id, brand_name, goods_name, img, url, price_now, b_count, stars, flag=True):
    self.cursor.execute(f"SELECT ITEM_ID FROM {self.base_name} WHERE ITEM_ID={item_id};")
    if self.cursor.fetchall() == []:
        self.cursor.execute(
            f"INSERT INTO {self.base_name} VALUES ({item_id},'{brand_name}','{goods_name}','{img}','{url}',{price_now},{price_now},{price_now}, 0);")
        self.conn.commit()
    else:
        self.cursor.execute(
            f"SELECT PRICE_NOW, PRICE_MIN, PRICE_MAX, TIMER FROM {self.base_name} WHERE ITEM_ID={item_id};")
        prices = self.cursor.fetchall()[0]
        price_prev = prices[0]
        min_price = prices[1]
        max_price = prices[2]
        timer = prices[3]
        if price_now < price_prev and price_now < min_price:
            prcnt = 100 - int(round(((price_now * 100) / price_prev), 0))
            self.cursor.execute(
                f"UPDATE {self.base_name} SET PRICE_NOW={price_now}, BRAND_NAME='{brand_name}', GOODS_NAME='{goods_name}', IMG='{img}', URL='{url}', TIMER={ceil(time.time())} WHERE ITEM_ID={item_id}")
            if flag:
                self.notification(item_id, prcnt, brand_name, goods_name, img, url, price_now, price_prev, min_price,
                                  max_price, b_count, stars)
            self.conn.commit()
            self.cursor.execute(f"UPDATE {self.base_name} SET PRICE_MIN={price_now} WHERE ITEM_ID={item_id}")
            self.conn.commit()
        elif price_now < price_prev and price_now >= min_price:
            prcnt = 100 - int(round(((price_now * 100) / price_prev), 0))
            self.cursor.execute(
                f"UPDATE {self.base_name} SET PRICE_NOW={price_now}, BRAND_NAME='{brand_name}', GOODS_NAME='{goods_name}', IMG='{img}', URL='{url}', TIMER={ceil(time.time())} WHERE ITEM_ID={item_id}")
            if flag and (ceil(time.time()) - timer) > 864000:
                self.notification(item_id, prcnt, brand_name, goods_name, img, url, price_now, price_prev, min_price,
                                  max_price, b_count, stars)
            self.conn.commit()
        elif price_now > price_prev:
            self.cursor.execute(
                f"UPDATE {self.base_name} SET PRICE_NOW={price_now}, BRAND_NAME='{brand_name}', GOODS_NAME='{goods_name}', IMG='{img}', URL='{url}' WHERE ITEM_ID={item_id}")
            self.conn.commit()
            if price_now > max_price:
                self.cursor.execute(f"UPDATE {self.base_name} SET PRICE_MAX={price_now} WHERE ITEM_ID={item_id}")
                self.conn.commit()