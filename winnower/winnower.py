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

categories=['biological-sciences','engineering','medicine','chemistry','humanities','computer-sciences','earth-sciences',\
            'mathematics','physics','reddit','science-and-society','social-sciences']

base='https://thewinnower.com/topics/'

for cat in categories:
    index=1
    print cat
    templinks=[]
    while True:
        print index
        r=requests.get(base+cat+'?page='+str(index))
        print r.ok
        soup=BeautifulSoup(r.content,'html.parser')
        for i in soup.find_all("h3", {'class':'alt'}):
            templinks.append(i.find('a').get('href'))
        if soup.find_all("a", {'class':'load_more green button'}):
            index+=1
        else:
            break
    for i in templinks:
        print i
        r=requests.get('https://thewinnower.com'+i)
        soup=BeautifulSoup(r.content,'html.parser')
        if soup.find('ul',{'class','paper-meta'}).find_all('li')[-1].text.split('\n')[-2]=='Paper':
            dates.append(soup.find('ul',{'class','paper-meta'}).find_all('li')[1].text.split('\n')[-2].strip())
            titles.append(soup.find('div',{'class','paper'}).find('h1').text.strip())
            abstracts.append('')
            links.append(i)
            temp_authors=[]
            for j in soup.find('ul',{'class','authors'}).find_all('li'):
                temp_authors.append(unicodedata.normalize('NFKD',j.text.split('\n')[1].strip()).encode('ascii','ignore'))
            authors.append(temp_authors)
            temp_aff=[]
            for j in soup.find('ol',{'class','affiliations'}).find_all('li'):
                temp_aff.append(j.text.split(u'\xa0')[-1].strip())
            author_aff.append(temp_aff)
            if cat=='computer-sciences':
                tags.append(['Computer Sciences'])
            elif cat=='mathematics':
                tags.append(['Mathematics'])
            elif cat=='physics':
                tags.append(['Physics'])
            elif cat=='social-sciences':
                tags.append(['Social Sciences'])
            else:
                temp_tags=[]
                for j in soup.find('ul',{'class',cat}).find_all('li')[1:]:
                    temp_tags.append(j.text.strip())
                tags.append(temp_tags)
                    
        else:
            pass
            
        
    
if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
    f=open('winnower.txt','w')
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        f.write(str([title,author,date,abstract,link,tag,author_af]))
        f.write('\n')
    f.close()
else:
    print 'error'
    
