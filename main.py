import bs4
import requests
import logging
import collections
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')


ParserResult = collections.namedtuple(
    'ParseResult',
    (
        'url',
        'goods_name',
        'price',
    ),
)

HEADERS = (
    'Ссылка',
    'Наименование',
    'Цена',
)


class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {


        'user-agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 96.0.4664.45 Safari / 537.36'
        }

        self.result = []

    def load_page(self):
        url = 'https://voronezh.brick24.ru/catalog/brick/filter/clear/apply/?PAGEN_31=2&SIZEN_31=21'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.catalog__item-block.item-block.js-catalog-item.item-block--in-stock')
        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):
        # logger.info(block)
        # logger.info('=' * 100)

        url_block = block.select_one('a')
        if not url_block:
            logger.error('no url')
            return

        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return

        name_block = block.select_one('div.item-block__name')
        if not name_block:
            logger.error('no name on {url}')
            return

        price_block = block.select_one('div.item-block__price')
        if not price_block:
            logger.error('no price on {url}')
            return



        self.result.append(ParserResult(
            url=url,
            goods_name=name_block,
            price=price_block,
        ))

        logger.debug('%s, %s, %s', url, name_block, price_block)
        logger.debug('-' * 100)

    def save_results(self):
        path = '/Users/Masyanov/PycharmProjects/django/brick/test.csv'
        with open(path, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)


    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        logger.info(f'получили {len(self.result)} элемент')
        self.save_results()

if __name__ == '__main__':
    parser = Client()
    parser.run()