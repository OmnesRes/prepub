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

##note there was a retracted article at index 2821

subject_areas={'387':'Genomics, Computational & Systems Biology','394':'Immunology, Microbiology & Infectious Diseases',\
               '396':'Neuroscience, Neurology & Psychiatry','395':'Molecular, Cellular & Structural Biology',\
               '398':'Physiology, Pharmacology & Drug Discovery','401':'Public Health & Epidemiology',\
               '399':'Plant Biology, Ecology & Environmental Sciences','400':'Publishing, Education & Communication',\
               '386':'Cardiopulmonary & Vascular Disorders','391':'Endocrinology & Gastroenterology',\
               '397':'Oncology & Hematology','388':'Critical Care & Emergency Medicine',\
               '402':'Urology, Gynecology & Obstetrics','390':'Development & Evolution',\
               '393':'Hepatology & Nephrology','385':'Bone Disorders',\
               '389':'Dermatology','392':'Eye Disorders & ENT'}
               
               
for subject in subject_areas:
    print subject
    for index in range(1,10):
        r=requests.get("http://f1000research.com/subjects/"+subject+"?selectedDomain=articles&show=100&page="+str(index))
        if not r.ok:
            print r
            
        soup=BeautifulSoup(r.content)
        
        if soup.find_all('div',{'class':'search-result-message-text search-results-empty browse'}):
            break
##        for i in soup.find_all("span", {"class":"article-title"}):
##            titles.append(i.text.strip())
##            tags.append([subject_areas[subject]])
##
##        for i in soup.find_all('div',{'class':'article-detail-text'}):
##            temp=[]
##            for j in i.find_all('span',{'class':'author-listing-formatted'}):
##                name=j.text.split('\n')[1].strip().strip(',')
##                temp.append(unicodedata.normalize('NFKD',name).encode('ascii','ignore'))
##            authors.append(temp)
##                            
##        for i in soup.find_all('div',{'class':'article-title-text'}):
##            links.append(i.find('a').get('href').strip())

#######################this does not work!!!!!!
        for i in soup.find_all("div",{'class':"article-bottom-bar"}):
            dates.append(i.text.strip("PUBLISHED ").split("\n")[0].strip())


##
##
##for index,i in enumerate(links):
##    print index,i
##    r=requests.get('http://f1000research.com'+i)
##    if not r.ok:
##        print r
##    soup=BeautifulSoup(r.content)
##    abstracts.append(soup.find('div',{'class':"abstract-text is-expanded"}).text.strip())
##    temp=[]
##    for j in soup.find('div',{'class':'expanded-details affiliations is-hidden'}).text.strip().split('\n'):
##        if not re.search('^[0-9]+$',j.strip()):
##            temp.append(j.strip())
##    author_aff.append(temp)
##
##
##
##if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
##    f=open('f1000research.txt','w')
##    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
##        f.write(str([title,author,date,abstract,link,tag,author_af]))
##        f.write('\n')
##    f.close()
##else:
##    print 'error'
