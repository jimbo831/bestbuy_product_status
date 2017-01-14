import properties
import urllib
import json
import time
from instapush import App


class Product:
    def __init__(self):
        self.valid_sku = False
        self.name = ''
        self.available_online = False
        self.online_details = ''
        self.available_in_store = False
        self.stores_available = []


def check_online_status():
    page = 1
    while True:
        online_url = 'https://api.bestbuy.com/v1/products(sku%20in%20(' + properties.skus + \
                     '))?apiKey=' + str(properties.api_key) + \
                     '&sort=name.asc&show=name,sku,onlineAvailability,onlineAvailabilityText' + \
                     '&page=' + str(page) + '&format=json'
        response = urllib.urlopen(online_url)
        data = json.load(response)
        found_products = data['products']
        for found_product in found_products:
            sku = found_product['sku']
            products[sku].valid_sku = True
            products[sku].name = found_product['name']
            products[sku].available_online = (found_product['onlineAvailability'] and
                                              (not 'Backordered' in found_product['onlineAvailabilityText']
                                                and not 'Pre-order' in found_product['onlineAvailabilityText']))
            products[sku].online_details = found_product['onlineAvailabilityText']
        if page >= data['totalPages']:
            break
        else:
            page += 1
            time.sleep(1)


def check_store_status():
    page = 1
    while True:
        store_url = 'https://api.bestbuy.com/v1/stores((area(' + str(properties.zip_code) + ',' + \
                    str(properties.store_range) + '))&((storeType=bigbox)))+products(sku%20in%20(' + \
                    properties.skus + '))?apiKey=' + str(properties.api_key) + \
                    '&show=products.sku,name&page=' + str(page) + '&format=json'
        response = urllib.urlopen(store_url)
        data = json.load(response)
        stores = data['stores']
        for store in stores:
            for sku in [product['sku'] for product in store['products']]:
                products[sku].available_in_store = True
                products[sku].stores_available.append(store['name'])
        if page >= data['totalPages']:
            break
        else:
            page += 1
            time.sleep(1)


skus = [int(x) for x in properties.skus.split(',')]
products = {sku: Product() for sku in skus}
check_online_status()
check_store_status()

app = App(appid=properties.insta_app_id, secret=properties.insta_app_secret)
for sku, product in products.iteritems():
    if not product.valid_sku:
        app.notify(event_name='sku_error', trackers={'sku': str(sku)})
    if product.available_online:
        app.notify(event_name='online_product_update', trackers={'name': product.name, 'text': product.online_details})
    if product.available_in_store:
        app.notify(event_name='in-store_product_update', trackers={
            'name': product.name, 'stores': ', '.join(product.stores_available)})
