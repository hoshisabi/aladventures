import csv
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import unquote

exclude = "/search?"

def search_dmsguild(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    time.sleep(1)  # Delay for 10 seconds between requests
    response = requests.get("https://www.google.com/search", params={"q": f'{keyword} site:dmsguild.com'}, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('a')
    for result in search_results:
        url = result.get('href')
        if url and 'www.dmsguild.com' in url:
            return url
    return None

def search_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keyword = row['Code']
            dmsguild_value = row['URL']
            if dmsguild_value is not None and dmsguild_value.strip() != '':
                continue  # Skip if DMGuild column is not blank
            result = search_dmsguild(keyword)
            print(f'Keyword: {keyword}')
            if result:
                print(f'Result: {result}')
            else:
                print('No result found.')
            print('-' * 40)

# Replace 'path/to/your/csv_file.csv' with the actual path to your CSV file
#search_csv('path/to/your/csv_file.csv')

search_csv('_data/orig_adventures.csv')