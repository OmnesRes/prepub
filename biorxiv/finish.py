import time
import requests
from bs4 import BeautifulSoup
import unicodedata
titles=[]
authors=[]
dates=[]
abstracts=[]
links=[]
tags=[]
author_aff=[]

f=open('links1.txt')
links=eval(f.read())

for index,i in enumerate(links[2597:]):
    print index+2597
    r=requests.get('http://biorxiv.org'+i)
    if not r.ok:
        print r
    soup=BeautifulSoup(r.content)
    dates.append(soup.find('li',{'class':"published"}).text.strip('Posted').strip())
    abstracts.append(soup.find('p',{'id':"p-2"}).text.strip())
    temp=[]
    unique={}
    for j in soup.find_all('span',{'class':'nlm-aff'}):
        if j.text.strip() not in unique:
            unique[j.text.strip()]=''
            temp.append(j.text.strip())
    author_aff.append(temp)
    temp=[]
    for j in soup.find_all('span',{'class':'highwire-article-collection-term'}):
        temp.append(j.text.strip())
    tags.append(temp)

