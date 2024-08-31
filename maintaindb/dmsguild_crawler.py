try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import requests
import pathlib
import os
from multiprocessing import Pool
import logging
import sys
import random
import re
import time
import json

from dmsguild_webpage import url_2_DC
from enum import Enum


logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())


THROTTLING_SLEEP_TIME_LIST = [1, 1, 3, 5, 8, 13, 21]


class CrawlerStatus(Enum):
    SUCCESS = 1,
    CACHED = 2,
    ERROR = 3


class DmsGuildProduct:
    def __init__(self, product_id, url, alt=None) -> None:
        self.product_id = product_id
        self.url = url
        self.alt = alt

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, DmsGuildProduct):
            return self.product_id == __value.product_id
        return False

    def __hash__(self):
        return hash(self.product_id)

def product_2_dungeon_craft_worker(dmsGuildProduct: DmsGuildProduct):
    try:
        sleep_time = random.choice(THROTTLING_SLEEP_TIME_LIST)
        json_output_path = os.path.join(
            root, '_dc', f'{dmsGuildProduct.product_id}.json')

        if not os.path.exists(json_output_path):
            logger.info(
                f'Fetching {dmsGuildProduct.product_id} ... in {sleep_time}s')
            time.sleep(sleep_time)
            dc_data = url_2_DC(dmsGuildProduct.url,
                               product_id=dmsGuildProduct.product_id, product_alt=dmsGuildProduct.alt)
            json_data = dc_data.to_json()
            with open(json_output_path, 'w') as f:
                json.dump(json_data, f, indent=4, sort_keys=True)
                return CrawlerStatus.SUCCESS
        else:
            logger.info(
                f'>> [CACHED] {dmsGuildProduct.product_id} already processed')
            return CrawlerStatus.CACHED
    except Exception as ex:
        logger.error(str(ex))
        return CrawlerStatus.ERROR


def get_patt_first_group(regex, text):
    if matches := re.search(regex, text, re.MULTILINE | re.IGNORECASE):
        return matches[1]
    return None


def get_product_id(node):
    children = node.findChildren("img", recursive=False)
    for child in children:
        if child.attrs and 'alt' in child.attrs:
            product_id = child.attrs['alt']
            product_str = re.sub(r"[ :-]", "_", product_id)
            product_str = re.sub(r"\W", "", product_str).replace("_", "-")
            return product_str

    return None


def get_product_alt(node):
    children = node.findChildren("img", recursive=False)
    for child in children:
        if child.attrs and 'alt' in child.attrs:
            return child.attrs['alt']

    return None


def crawl_dc_listings(base_url = "https://www.dmsguild.com/browse.php?filters=0_0_100057_0_0_0_0_0", page_number=1, max_results=None):

    product_list = set()
    url = f'{base_url}&page={page_number}&sort=4a'

    parsed_html = BeautifulSoup(requests.get(url).text, features="html.parser")

    all_product_links = parsed_html.body.find_all(
        "a", {"class": "product_listing_link"})
    for idx, product in enumerate(all_product_links):
        if product.attrs and 'href' in product.attrs:
            product_ulr = product.attrs['href']
            product_id = get_product_id(product)
            product_alt = get_product_alt(product)

            if product_id and 'bundle' not in product_id.lower() and 'roll20' not in product_id.lower():
                product_list.add(DmsGuildProduct(
                    product_id, product_ulr, alt=product_alt))

    # Trim the list down if max_results is set.
    # Useful for testing purposes.
    product_list = list(product_list)
    if max_results:
        logger.info(
            f"Trimming {len(product_list)} to max_results={max_results}")
        product_list = product_list[:max_results]

    agents = 5
    chunksize = 20
    # processes is the number of worker processes to use
    pool = Pool(processes=agents)

    # This method chops the iterable into a number of chunks which it submits to the process pool as separate tasks.
    # The (approximate) size of these chunks can be specified by setting chunksize to a positive integer.
    result = pool.map(product_2_dungeon_craft_worker, product_list, chunksize)

    success = list(filter(lambda k: k == CrawlerStatus.SUCCESS, result))
    cached = list(filter(lambda k: k == CrawlerStatus.CACHED, result))
    error = list(filter(lambda k: k == CrawlerStatus.ERROR, result))

    logger.info("------")
    logger.info(f"{len(product_list)} files processed")

    logger.info(f"  {len(success)} SUCCESS")
    logger.info(f"  {len(cached)} CACHED")
    logger.info(f"  {len(error)} ERROR")


if __name__ == '__main__':
    base_url = "https://www.dmsguild.com/browse.php?filters=1000044_0_45393_0_0_0_0_0&sort=3a&src=fid45393"
    if (len(sys.argv) > 1):
        base_url = sys.argv[1]
        print("Crawling base_url: " + base_url)

    for i in range(1, 20):
        sleep_time = random.choice(THROTTLING_SLEEP_TIME_LIST)
        crawl_dc_listings(base_url = base_url, page_number=i)
        logger.info(
                f'----------')
        logger.info(
                f'Fetching {i}-th page in {sleep_time}s')
        time.sleep(sleep_time)
