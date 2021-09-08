import datetime
import time
import datetime as dt
import pathlib
import json
import random


import requests
from bs4 import BeautifulSoup as bs

# typing
import typing
from bs4.element import Tag

# orm
from models import init_models

# tor features
from stem import Signal
from stem.control import Controller
import stem


# SETTINGS
URL = "https://www.avito.ru/"
FILES_ROOT_DIR_PATH = pathlib.Path.cwd() / "parsed"


# ORM SETUP
SESSION, BASE, ENGINE, Unit = init_models()


def url_fabric(page, max_price=500) -> str:
    """
    эта функция создаёт ссылку для запроса по выбранной категории с параметрами
    :param page: индекс страницы
    :param max_price: максимальная цена товара при выдаче
    :return:
    """
    url = f"https://www.avito.ru/sankt-peterburg/bytovaya_elektronika?pmax={max_price}&p={page}"
    return url


def get_current_ip():
    session = requests.session()

    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'

    # TO Request URL with SOCKS over TOR
    try:
        r = session.get('http://httpbin.org/ip')

    except Exception as e:
        print(str(e))
    else:
        print(r.text)
        return r.text


def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="abubakr1123")
        controller.signal(Signal.NEWNYM)


# script main
def main():
    page_index_counter = 1
    while True:
        current_url = url_fabric(page_index_counter)
        time.sleep(random.uniform(0, 1))

        headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}

        session = requests.Session()
        session.proxies = {}

        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'

        traceback = session.get(current_url,
                                headers=headers
                                )

        if str(traceback.status_code)[0] == "2":
            soup = bs(traceback.text, "html.parser")

            content_blocks: typing.List[Tag] = soup.find_all("div", attrs={"class": "iva-item-content-UnQQ4"})

            try:
                for block in content_blocks:
                    title = block.find("h3", attrs={"itemprop": "name"}).get_text()

                    try:
                        price = int(block.find("span", attrs={"class": "price-text-E1Y7h text-text-LurtD text-size-s-BxGpL"}).get_text()[:-2])
                    except ValueError:
                        price = 0

                    try:
                        url = URL[:-1] + block.find("a", attrs={"class": "link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes"}).attrs["href"]
                    except AttributeError:
                        url = ""

                    try:
                        places = block.find("div", attrs={"class": "geo-root-H3eWU iva-item-geo-g3iIJ"}).get_text()
                    except ValueError:
                        places = ""


                    new_unit = Unit(
                                    url=url,
                                    places=places,
                                    price=price,
                                    title=title
                                )

                    SESSION.add(new_unit)

            except Exception as ex:
                print(ex)

            page_index_counter += 1
            SESSION.commit()
            print("на данный момент спаршено:\t", len(SESSION.query(Unit).all()))

        elif traceback.status_code in [429, 403]:
            print("нас вычислил. Текаем с городу")
            renew_tor_ip()
            get_current_ip()

        else:
            break

    # except Exception as ex:
    #     renew_tor_ip()
    #     get_current_ip()


if __name__ == "__main__":
    get_current_ip()
    renew_tor_ip()
    get_current_ip()

    for i in range(20):
        try:
            main()
        except requests.exceptions.ConnectionError:
            print("случился прикол")
