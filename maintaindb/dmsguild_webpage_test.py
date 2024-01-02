import unittest
import logging
import sys
import random
import re
import time
import json

from dmsguild_webpage import url_2_DC
from dmsguild_webpage import DungeonCraft
from enum import Enum

class TestUrl2DC(unittest.TestCase):
    
    # Add fetchers here to avoid throttling
    @classmethod
    def setUpClass(cls):
        url = 'https://www.dmsguild.com/product/465696/SJDCRFJK0203-Colony-Calling?filters=0_0_100057_0_0_0_0_0'
        cls.dc_SJ_DC_RFJK = url_2_DC(url)
        
        url = 'https://www.dmsguild.com/product/465438/SJDCASI03-Elemental-Brainstorm?filters=0_0_100057_0_0_0_0_0'
        cls.dc_SJ_DC_ASI = url_2_DC(url)

    def test_parse_hours_str(self):
        self.assertEqual(2, TestUrl2DC.dc_SJ_DC_RFJK.hours)
        
    def test_parse_hours_int(self): 
        self.assertEqual(4, TestUrl2DC.dc_SJ_DC_ASI.hours)
        
    def test_fetch(self):
        expected = {
            "apl": 13,
            "authors": [
                "Douglas Bushong"
            ],
            "campaign": "Forgotten Realms",
            "code": "SJ-DC-DD-12",
            "date_created": "20231231",
            "hours": 4,
            "level_range": None,
            "product_id": None,
            "tiers": 3,
            "title": "SJ-DC-DD-12 The End of the Line",
            "url": "https://www.dmsguild.com/product/465468/SJDCDD12-The-End-of-the-Line?filters=0_0_100057_0_0_0_0_0"
        }
        url = 'https://www.dmsguild.com/product/465468/SJDCDD12-The-End-of-the-Line?filters=0_0_100057_0_0_0_0_0'
        dc = url_2_DC(url, product_alt='SJ-DC-DD-12 The End of the Line')
        dc_json = dc.to_json()
        for key, value in dc_json.items():
            self.assertTrue(key in expected)
            self.assertEqual(value, expected[key])
        


if __name__ == '__main__':
    unittest.main()