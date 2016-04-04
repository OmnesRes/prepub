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

for index in range(1,128):
    print index
    r=requests.get("https://peerj.com/search/?q=&t=&type=preprints&subject=&topic=&uid=&sort=&journal=&page="+str(index))
    soup=BeautifulSoup(r.content)
    for i in soup.find_all("div", {"class":"search-item-title"}):
        titles.append(i.text.strip())
    for i in soup.find_all("div", {"class":"main-search-authors-target"}):
        temp=[]    
        for j in i.find_all("a"):
            temp.append(unicodedata.normalize('NFKD',j.text.strip()).encode('ascii','ignore'))
        authors.append(temp)
    for i in soup.find_all("div",{"class":"span7 main-search-item-subjects"}):
        tags.append(eval(i.text))
    for i in soup.find_all("div", {"class":"search-item-title"}):
        links.append('https://peerj.com'+i.find('a').get('href'))



f=open('titles.txt','w')
f.write(str(titles))
f.close()
f=open('tags.txt','w')
for i in tags:
    f.write(str(i))
    f.write('\n')
f.close()
f=open('links.txt','w')
f.write(str(links))
f.close()
f=open('authors.txt','w')
for i in authors:
    f.write(str(i))
    f.write('\n')
f.close()


for i in links:
    print i
    r=requests.get(i)
    soup=BeautifulSoup(r.content)
    try:
        dates.append(soup.find("time", {"data-itemprop":"dateAccepted"}).text.strip())
    except:
        dates.append(soup.find("time", {"itemprop":"datePublished"}).text.strip())
    abstracts.append(soup.find("div", {"class":"abstract"}).text.strip())
    
    temp=[]
    for j in soup.find_all("span", {"itemprop":"address"}):
        try:
            temp.append(j.find("span", {"class":"institution"}).text.strip())
        except:
            pass
    author_aff.append(temp)


f=open('dates.txt','w')
f.write(str(dates))
f.close()
f=open('author_aff.txt','w')
for i in author_aff:
    f.write(str(i))
    f.write('\n')
f.close()
f=open('abstracts.txt','w')
f.write(str(abstracts))
f.close()
    
