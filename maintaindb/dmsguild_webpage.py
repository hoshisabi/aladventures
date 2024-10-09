
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import requests
import logging
import datetime
import re
import json
from word2number import w2n
import sys


logger = logging.getLogger()

DC_CAMPAIGNS = {
    'DL-DC': 'Dragonlance',
    'EB-DC': 'Eberron',
    'FR-DC': 'Forgotten Realms',
    'PS-DC': 'Forgotten Realms',
    'SJ-DC': 'Forgotten Realms',
    'WBW-DC': 'Forgotten Realms',
    'DC-POA': 'Forgotten Realms',
    'PO-BK': 'Forgotten Realms',
    'BMG-DRW': 'Forgotten Realms',
    'BMG-DL': 'Dragonlance',
    'BMG-MOON': 'Forgotten Realms',
    'BMG-DL': 'Dragonlance',
    'CCC-': 'Forgotten Realms',
    'RV-DC': 'Ravenloft',
}

DDAL_CAMPAIGN = {
    'DDAL4': ['Forgotten Realms', 'Ravenloft'],
    'DDAL04': ['Forgotten Realms', 'Ravenloft'],
    'DDEX1': ['Forgotten Realms'],
    'DDEX2': ['Forgotten Realms'],
    'DDEX3': ['Forgotten Realms'],
    'DDAL5': ['Forgotten Realms'],
    'DDAL6': ['Forgotten Realms'],
    'DDAL7': ['Forgotten Realms'],
    'DDAL8': ['Forgotten Realms'],
    'DDAL9': ['Forgotten Realms'],
    'DDAL10': ['Forgotten Realms'],
    'DDAL-DRW': ['Forgotten Realms'],
    'DDAL-ELW': ['Eberron'],
    'EB': ['Eberron'],
}

class DungeonCraft:

    def __init__(self, product_id, title, authors, code, date_created, hours, tiers, apl, level_range, url, campaign) -> None:
        self.product_id = product_id
        self.full_title = title
        self.title = self.__get_short_title(title).strip()
        self.authors = authors
        self.code = code
        self.date_created = date_created
        self.hours = hours
        self.tiers = tiers
        self.apl = apl
        self.level_range = level_range
        self.url = url
        self.campaign = campaign

    def __get_short_title(self, title):
        regex = r'[A-Z]{2,}-DC-([A-Z]{2,})([^\s]+)'
        new_title = title.replace('(', '').replace(')', '').replace(':', '')
        result = re.sub(regex, '', new_title)
        return result.strip()

    def __str__(self) -> str:
        return json.dumps(self.to_json(),  sort_keys=True, indent=2,)

    def to_json(self):
        result = dict(
            product_id=self.product_id,
            full_title=self.full_title,
            title=self.title,
            authors=self.authors,
            code=self.code,
            date_created=self.date_created.strftime('%Y%m%d'),
            hours=self.hours,
            tiers=self.tiers,
            apl=self.apl,
            level_range=self.level_range,
            url=self.url,
            campaign=self.campaign,
        )
        return result


def get_patt_first_matching_group(regex, text):
    if matches := re.search(regex, text, re.MULTILINE | re.IGNORECASE):
        for group in matches.groups():
            if group:
                return group
    return None


def __get_dc_code_and_campaign(product_title):
    content = str(product_title).upper().split()
    for text in content:
        text = text.replace(',', '').replace(
            '(', '').replace(')', '').replace("'", '').replace(':', '-')
        text = text.strip()
        if text:
            for code in DC_CAMPAIGNS:
                if text.startswith(code):
                    return (text, DC_CAMPAIGNS.get(code))
            for code in DDAL_CAMPAIGN:
                if text.startswith(code):
                    return (text, DDAL_CAMPAIGN.get(code))
    return None



def __str_to_int(value):
    if not value:
        return None

    try:
        number = int(value)
        return number
    except ValueError:
        number = w2n.word_to_num(value)
        return number
    except Exception:
        return None


def url_2_DC(input_url: str, product_id: str = None, product_alt=None) -> DungeonCraft:
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

        hours = get_patt_first_matching_group(r"(?i)(two|four|\d)+(?:hour|to|through|\+|-|\s+)*(?:(\d|two|four|eight|\s)+)*Hour", text)
        hours = __str_to_int(hours)
        tier = get_patt_first_matching_group(r"Tier ?([1-4])", text)
        tier = __str_to_int(tier)
        apl = get_patt_first_matching_group(r"APL ?(\d+)", text)
        apl = __str_to_int(apl)
        level_range = get_patt_first_matching_group(r"(?i)(?:levels ?)?(\d+)(?:nd|th)?(?:[ -]|through|to)*(\d+)(?:nd|th)?[- ](?:level)?", text)
	

        code = None
        campaign = None
        if product_alt:
            result = __get_dc_code_and_campaign(product_alt)
            if result is not None: (code, campaign) = result

        dc = DungeonCraft(product_id, module_name, authors,
                          code, date_created, hours, tier, apl, level_range, input_url, campaign)

        logger.info(f'>> {product_id} processed')
        return dc
    except Exception as ex:
        logger.error(str(ex))
        return None


if __name__ == '__main__':
    url = sys.argv[1]
    product_alt = sys.argv[2]

    dc = url_2_DC(url, product_alt=product_alt)
    print(str(dc))
