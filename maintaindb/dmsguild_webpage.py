
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import requests
import logging
import datetime
import re
import json


logger = logging.getLogger()



class DungeonCraft:

    def __init__(self, product_id, title, authors, code, date_created, hours, tiers, apl, level_range, url) -> None:
        self.product_id = product_id
        self.title = title
        self.authors = authors
        self.code = code
        self.date_created = date_created
        self.hours = hours
        self.tiers = tiers
        self.apl = apl
        self.level_range = level_range
        self.url = url

    def __str__(self) -> str:
        return json.dumps(self.to_json(),  sort_keys=True, indent=2,)

    def to_json(self):
        result = dict(
            product_id=self.product_id,
            title=self.title,
            authors=self.authors,
            code=self.code,
            date_created=self.date_created.strftime('%Y%m%d'),
            hours=self.hours,
            tiers=self.tiers,
            apl=self.apl,
            level_range=self.level_range,
            url = self.url
        )
        return result


def get_patt_first_group(regex, text):
    if matches := re.search(regex, text, re.MULTILINE | re.IGNORECASE):
        return matches[1]
    return None


def url_2_DC(input_url: str, product_id: str = None) -> DungeonCraft:
    try:
        parsed_html = BeautifulSoup(requests.get(
            input_url).text, features="html.parser")

        module_name = None
        product_title = parsed_html.body.find(
            "div", {"class": "grid_12 product-title"})
        children = product_title.findChildren(
            "span", {"itemprop": "name"}, recursive=True)
        for child in children:
            module_name = child.text
            break

        authors = []
        product_from = parsed_html.body.find(
            "div", {"class": "grid_12 product-from"})
        children = product_from.findChildren("a", recursive=True)
        for child in children:
            current_author = child.text
            authors.append(current_author)

        date_created = None
        children = parsed_html.body.find_all(
            "div", {"class": "widget-information-item-content"})
        key = 'This title was added to our catalog on '
        for child in children:
            if key in child.text:
                date_str = child.text.replace(key, '').replace('.', '')
                date_created = datetime.datetime.strptime(
                    date_str.strip(), "%B %d, %Y").date()
                break

        product_content = parsed_html.body.find(
            "div", {"class": "alpha omega prod-content"})
        text = product_content.text

        hours = get_patt_first_group(r"([0-9-]+|(two|four))[ -]hour", text)
        tier = get_patt_first_group(r"Tier ?([1-4])", text)
        apl = get_patt_first_group(r"APL ?(\d+)", text)
        level_range = get_patt_first_group(r"Levels (\d+ ?-\d+)", text)

        dc = DungeonCraft(product_id, module_name, authors,
                          None, date_created, hours, tier, apl, level_range, input_url)
        logger.info(f'>> {product_id} processed')
        return dc
    except Exception as ex:
        logger.error(str(ex))
        return None

