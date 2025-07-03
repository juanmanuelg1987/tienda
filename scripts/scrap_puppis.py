import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = 'https://www.puppis.com.ar'
CATALOG_URL = BASE_URL + '/alimentos-para-perros?PS=48&O=OrderByReleaseDateDESC'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Puedes cambiar la URL para otras categorías o "alimentos-para-gatos", etc.


def get_product_links(catalog_url):
    links = []
    page = 1
    while True:
        url = f'{catalog_url}&PageNumber={page}'
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('a.product-item__name')
        if not items:
            break
        for a in items:
            href = a.get('href')
            if href and href.startswith('/'):
                links.append(BASE_URL + href)
        page += 1
        time.sleep(1)  # Para no saturar el sitio
    return links


def get_product_data(product_url):
    resp = requests.get(product_url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    name = soup.select_one('.productName').get_text(strip=True) if soup.select_one('.productName') else ''
    desc = soup.select_one('.productDescription').get_text(strip=True) if soup.select_one('.productDescription') else ''
    price = soup.select_one('.skuBestPrice').get_text(strip=True).replace('$','').replace('.','').replace(',','.') if soup.select_one('.skuBestPrice') else ''
    img = soup.select_one('.productImage img')
    img_url = img.get('src') if img else ''
    category = 'perro' if 'perro' in product_url else 'gato' if 'gato' in product_url else ''
    return {
        'name': name,
        'description': desc,
        'price': price,
        'image_url': img_url,
        'category': category,
        'source_url': product_url
    }


def main():
    links = get_product_links(CATALOG_URL)
    print(f'Total productos encontrados: {len(links)}')
    with open('productos_puppis.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'description', 'price', 'image_url', 'category', 'source_url'])
        writer.writeheader()
        for i, url in enumerate(links):
            try:
                data = get_product_data(url)
                writer.writerow(data)
                print(f'[{i+1}/{len(links)}] {data["name"]}')
                time.sleep(0.5)
            except Exception as e:
                print(f'Error en {url}: {e}')

if __name__ == '__main__':
    main()
