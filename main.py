import properties
import product_status_check as psc
from sku_error import SkuError


sku = properties.sku
message = []
try:
    online_status = psc.check_online_status(sku)
    if online_status:
        message.append(psc.get_product_name(sku) +
                       ' is in stock online!')
except SkuError, arg:
    message.append('SKU problem with ' + str(arg))
store_status = psc.check_store_status(sku)
if len(store_status) > 0:
    message.append(psc.get_product_name(sku) +
                   ' is in stock at ' + ', '.join(store_status) + '!')
print message