from random import choice

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # pip install fake-useragent


def get_proxy():
    html_link = 'https://free-proxy-list.net/'
    response = requests.get(html_link)
    soup = BeautifulSoup(response.text, 'lxml')
    trs = soup.find('table', class_="table table-striped table-bordered").find_all('tr')[1:]
    proxies = []
    for tr in trs:
        try:
            tds = tr.find_all('td')
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            protocol = 'https' if 'yes' in tds[6].text.strip() else 'http'
            checker_tmp = tds[7].text.strip()
            if 'secs' in checker_tmp:
                checker = True
            else:
                if int(checker_tmp[:2].strip()) <= 5:
                    checker = True
                else:
                    checker = False
            if checker == True and protocol == 'http':
                proxies.append((protocol, f'{ip}:{port}'))
        except:
            pass
    return choice(proxies)


def get_UA():
    ua = UserAgent()
    return ua.random


print(get_UA())
print(get_proxy())
