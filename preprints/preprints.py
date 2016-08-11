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

##get all articles

categories=['biology','medicine_pharmacology','life_sciences']

base='http://preprints.org/subject/browse/'

for cat in categories:
    index=1
    print cat
    templinks=[]
    tempdates=[]
    tempabstracts=[]
    tempauthors=[]
    temptags=[]
    while True:
        print index
        r=requests.get(base+cat+'?page_num='+str(index)+'&page_length=100')
        print r.ok
        count=0
        soup=BeautifulSoup(r.content,'html.parser')
        for i in soup.find_all("a", {'class':'title'}):
            templinks.append(i.get('href'))
        templinks=templinks[:-1]
        for i in soup.find_all('div',{'class','search-content-box'}):
            tempdate=i.find('div',{'class','show-for-large-up'}).text.strip().split('Online: ')[1].split(' (')[0].strip().split()
            tempdates.append(tempdate[1]+' '+tempdate[0]+' '+tempdate[2])
            count+=1
        for i in soup.find_all('div',{'class','abstract-content'}):
            tempabstracts.append(i.text)
        for i in soup.find_all('div',{'class','search-content-box-author'}):
            tempauthors.append([unicodedata.normalize('NFKD',j.text).encode('ascii','ignore') for j in i.find_all('a')])
        for i in soup.find_all('div',{'class','search-content-box'}):
            temptags.append([i.find_all('div')[4].text.strip().split(', ')[1].split(';')[0].strip()])
        if count==100:
            index+=1
        else:
            break

    for i,j,k,l,m in zip(templinks,tempdates,tempabstracts,tempauthors,temptags):
        if 'manuscript' in i:
            print i
            r=requests.get('http://preprints.org'+i)
            soup=BeautifulSoup(r.content,'html.parser')
            if soup.find('span',{'class','type-span'}).text in ['Review','Article']:
                dates.append(j)
                titles.append(soup.find('h1').text.strip())
                abstracts.append(k)
                links.append(i)
                authors.append(l)
                temp_aff=[]
                for aff in soup.find('div',{'class','manuscript-affiliations'}).find_all('li'):
                    temp_aff.append(aff.text)
                author_aff.append(temp_aff)
                tags.append(m)
                
                        
            else:
                pass
            
        
    
if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
    f=open('preprints.txt','w')
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        f.write(str([title,author,date,abstract,link,tag,author_af]))
        f.write('\n')
    f.close()
else:
    print 'error'
    
