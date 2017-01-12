import properties
import urllib
import json
from sku_error import SkuError


def check_online_status(sku):
    online_url = 'https://api.bestbuy.com/v1/products(sku='+str(sku)+')?apiKey='+str(properties.api_key)+ \
                 '&sort=onlineAvailability.asc&show=onlineAvailability,onlineAvailabilityText&format=json'
    response = urllib.urlopen(online_url)
    data = json.load(response)
    products = data['products']
    if len(products) != 1:
        raise SkuError(sku)
    elif products[0]['onlineAvailability'] == True and 'Shipping' in products[0]['onlineAvailabilityText']:
        return True
    else:
        return False


def check_store_status(sku):
    store_url = 'https://api.bestbuy.com/v1/stores((area(' + str(properties.zip) + ',' + str(properties.range) + \
                '))&((storeType=bigbox)))+products(sku%20in%20(' + str(sku) + '))?apiKey=' + str(properties.api_key) + \
                '&show=products.sku,products.name,products.shortDescription,products.salePrice,products' + \
                '.regularPrice,products.addToCartURL,products.url,products.image,products.' + \
                'customerReviewCount,products.customerReviewAverage,name&format=json'
    response = urllib.urlopen(store_url)
    data = json.load(response)
    print data
    stores = data['stores']
    return [store['name'] for store in stores if 'name' in store]


def get_product_name(sku):
    name_url = 'https://api.bestbuy.com/v1/products(sku=' + str(sku) + ')?apiKey=' + \
               str(properties.api_key) + '&sort=name.asc&show=name&format=json'
    response = urllib.urlopen(name_url)
    data = json.load(response)
    products = data['products']
    if len(products) != 1:
        raise SkuError(sku)
    else:
        return products[0]['name']