import properties
import urllib
import json


class Product:
    def __init__(self):
        self.valid_sku = False
        self.name = ''
        self.available_online = False
        self.online_details = ''
        self.available_in_store = False
        self.stores_available = []

    def __str__(self):
        return str(json.dumps(self.__dict__))

    def __repr__(self):
        return str(json.dumps(self.__dict__))


def check_online_status():
    online_url = 'https://api.bestbuy.com/v1/products(sku%20in%20(' + properties.skus + \
                 '))?apiKey=' + str(properties.api_key) + \
                 '&sort=name.asc&show=name,sku,onlineAvailability,onlineAvailabilityText' + \
                 '&format=json'
    response = urllib.urlopen(online_url)
    data = json.load(response)
    found_products = data['products']
    for found_product in found_products:
        sku = found_product['sku']
        products[sku].valid_sku = True
        products[sku].name = found_product['name']
        products[sku].available_online = (found_product['onlineAvailability'] and
                                          'Shipping' in found_product['onlineAvailabilityText'])
        products[sku].online_details = found_product['onlineAvailabilityText']


def check_store_status():
    store_url = 'https://api.bestbuy.com/v1/stores((area(' + str(properties.zip_code) + ',' + \
                str(properties.store_range) + '))&((storeType=bigbox)))+products(sku%20in%20(' + \
                properties.skus + '))?apiKey=' + str(properties.api_key) + \
                '&show=products.sku,name&format=json'
    response = urllib.urlopen(store_url)
    data = json.load(response)
    print data
    stores = data['stores']
    for store in stores:
        for sku in [product['sku'] for product in store['products']]:
            products[sku].available_in_store = True
            products[sku].stores_available.append(store['name'])


skus = [int(x) for x in properties.skus.split(',')]
products = {sku: Product() for sku in skus}
check_online_status()
check_store_status()
print products


# message = []
# try:
#     online_status = check_online_status(properties.skus)
#     if online_status:
#         message.append(psc.get_product_name(sku) +
#                        ' is in stock online!')
# except SkuError, arg:
#     message.append('SKU problem with ' + str(arg))
# store_status = check_store_status(properties.skus)
# if len(store_status) > 0:
#     message.append(psc.get_product_name(sku) +
#                    ' is in stock at ' + ', '.join(store_status) + '!')
# print message

