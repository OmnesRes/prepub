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

subjects=['bioinformatics','biotechnology','cancer','chemistry','data-standards','development','earth-and-environment',\
          'ecology','evolutionary-biology','genetics','immunology','microbiology','molecular-cell-biology','neuroscience',\
          'pharmacology','plant-biology']


templinks=[]
for subject in subjects:
    print subject
    for index in range(1,100):
        r=requests.get("http://precedings.nature.com/subjects/"+subject+'?page='+str(index))
        soup=BeautifulSoup(r.content)
        if "There are no documents in this subject." in soup.find_all('em')[0].text:
            break
        for i in soup.find_all('div', {'class':'thumbnail'}):
            templink=i.find('a').get('href')
            if templink not in templinks:
                templinks.append(templink)



for index,i in enumerate(templinks):
    print index
    r=requests.get(i)
    soup=BeautifulSoup(r.content)
    try:
        if soup.find('dl',{'class':'document-details'}).find_all('dd')[0].text=='Manuscript':
            links.append(i)
            titles.append(soup.find('meta',{'name':'DC.title'}).get('content'))
            dates.append(soup.find('meta',{'name':'DC.date'}).get('content'))
            temp_authors=[]
            for j in soup.find_all("meta", {"name":"DC.creator"}):
                temp_authors.append(unicodedata.normalize('NFKD',j.get('content').strip()).encode('ascii','ignore'))
            authors.append(temp_authors)
            temp_tags=[]
            for j in soup.find_all("meta", {"name":"DC.Subject"}):
                temp_tags.append(j.get('content'))
            tags.append(temp_tags)
            temp_aff=[]
            for j in soup.find('ol',{'class':'affiliation'}).find_all('li'):
                temp_aff.append(j.text)
            author_aff.append(temp_aff)
            abstracts.append(soup.find('dl',{'class':'document-details'}).find('dd',{'class':'abstract'}).text)
    except:
        pass
        
    



if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
    f=open('nature.txt','w')
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        f.write(str([title,author,date,abstract,link,tag,author_af]))
        f.write('\n')
    f.close()
else:
    print 'error'
