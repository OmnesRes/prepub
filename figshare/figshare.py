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
##can only get 1000 articles at a time
##will use different ordering schemes to get as many articles as possible

r=requests.get("https://api.figshare.com/v2/articles?page=1&order=published_date&order_direction=asc&page_size=1000")
if not r.ok:
    print r

for i in r.json():
    if i['doi'] not in unique:
        unique[i['doi']]=''
        templinks.append(i['url'])


r=requests.get("https://api.figshare.com/v2/articles?page=1&order=published_date&order_direction=desc&page_size=1000")
if not r.ok:
    print r

for i in r.json():
    if i['doi'] not in unique:
        unique[i['doi']]=''
        templinks.append(i['url'])

r=requests.get("https://api.figshare.com/v2/articles?page=1&order=modified_date&order_direction=asc&page_size=1000")
if not r.ok:
    print r

for i in r.json():
    if i['doi'] not in unique:
        unique[i['doi']]=''
        templinks.append(i['url'])

r=requests.get("https://api.figshare.com/v2/articles?page=1&order=modified_date&order_direction=desc&page_size=1000")
if not r.ok:
    print r

for i in r.json():
    if i['doi'] not in unique:
        unique[i['doi']]=''
        templinks.append(i['url'])



for index, i in enumerate(templinks):
    r=requests.get(i)
    myjson=r.json()
    print index, i
    try:
        abstract=BeautifulSoup(myjson['description']).find('p').text.strip()
        date=myjson['created_date'].strip()
        link=myjson['figshare_url'].strip()
        title=myjson['title'].strip()
        temp=[]
        for j in myjson['categories']:
            temp.append(j['title'].replace(' not elsewhere classified',''))
        tag=temp
        temp=[]
        for j in myjson['authors']:
            temp.append(unicodedata.normalize('NFKD',j['full_name']).encode('ascii','ignore'))
        author=temp
        
        author_aff.append([])
        abstracts.append(abstract)
        dates.append(date)
        links.append(link)
        tags.append(tag)
        authors.append(author)
        titles.append(title)
    except:
        pass
        


if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
    f=open('figshare.txt','w')
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        f.write(str([title,author,date,abstract,link,tag,author_af]))
        f.write('\n')
    f.close()
else:
    print 'error'
