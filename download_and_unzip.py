import requests
from bs4 import BeautifulSoup
import os
from io import BytesIO
from zipfile import ZipFile

url = 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx'


def get_downloadable_links():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    links = soup.findAll('a', href=True)
    downloadable_links = [link['href']
                          for link in links if link['href'].endswith('ZIP') and '/Equity/' in link['href']]
    return downloadable_links


def download_file(download_link):

    response = requests.get(download_link, stream=True)
    file_object = BytesIO(response.content)

    def extract_zip(input_zip):
        output_zip = ZipFile(input_zip)
        output_zip.extractall()
        return(output_zip.namelist()[0])

    extracted = extract_zip(file_object)
    return extracted
