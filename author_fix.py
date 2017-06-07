import os
##set virtual env on pythonanywhere with /home/yourusername/path/to/virtualenv/bin/python /home/yourusername/yourscript.py


date_dict={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
           "July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
           "Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
           "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}



def middle_function(name):
    if name=='':
        return ''
    else:
        return name[0]


##this is for abb, needed
def first_function(name):
    try:
        if '-' in name:
            name_split=name.split('-')
            return name_split[0][0]+name_split[1][0]
        else:
            return name[0]
    except:
        return ''

def update_authors(pub_authors):
    for i in pub_authors:
        i=i.replace(',','').replace('.','').lower()
        if i!='':
            if i[:3]=='jr ':
                i=i[3:]
            if i[-3:]==' jr':
                i=i[:-3]
            if i[:3]=='sr ':
                i=i[3:]
            if i[-3:]==' sr':
                i=i[:-3]
            last_name=i.split()[-1]
            if len(i.split())==1:
                first_name=''
                middle_name=''
            elif len(i.split())==2:
                first_name=i.split()[0]
                middle_name=''
            else:
                first_name=i.split()[0]
                middle_name=i.replace(first_name+' ','').replace(' '+last_name,'').strip()
            ##need separate unique dictionaries
            myauthor_first=(last_name,first_name,middle_function(middle_name))
            myauthor_last=(last_name,first_function(first_name),middle_function(middle_name))
            
            if myauthor_first not in unique_first:
                unique_first[(last_name,first_name,middle_function(middle_name))]=''
                name_first[first_name]=[name_first.get(first_name,[[],[]])[0]+[last_name],\
                                        name_first.get(first_name,[[],[]])[1]+[middle_function(middle_name)]]

            if myauthor_last not in unique_last:
                unique_last[(last_name,first_function(first_name),middle_function(middle_name))]=''
                name_last[last_name]=[name_last.get(last_name,[[],[]])[0]+[first_function(first_name)],\
                                      name_last.get(last_name,[[],[]])[1]+[middle_function(middle_name)]]
    if pub_authors!=[]:
        f=open(os.path.join(BASE_DIR,'papers','unique_last.py'),'w')
        f.write('unique_last='+str(unique_last))
        f.close()

        f=open(os.path.join(BASE_DIR,'papers','unique_first.py'),'w')
        f.write('unique_first='+str(unique_first))
        f.close()

        f=open(os.path.join(BASE_DIR,'papers','name_last.py'),'w')
        f.write('name_last='+str(name_last))
        f.close()

        f=open(os.path.join(BASE_DIR,'papers','name_first.py'),'w')
        f.write('name_first='+str(name_first))
        f.close()



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()


from papers.models import Article
from papers.models import Tag
from papers.models import Affiliation
from papers.models import Author
from datetime import date as dt
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import unicodedata
import re
import io



BASE_DIR=os.path.dirname(os.path.abspath(__file__))

f=open(os.path.join(BASE_DIR,'preprints','to_be_fixed.txt'))
data=[eval(i.strip()) for i in f]


######deal with updating author dictionaries
from papers.name_last import name_last
from papers.name_first import name_first
from papers.unique_last import unique_last
from papers.unique_first import unique_first


pub_authors=[]
for i in data:
    for author in i[1]:
        pub_authors.append(author)

update_authors(pub_authors)


for i in data:
    paper=Article.objects.get(title=i[0],link__icontains=i[-3])
    temp=[]
    for author in i[1]:
        name=author.replace(',','').replace('.','')
        if name!='':
            if name[:3].lower()=='jr ':
                name=name[3:]
            if name[-3:].lower()==' jr':
                name=name[:-3]
            if name[:3].lower()=='sr ':
                name=name[3:]
            if name[-3:].lower()==' sr':
                name=name[:-3]
            last_name=name.split()[-1]
            if len(name.split())==1:
                first_name=''
                middle_name=''
            elif len(name.split())==2:
                first_name=name.split()[0]
                middle_name=''
            else:
                first_name=name.split()[0]
                middle_name=name.replace(first_name+' ','').replace(' '+last_name,'').strip()
            if middle_name!='' and first_name!='':
                temp.append(first_name+' '+middle_name+' '+last_name)
            elif middle_name=='' and first_name:
                temp.append(first_name+' '+last_name)
            else:
                temp.append(last_name)
            try:
                auth=Author.objects.get(first=first_name,middle=middle_name,last=last_name)
                paper.authors.add(auth)
            except:
                auth=Author.objects.create(first=first_name,middle=middle_name,last=last_name)
                paper.authors.add(auth)
    paper.author_list=str(temp)
    paper.save()
    

print 'pass'
    

