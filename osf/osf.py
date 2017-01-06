##currently not indexing OSF, this may change in the future


import time
import requests
import unicodedata
import re
from bs4 import BeautifulSoup
titles=[]
authors=[]
dates=[]
abstracts=[]
links=[]
tags=[]
author_aff=[]
templinks=[]
unique={}
##don't know upper limit for the size
##use this API call
r=requests.get('https://share.osf.io/api/v2/search/creativeworks/_search?q=(types.raw:"preprint") AND (sources.raw:"OSF")&order=date_created&size=100&from=0')
if not r.ok:
    print r

for i in r.json()['hits']['hits']:
    print i['_source']['title']
    print

##    for j in i['_source']:
##        print j,'\t',i['_source'][]

