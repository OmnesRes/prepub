import os




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()


from papers.models import Article
from papers.models import Tag
from papers.models import Affiliation
from papers.models import Author
from datetime import date as dt
import time
import requests
from bs4 import BeautifulSoup
import unicodedata







f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\figshare\figshare.txt')
data=[eval(i.strip()) for i in f]
newdata=[]
unique={}
for i in data:
    unique[i[-3].split('/')[-1]]=''



titles=[]
authors=[]
dates=[]
abstracts=[]
links=[]
tags=[]
author_aff=[]
templinks=[]

print len(unique)
print len(templinks)


r=requests.get("https://api.figshare.com/v2/articles?page=1&order=published_date&order_direction=desc&page_size=1000")


for i in r.json():
    if i['url'].split('/')[-1] not in unique:
        unique[i['url'].split('/')[-1]]=''
        templinks.append(i['url'])

print len(unique)
print len(templinks)
        
r=requests.get("https://api.figshare.com/v2/articles?page=1&order=modified_date&order_direction=desc&page_size=1000")


for i in r.json():
    if i['url'].split('/')[-1] not in unique:
        unique[i['url'].split('/')[-1]]=''
        templinks.append(i['url'])

print len(unique)
print len(templinks)

##error=False
##try:
##    for index, i in enumerate(templinks):
##        r=requests.get(i)
##        myjson=r.json()
##        print index, i
##        try:
##            abstract=BeautifulSoup(myjson['description']).find('p').text.strip()
##            date=myjson['created_date'].strip()
##            link=myjson['figshare_url'].strip()
##            title=myjson['title'].strip()
##            temp=[]
##            for j in myjson['categories']:
##                temp.append(j['title'].replace(' not elsewhere classified',''))
##            tag=temp
##            temp=[]
##            for j in myjson['authors']:
##                temp.append(unicodedata.normalize('NFKD',j['full_name']).encode('ascii','ignore'))
##            author=temp
##            author_aff.append([])
##            abstracts.append(abstract)
##            dates.append(date)
##            links.append(link)
##            tags.append(tag)
##            authors.append(author)
##            titles.append(title)
##        except:
##            pass
##except Exception as e:
##    error=True
##    f=open(os.path.join(BASE_DIR,'figshare','error_log',str(dt.today())+'.txt'),'w')
##    f.write(str(e))
##    f.close()
##
##
##
##if error==False:
##    if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
##        f=open(os.path.join(BASE_DIR,'figshare','update_log',str(dt.today())+'.txt'),'w')
##        for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
##            f.write(str([title,author,date,abstract,link,tag,author_af]))
##            f.write('\n')
##            newdata.append([title,author,date,abstract,link,tag,author_af])
##        f.close()
##    else:
##        f=open(os.path.join(BASE_DIR,'figshare','error_log',str(dt.today())+'.txt'),'w')
##        f.write('length error')
##        f.close()
##else:
##    pass


##
##f=open(os.path.join(BASE_DIR,'figshare','figshare.txt'),'a')
##for i in newdata:
##    f.write(str(i))
##    f.write('\n')
##f.close()
##
##
##
##from papers.name_last import name_last
##from papers.name_first import name_first
##from papers.unique_last import unique_last
##from papers.unique_first import unique_first
##
##
##pub_authors=[]
##for i in newdata:
##    for author in i[1]:
##        pub_authors.append(author)
##
##
##
##for i in pub_authors:
##    i=i.replace(',','').replace('.','').lower()
##    if i[:3]=='jr ':
##        i=i[3:]
##    if i[-3:]==' jr':
##        i=i[:-3]
##    if i[:3]=='sr ':
##        i=i[3:]
##    if i[-3:]==' sr':
##        i=i[:-3]
##    first_name=i.split()[0]
##    last_name=i.split()[-1]
##    if len(i.split())==2:
##        middle_name=''
##    else:
##        middle_name=i.replace(first_name+' ','').replace(' '+last_name,'').strip()
##    ##need separate unique dictionaries
##    myauthor_first=(last_name,first_name,middle_function(middle_name))
##    myauthor_last=(last_name,first_function(first_name),middle_function(middle_name))
##    
##    if myauthor_first not in unique_first:
##        unique_first[(last_name,first_name,middle_function(middle_name))]=''
##        name_first[first_name]=[name_first.get(first_name,[[],[]])[0]+[last_name],\
##                                name_first.get(first_name,[[],[]])[1]+[middle_function(middle_name)]]
##
##    if myauthor_last not in unique_last:
##        unique_last[(last_name,first_function(first_name),middle_function(middle_name))]=''
##        name_last[last_name]=[name_last.get(last_name,[[],[]])[0]+[first_function(first_name)],\
##                              name_last.get(last_name,[[],[]])[1]+[middle_function(middle_name)]]
##
##
##
##f=open(os.path.join(BASE_DIR,'papers','unique_last.py'),'w')
##f.write('unique_last='+str(unique_last))
##f.close()
##
##f=open(os.path.join(BASE_DIR,'papers','unique_first.py'),'w')
##f.write('unique_first='+str(unique_first))
##f.close()
##
##f=open(os.path.join(BASE_DIR,'papers','name_last.py'),'w')
##f.write('name_last='+str(name_last))
##f.close()
##
##f=open(os.path.join(BASE_DIR,'papers','name_first.py'),'w')
##f.write('name_first='+str(name_first))
##f.close()
##
##
##
##for i in newdata:
##    paper=Article(title=i[0],abstract=i[3],link=i[4])
##    temp=i[2].split('T')[0].split('-')
##    paper.pub_date=dt(int(temp[0]),int(temp[1]),int(temp[2]))
##    paper.save()
##    temp=[]
##    for author in i[1]:
##        name=author.replace(',','').replace('.','')
##        if name[:3].lower()=='jr ':
##            name=name[3:]
##        if name[-3:].lower()==' jr':
##            name=name[:-3]
##        if name[:3].lower()=='sr ':
##            name=name[3:]
##        if name[-3:].lower()==' sr':
##            name=name[:-3]
##        first_name=name.split()[0]
##        last_name=name.split()[-1]
##        if len(name.split())==2:
##            middle_name=''
##        else:
##            middle_name=name.replace(first_name+' ','').replace(' '+last_name,'').strip()
##        if middle_name!='':
##            temp.append(first_name+' '+middle_name+' '+last_name)
##        else:
##            temp.append(first_name+' '+last_name)
##        try:
##            auth=Author.objects.get(first=first_name,middle=middle_name,last=last_name)
##            paper.authors.add(auth)
##        except:
##            auth=Author.objects.create(first=first_name,middle=middle_name,last=last_name)
##            paper.authors.add(auth)
##    paper.author_list=str(temp)
##    for affiliation in i[-1]:
##        try:
##            aff=Affiliation.objects.get(name=affiliation)
##            paper.affiliations.add(aff)
##        except:
##            aff=Affiliation.objects.create(name=affiliation)
##            paper.affiliations.add(aff)
##    for t in i[-2]:
##        try:
##            tag=Tag.objects.get(name=t)
##            paper.tags.add(tag)
##        except:
##            tag=Tag.objects.create(name=t)
##            paper.tags.add(tag)
##    paper.save()
##    

















