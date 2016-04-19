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

for index in range(1,131):
    print index
    r=requests.get("https://peerj.com/search/?q=&t=&type=preprints&subject=&topic=&uid=&sort=&journal=&page="+str(index))
    print r
    soup=BeautifulSoup(r.content)
    for i in soup.find_all("div", {"class":"search-item-title"}):
        titles.append(i.text.strip())
    for i in soup.find_all("div", {"class":"main-search-authors-target"}):
        temp=[]    
        for j in i.find_all("a"):
            if len(unicodedata.normalize('NFKD',j.text.strip()).encode('ascii','ignore'))==len(j.text.strip()):
                temp.append(unicodedata.normalize('NFKD',j.text.strip()).encode('ascii','ignore'))
            else:
                try:
                    r2=requests.get("https://peerj.com"+j.get('href'))
                    soup2=BeautifulSoup(r2.content)
                    name=soup2.find('h1').find('span').text.strip()
                    temp.append(unicodedata.normalize('NFKD',name).encode('ascii','ignore'))
                except:
                    temp.append(unicodedata.normalize('NFKD',j.text.strip()).encode('ascii','ignore'))
        authors.append(temp)
    for i in soup.find_all("div",{"class":"span7 main-search-item-subjects"}):
        tags.append(eval(i.text))
    for i in soup.find_all("div", {"class":"search-item-title"}):
        links.append('https://peerj.com'+i.find('a').get('href'))
        print 'https://peerj.com'+i.find('a').get('href')
    time.sleep(1)

for index,i in enumerate(links):
    print index
    r=requests.get(i)
    print r
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


if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
    f=open('new_peerj.txt','w')
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        f.write(str([title,author,date,abstract,link,tag,author_af]))
        f.write('\n')
    f.close()
else:
    print 'error'
