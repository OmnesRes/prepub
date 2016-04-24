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
##to ensure it is a figshare exclusive article need to see 'figshare' in the doi and citation


r=requests.get("https://api.figshare.com/v2/articles?page=1&order=published_date&order_direction=desc&page_size=1000")
if not r.ok:
    print r

for i in r.json():
    if i['url'].split('/')[-1] not in unique:
        unique[i['url'].split('/')[-1]]=''
        if 'figshare' in i['doi']:
            templinks.append(i['url'])


r=requests.get("https://api.figshare.com/v2/articles?page=1&order=modified_date&order_direction=desc&page_size=1000")
if not r.ok:
    print r

for i in r.json():
    if i['url'].split('/')[-1] not in unique:
        unique[i['url'].split('/')[-1]]=''
        if 'figshare' in i['doi']:
            templinks.append(i['url'])



for index, i in enumerate(templinks):
    r=requests.get(i)
    myjson=r.json()
    print index, i
    try:
        if 'figshare' in myjson['citation'] and 'Taylor & Francis' not in myjson['citation']:
            abstract=BeautifulSoup(myjson['description']).find('p').text.strip()
            if len(abstract)>250:
                if ' de ' not in abstract and ' el ' not in abstract and ' y ' not in abstract:
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
        

from figshare_categories import categories

if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
    f=open('figshare.txt','w')
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        if int(date.split('-')[0])>=2014:
            for j in tag:
                    if j in categories:
                        f.write(str([title,author,date,abstract,link,tag,author_af]))
                        f.write('\n')
                        break
    f.close()
else:
    print 'error'