##
##f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\biorxiv\biorxiv.txt')
##biorxiv=[eval(i.strip()) for i in f]
##
##f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\f1000research\f1000research.txt')
##f1000research=[eval(i.strip()) for i in f]
##
##
##
##
##





##
##for i in f1000research:
##    paper=Article(title=i[0],abstract=i[3],link='http://f1000research.com'+i[4])
##    temp=i[2].split()
##    paper.pub_date=date(int(temp[2]),date_dict[temp[1]],int(temp[0]))
##    paper.save()
##    temp=[]
##    for author in i[1]:
##        name=author.replace(',','').replace('.','')
##        if name[:3].lower()=='jr ':
##            name=name[3:]
##        if name[-3:].lower()==' jr':
##            name=name[:-3]
##        if name[:3].lower()=='sr ':
##            name=name[3:]
##        if name[-3:].lower()==' sr':
##            name=name[:-3]
##        first_name=name.split()[0]
##        last_name=name.split()[-1]
##        if len(name.split())==2:
##            middle_name=''
##        else:
##            middle_name=name.replace(first_name+' ','').replace(' '+last_name,'').strip()
##        if middle_name!='':
##            temp.append(first_name+' '+middle_name+' '+last_name)
##        else:
##            temp.append(first_name+' '+last_name)
##        try:
##            auth=Author.objects.get(first=first_name,middle=middle_name,last=last_name)
##            paper.authors.add(auth)
##        except:
##            auth=Author.objects.create(first=first_name,middle=middle_name,last=last_name)
##            paper.authors.add(auth)
##    paper.author_list=str(temp)
##    for affiliation in i[-1]:
##        try:
##            aff=Affiliation.objects.get(name=affiliation)
##            paper.affiliations.add(aff)
##        except:
##            aff=Affiliation.objects.create(name=affiliation)
##            paper.affiliations.add(aff)
##    for t in i[-2]:
##        try:
##            tag=Tag.objects.get(name=t)
##            paper.tags.add(tag)
##        except:
##            tag=Tag.objects.create(name=t)
##            paper.tags.add(tag)
##    paper.save()
##
##
##for i in biorxiv:
##    paper=Article(title=i[0],abstract=i[3],link='http://biorxiv.org'+i[4])
##    temp=i[2].replace(',','').replace('.','').split()
##    paper.pub_date=date(int(temp[2]),date_dict[temp[0]],int(temp[1]))
##    paper.save()
##    temp=[]
##    for author in i[1]:
##        name=author.replace(',','').replace('.','')
##        if name[:3].lower()=='jr ':
##            name=name[3:]
##        if name[-3:].lower()==' jr':
##            name=name[:-3]
##        if name[:3].lower()=='sr ':
##            name=name[3:]
##        if name[-3:].lower()==' sr':
##            name=name[:-3]
##        first_name=name.split()[0]
##        last_name=name.split()[-1]
##        if len(name.split())==2:
##            middle_name=''
##        else:
##            middle_name=name.replace(first_name+' ','').replace(' '+last_name,'').strip()
##        if middle_name!='':
##            temp.append(first_name+' '+middle_name+' '+last_name)
##        else:
##            temp.append(first_name+' '+last_name)
##        try:
##            auth=Author.objects.get(first=first_name,middle=middle_name,last=last_name)
##            paper.authors.add(auth)
##        except:
##            auth=Author.objects.create(first=first_name,middle=middle_name,last=last_name)
##            paper.authors.add(auth)
##    paper.author_list=str(temp)
##    for affiliation in i[-1]:
##        try:
##            aff=Affiliation.objects.get(name=affiliation)
##            paper.affiliations.add(aff)
##        except:
##            aff=Affiliation.objects.create(name=affiliation)
##            paper.affiliations.add(aff)
##    for t in i[-2]:
##        try:
##            tag=Tag.objects.get(name=t)
##            paper.tags.add(tag)
##        except:
##            tag=Tag.objects.create(name=t)
##            paper.tags.add(tag)
##    paper.save()
##
##
