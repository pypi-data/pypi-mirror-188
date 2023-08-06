from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import argparse

def download_web_page(url):
    url_base = urllib.parse.urlsplit(url)._replace(path='', query='', fragment='').geturl()

    # Make a request for the HTML content of the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all the assets (images, stylesheets, and JavaScript files)
    assets = []
    for tag in soup.find_all(['img', 'script', 'link']):
        if 'src' in tag.attrs:
            assets.append(tag['src'])
        if 'href' in tag.attrs:
            assets.append(tag['href'])

    # Create the result folder if it does not exist
    if not os.path.exists('result'):
        os.makedirs('result')

    # Make a request for each asset and save it to a file
    failed = []
    for asset in tqdm(assets, bar_format='{l_bar}{bar}|{n_fmt}/{total_fmt}'):
        if not asset.startswith(('http://', 'https://')):
            asset = urllib.parse.urljoin(url_base, asset)
        try:
            asset_response = requests.get(asset)
            asset_filename = os.path.join('result', asset.split('/')[-1])
            with open(asset_filename, 'wb') as f:
                f.write(asset_response.content)
        except:
            # Catch any exceptions that may occur and add the asset to the failed list
            failed.append(asset)
            continue

    # Save the HTML content of the page to a file
    html_filename = os.path.join('result', 'index.html')
    with open(html_filename, 'wb') as f:
        f.write(response.content)

    # Print a summary of the results
    print('\nSummary:')
    print(f'{len(assets) - len(failed)}/{len(assets)} assets downloaded successfully.')
    if failed:
        print('\033[91mFailed to download the following assets:\033[0m')
        for asset in failed:
            print(asset)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download a complete web page with assets for testing.')
    parser.add_argument('url', help='The URL of the web page to download.')
    args = parser.parse_args()
    download_web_page(args.url)
