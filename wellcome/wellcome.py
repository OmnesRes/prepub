import time
import requests
from bs4 import BeautifulSoup
import unicodedata
import re
titles=[]
authors=[]
dates=[]
abstracts=[]
links=[]
tags=[]
author_aff=[]

##no subject areas available

for index in range(1,10):
    r=requests.get("https://wellcomeopenresearch.org/browse?selectedDomain=articles&show=20&page="+str(index))
    if not r.ok:
        print r
        
    soup=BeautifulSoup(r.content)
    
    if soup.find_all('div',{'class':'search-result-message-text search-results-empty browse'}):
        break

    for i in soup.find_all("span", {"class":"article-title"}):
        titles.append(i.text.strip())
        tags.append([])

    for i in soup.find_all('div',{'class':'article-detail-text'}):
        temp=[]
        for j in i.find_all('span',{'class':'author-listing-formatted'}):
            name=j.text.split('\n')[1].strip().strip(',')
            temp.append(unicodedata.normalize('NFKD',name).encode('ascii','ignore'))
        authors.append(temp)
                        
    for i in soup.find_all('div',{'class':'article-title-text'}):
        links.append(i.find('a').get('href').strip())
    



for index,i in enumerate(links):
    print index,i
    r=requests.get('https://wellcomeopenresearch.org'+i)
    if not r.ok:
        print r
    soup=BeautifulSoup(r.content)
    abstracts.append(soup.find('div',{'class':"abstract-text is-expanded"}).text.strip())
    temp=[]
    for j in soup.find('div',{'class':'expanded-details affiliations is-hidden'}).text.strip().split('\n'):
        if not re.search('^[0-9]+$',j.strip()):
            temp.append(j.strip())
    author_aff.append(temp)
    temp=[[i.get('name'),i.get('content')] for i in soup.find_all('meta')]
    for j in temp:
        if j[0]=='citation_date':
            dates.append(j[1])



if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
    f=open('wellcome.txt','w')
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        f.write(str([title,author,date,abstract,link,tag,author_af]))
        f.write('\n')
    f.close()
else:
    print 'error'
