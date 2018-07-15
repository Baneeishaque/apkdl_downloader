import sys

import requests

# try:
#     from urllib.parse import quote_plus
# except ImportError:
#     from urlparse import quote_plus
try:
    from urllib import quote_plus  # Python 2.X
except ImportError:
    from urllib.parse import quote_plus  # Python 3+
from bs4 import BeautifulSoup

APPS = []


def search(given_query):
    res = requests.get('https://apkpure.com/search?q={}&region='.format(quote_plus(given_query)), headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5'
    }).text
    soup = BeautifulSoup(res, "html.parser")
    for i in soup.find('div', {'id': 'search-res'}).findAll('dl', {'class': 'search-dl'}):
        app = i.find('p', {'class': 'search-title'}).find('a')
        APPS.append((app.text,
                     i.findAll('p')[1].find('a').text,
                     'https://apkpure.com' + app['href']))


def download(link):
    res = requests.get(link + '/download?from=details', headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5'
    }).text
    soup = BeautifulSoup(res, "html.parser").find('a', {'id': 'download_link'})
    if soup['href']:
        r = requests.get(soup['href'], stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5'
        })
        with open(link.split('/')[-1] + '.apk', 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

if len(sys.argv) > 1:
    search(" ".join(sys.argv[1:]))
    if len(APPS) > 0:
        print('Downloading {}.apk ...'.format(APPS[00][2].split('/')[-1]))
        download(APPS[00][2])
        print('Download completed!')
    else:
        print('No results')
else:
    print('Missing apk package name')
    print('apkdl_downloader apk_package_name')
