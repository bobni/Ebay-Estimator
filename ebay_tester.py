from urllib2 import urlopen
from json import load, dumps
import requests

key = "yourkeyhere"

url = "http://svcs.ebay.com/services/search/FindingService/v1"
url += "?OPERATION-NAME=findCompletedItems"
url += "&SERVICE-VERSION=1.0.0"
url += "&SECURITY-APPNAME="
url += key
url += "&GLOBAL-ID=EBAY-US"
url += "&RESPONSE-DATA-FORMAT=JSON"
url += "&REST-PAYLOAD"
url += "&keywords="
#search = raw_input("What product are you looking for? ")
search = "zune 32gb"
url += search.replace(" ","%20")
url += "&paginationInput.entriesPerPage=10"

print url 
response=urlopen(url)
json_obj=load(response)
for item in json_obj['findCompletedItemsResponse'][0]['searchResult'][0]['item']:
    print item['title']

UPC = []
for item in json_obj['findCompletedItemsResponse'][0]['searchResult'][0]['item']:
    if 'productId' in item:
        UPC.append(item['productId'][0]['__value__'])

uniqueUPC = list(set(UPC))
for idx, item in enumerate(uniqueUPC):
    newurl = "http://svcs.ebay.com/services/search/FindingService/v1"
    newurl += "?OPERATION-NAME=findItemsByProduct"
    newurl += "&SERVICE-VERSION=1.0.0"
    newurl += "&SECURITY-APPNAME="
    newurl += key
    newurl += "&RESPONSE-DATA-FORMAT=JSON"
    newurl += "&REST-PAYLOAD"
    newurl+= "&productId.@type=ReferenceID"
    newurl += "&productId="
    newurl += item
    print newurl
    newresponse = urlopen(newurl)
    new_json = load(newresponse)
    print idx+1, new_json['findItemsByProductResponse'][0]['searchResult'][0]['item'][0]['title']

productId = int(raw_input("What number corresponds to the item you are looking for? "))-1

producturl = "http://svcs.ebay.com/services/search/FindingService/v1"
producturl += "?OPERATION-NAME=findItemsByProduct"
producturl += "&SERVICE-VERSION=1.0.0"
producturl += "&SECURITY-APPNAME="
producturl += key
producturl += "&RESPONSE-DATA-FORMAT=JSON"
producturl += "&REST-PAYLOAD"
producturl+= "&productId.@type=ReferenceID"
producturl += "&productId="
producturl += uniqueUPC[productId]

productresponse = urlopen(producturl)
product_json = load(productresponse)
print "So you are looking for", product_json['findItemsByProductResponse'][0]['searchResult'][0]['item'][0]['title'][0].encode('ascii'), "?"
