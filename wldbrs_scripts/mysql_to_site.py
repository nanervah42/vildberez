import mysql.connector

database_mysql = 'wb_base'
host_mysql = 'localhost'
port_mysql = '3306'
user_name_mysql = 'user'
user_password_mysql = 'password'
tablename = 'html_site_wb_base'


def add_on_site(item_id, brand_name, goods_name, img, url, price_now, price_prev, price_min, price_max,
                b_count, stars, company_name, product_type):
    def connect_db():
        connection = mysql.connector.connect(
            host=host_mysql,
            port=port_mysql,
            user=user_name_mysql,
            passwd=user_password_mysql,
            database=database_mysql
        )
        return connection

    def execute_db(query):
        connection = connect_db()
        print("Connected...")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Query successfully")

    def read_db(query):
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    tmp = read_db(
        f"""
        SELECT * FROM {tablename}
        WHERE item_id = {item_id}
        """
    )

    if tmp == []:
        execute_db(
            f"""
            INSERT INTO
                {tablename} (item_id, brand_name, goods_name, img, url, price_now, price_prev, price_min, 
                                   price_max, b_count, stars, company_name, product_type, updated_time)
            VALUES
                ({item_id}, '{brand_name}', '{goods_name}', '{img}', '{url}', {price_now}, {price_prev}, {price_min}, 
                {price_max}, {b_count}, {stars}, '{company_name}', '{product_type}', now())
            """
        )
        print('Inserting...')
    else:
        execute_db(
            f"""
                    UPDATE {tablename}
                        SET brand_name = '{brand_name}',
                            goods_name = '{goods_name}',
                            img = '{img}',
                            url = '{url}',
                            price_now = {price_now},
                            price_prev = {price_prev},
                            price_min = {price_min},
                            price_max = {price_max},
                            b_count = {b_count},
                            stars = {stars},
                            company_name = '{company_name}',
                            product_type = '{product_type}',
                            updated_time = now()
                    WHERE item_id = {item_id}
            """
        )
        print('Updating...')


add_on_site(114, 'brand', 'goods', 'www.img.ru', 'www.url.ru', 100, 110, 50, 200, 555, 4, 'wildberries', 'shoes_m')
