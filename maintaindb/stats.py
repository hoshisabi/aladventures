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
import glob
import datetime
from collections import defaultdict

from dmsguild_webpage import url_2_DC
from dmsguild_webpage import DC_CAMPAIGNS
from enum import Enum
import glob

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())
input_path = os.path.join(root, '_stats')


def convert_date_to_readable_str(dc):
    if 'date_created' in dc and dc['date_created'] is not None:
        date_obj = datetime.datetime.strptime(dc['date_created'], "%Y%m%d")
        return date_obj.strftime("%Y, %b")
    return 'Unknown'


def is_tier(dc, tier):
    if 'tiers' in dc and dc['tiers'] is not None:
        return dc['tiers'] == tier
    return False


def is_tier_unknown(dc):
    if 'tiers' in dc and dc['tiers'] is None:
        return True
    return False


def is_hour(dc, hour):
    if 'hours' in dc and dc['hours'] is not None:
        return dc['hours'] == hour
    return False


def is_hour_unknown(dc):
    if 'hours' in dc and dc['hours'] is None:
        return True
    return False


def __get_dc_per_month(data):
    result = defaultdict(list)
    for dc in data:
        month = convert_date_to_readable_str(dc)
        result[month].append(dc)
    return result


def __sort_formatted_dates(dates):
    def sort_key(date_str):
        year, month_str = date_str.split(", ")
        month_num = datetime.datetime.strptime(month_str, "%b").month  # Convert month name to number
        return year, month_num

    return sorted(dates, key=sort_key)


def summarize(data, dc_season):
    logger.info(f"")
    logger.info(f"Stats for {dc_season}")
    logger.info(f"\nDC count {len(data)}")

    logger.info(f"\nTier split")
    t1_dcs = list(filter(lambda k: is_tier(k, 1), data))
    t2_dcs = list(filter(lambda k: is_tier(k, 2), data))
    t3_dcs = list(filter(lambda k: is_tier(k, 3), data))
    t4_dcs = list(filter(lambda k: is_tier(k, 4), data))
    tier_unknown = list(filter(lambda k: is_tier_unknown(k), data))

    logger.info(f"    t1={len(t1_dcs)}")
    logger.info(f"    t2={len(t2_dcs)}")
    logger.info(f"    t3={len(t3_dcs)}")
    logger.info(f"    t4={len(t3_dcs)}")
    logger.info(f"    ??={len(tier_unknown)}")

    logger.info(f"\nHour split")
    h2_dcs = list(filter(lambda k: is_hour(k, 2), data))
    h4_dcs = list(filter(lambda k: is_hour(k, 4), data))
    hour_unknown = list(filter(lambda k: is_hour_unknown(k), data))

    logger.info(f"    2h={len(h2_dcs)}")
    logger.info(f"    4h={len(h4_dcs)}")
    logger.info(f"    ??={len(hour_unknown)}")

    logger.info(f"\nTime split (grouped by month)")
    dc_per_month = __get_dc_per_month(data)

    for month in __sort_formatted_dates(dc_per_month.keys()):
        logger.info(f"    {month} =\t{len(dc_per_month[month])}")


input_season = 'SJ-DC'

if __name__ == '__main__':

    for dc_season in DC_CAMPAIGNS.keys():
        # TODO: add flag
        if input_season == dc_season:
            output_full_path = f"{str(input_path)}/{dc_season}.json"
            with open(output_full_path) as f:
                data = json.load(f)

                summarize(data, dc_season)
    # crawl_dc_listings(page_number=2, max_results=15)
