import requests
from bs4 import BeautifulSoup
import glob
import os

url = 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx'


def check_if_most_recent_file_available(name):
    try:
        file_list_available = glob.glob('downloads/*')
        file_name_available = max(file_list_available, key=os.path.getctime)
        if file_name_available == ''.join(['downloads/', name]):
            return True
        else:
            return False
    except:
        return False


def get_downloadable_links():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    links = soup.findAll('a', href=True)
    downloadable_links = [link['href']
                          for link in links if link['href'].endswith('ZIP') and '/Equity/' in link['href']]
    return downloadable_links


def download_file(download_link):
    file_name = download_link.split('/')[-1]

    if not check_if_most_recent_file_available(file_name):
        print(f'Downloading file {file_name}')
        try:
            response = requests.get(download_link, stream=True)
            download_file_location = './downloads/'

            with open(f'{download_file_location}{file_name}', 'wb') as f:
                for file_bits in response.iter_content(chunk_size=1024*1024):
                    if file_bits:
                        f.write(file_bits)

            print(f'{file_name} Downloaded!')
        except:
            print('Disconnected. Please check your connection')
    else:
        print("Latest Copy Already Availabe")


try:
    download_zip_file = get_downloadable_links()
    download_file(download_zip_file[0])

except:
    print('Files could not be downloaded. Check internet connection')
