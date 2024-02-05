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
from collections import defaultdict



from dmsguild_webpage import url_2_DC
from dmsguild_webpage import DC_CODES
from enum import Enum
import glob



logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())
input_path = os.path.join(root, '_dc')
output_path = os.path.join(root, '_stats')


def __add_to_map(data, aggregated_by_dc_code):
    if 'code' not in data:
        logger.info(f">> {data['full_title']} missing DC code")
        return
    
    dc_code = None
    for code in DC_CODES:
        if data['code'].upper().startswith(code.upper()):
            dc_code = code
            break
    
    if dc_code:
       aggregated_by_dc_code[dc_code].append(data)
            
    
def aggregate():
    
    aggregated_by_dc_code = defaultdict(list)
    for code in DC_CODES:
        aggregated_by_dc_code[code.upper()] = []
    
    logger.info(f'Reading all files at: {input_path}')
    input_full_path = f"{str(input_path)}/*.json"
    for file in glob.glob(input_full_path):
        with open(os.path.join(input_path, file), 'r') as _input:
            data = json.load(_input)
            __add_to_map(data, aggregated_by_dc_code)
    
    
    logger.info("------")
    logger.info(f'Aggregated stats:')
    for dc_season, dc_list in aggregated_by_dc_code.items():
        logger.info(f'  {dc_season} :: {len(dc_list)} DCs')
    
    
    logger.info("------")
    logger.info(f'Writting aggregated data at: {output_path}')
    for dc_season, dc_list in aggregated_by_dc_code.items():
        
        output_full_path = f"{str(output_path)}/{dc_season}.json"
        with open(output_full_path, 'w') as f:
                json.dump(dc_list, f, indent=4, sort_keys=True)



if __name__ == '__main__':
    # crawl_dc_listings(page_number=1, max_results=15)
    aggregate()
