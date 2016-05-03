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

categories={'q-bio.BM':'Biomolecules','q-bio.CB':'Cell Behavior','q-bio.GN':'Genomics','q-bio.MN':'Molecular Networks',\
            'q-bio.NC':'Neurons and Cognition','q-bio.OT':'Other','q-bio.PE':'Populations and Evolution',\
            'q-bio.QM':'Quantitative Methods','q-bio.SC':'Subcellular Processes','q-bio.TO':'Tissues and Organs'}



for cat in categories:
    X=True
    index=0
    while X==True:
        print cat, index
        r=requests.get("http://export.arxiv.org/api/query?search_query="\
                       +"cat:"+cat+"&max_results=1000&sortBy=submittedDate&sortOrder=descending&start="+str(index))
        soup=BeautifulSoup(r.content)
        for entry in soup.find_all('entry'):
            titles.append(entry.find('title').text.strip())
            temp=[]
            unique={}
            temp_aff=[]
            for author in entry.find_all('author'):
                temp.append(unicodedata.normalize('NFKD',author.find('name').text.strip()).encode('ascii','ignore'))
                if author.find('arxiv:affiliation')!=None:
                    if author.find('arxiv:affiliation').text.strip() not in unique:
                        unique[author.find('arxiv:affiliation').text.strip()]=''
                        temp_aff.append(author.find('arxiv:affiliation').text.strip())
                        
            authors.append(temp)
            dates.append(entry.find('published').text.strip().split('T')[0])
            abstracts.append(entry.find('summary').text.strip())
            links.append(entry.find('link',{'type':'text/html'}).get('href').strip())
            author_aff.append(temp_aff)
            tags.append([categories[cat]])
        if len(soup.find_all('entry'))<1000:
            X=False
        index+=1000
        time.sleep(3)





if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
    unique={}
    data=[]
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        data.append([title,author,date,abstract,link,tag,author_af])
        article_id=link.split('/')[-1].split('v')[0]
        if unique.get(article_id,[])==[]:
            unique[article_id]=unique.get(article_id,[])+tag
        else:
            if tag[0] not in unique[article_id]:
                unique[article_id]=unique.get(article_id,[])+tag
    newdata=[]
    all_articles={}
    for i in data:
        article_id=i[4].split('/')[-1].split('v')[0]
        if article_id not in all_articles:
            newdata.append(i[:5]+[unique[article_id]]+[i[-1]])
            all_articles[article_id]=''
    f=open('arxiv.txt','w')
    for i in newdata:
        f.write(str(i))
        f.write('\n')
    f.close()
else:
    print 'error'
