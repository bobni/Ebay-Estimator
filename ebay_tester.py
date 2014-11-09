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
#allow for user to search
search = raw_input("What product are you looking for? ")
url += search.replace(" ","%20")
url += "&paginationInput.entriesPerPage=10"

#check url
print url 

#connect to Ebay
response=urlopen(url)
json_obj=load(response)

#load the most recent listings matching search term
for item in json_obj['findCompletedItemsResponse'][0]['searchResult'][0]['item']:
    print item['title']

#extract all of the corresponding UPC's from the search results
allUPC = []
for item in json_obj['findCompletedItemsResponse'][0]['searchResult'][0]['item']:
    if 'productId' in item:
        allUPC.append(item['productId'][0]['__value__'])

#remove duplicate UPC's
uniqueUPC = list(set(allUPC))
for idx, item in enumerate(uniqueUPC):
    itemurl = "http://svcs.ebay.com/services/search/FindingService/v1"
    itemurl += "?OPERATION-NAME=findItemsByProduct"
    itemurl += "&SERVICE-VERSION=1.0.0"
    itemurl += "&SECURITY-APPNAME="
    itemurl += key
    itemurl += "&RESPONSE-DATA-FORMAT=JSON"
    itemurl += "&REST-PAYLOAD"
    itemurl+= "&productId.@type=ReferenceID"
    itemurl += "&productId="
    itemurl += item
    print itemurl
#search for the official names of the products
    itemresponse = urlopen(itemurl)
    item_list_json = load(itemresponse)

#print the returned products
    print idx+1, item_list_json['findItemsByProductResponse'][0]['searchResult'][0]['item'][0]['title']

#prompt the user to select the item he/she is looking for by asking for the index of the product from the previous list
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

#search for the specific product the user is looking for
productresponse = urlopen(producturl)
product_json = load(productresponse)
print "So you are looking for", product_json['findItemsByProductResponse'][0]['searchResult'][0]['item'][0]['title'][0].encode('ascii'), "?"
