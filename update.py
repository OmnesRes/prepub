import os
##need this
##import subprocess
##subprocess.call(['workon','prepubmed'])


date_dict={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,\
           "July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
           "Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,\
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



BASE_DIR=os.path.dirname(os.path.abspath(__file__))




##peerj


titles=[]
authors=[]
dates=[]
abstracts=[]
links=[]
tags=[]
author_aff=[]


f=open(os.path.join(BASE_DIR,'peerj','peerj.txt'))

data=[eval(i.strip()) for i in f]
newdata=[]


unique={}
all_links=[]
for i in data:
    unique[(i[2],i[-3])]=''
    all_links.append(i[-3])
error=False
try:
    X=True
    for index in range(1,131):
        if X==True:
            print 'index',index
            r=requests.get("https://peerj.com/search/?q=&t=&type=preprints&subject=&topic=&uid=&sort=&journal=&page="+str(index))
            templinks=[]
            soup=BeautifulSoup(r.content,'html.parser')
            for i in soup.find_all("div", {"class":"search-item-title"}):
                templinks.append('https://peerj.com'+i.find('a').get('href'))
                links.append('https://peerj.com'+i.find('a').get('href'))
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
            for index2,i in enumerate(templinks):
                print index2
                r=requests.get(i)
                soup=BeautifulSoup(r.content,'html.parser')
                try:
                    pub_date=soup.find("time", {"data-itemprop":"dateAccepted"}).text.strip()
                except:
                    pub_date=soup.find("time", {"itemprop":"datePublished"}).text.strip()
                if (pub_date,i) not in unique:
                    dates.append(pub_date)
                    abstracts.append(soup.find("div", {"class":"abstract"}).text.strip())
                    temp=[]
                    for j in soup.find_all("span", {"itemprop":"address"}):
                        try:
                            temp.append(j.find("span", {"class":"institution"}).text.strip())
                        except:
                            pass
                    author_aff.append(temp)
                else:
                    stop=index*15-(15-index2)
                    X=False
                    break
        else:
            break
except Exception as e:
    error=True
    f=open(os.path.join(BASE_DIR,'peerj','error_log',str(dt.today())+'.txt'),'w')
    f.write(str(e))
    f.close()


titles=titles[:stop]
authors=authors[:stop]
dates=dates[:stop]
abstracts=abstracts[:stop]
links=links[:stop]
tags=tags[:stop]
author_aff=author_aff[:stop]




##deal with revised articles here: ignore them
if error==False:
    if len(titles)==len(set(titles)):
        if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
            f=open(os.path.join(BASE_DIR,'peerj','update_log',str(dt.today())+'.txt'),'w')
            for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
                if link not in all_links:
                    f.write(str([title,author,date,abstract,link,tag,author_af]))
                    f.write('\n')
                    newdata.append([title,author,date,abstract,link,tag,author_af])
            f.close()
        else:
            f=open(os.path.join(BASE_DIR,'peerj','error_log',str(dt.today())+'.txt'),'w')
            f.write('length error')
            f.close()
    else:
        f=open(os.path.join(BASE_DIR,'peerj','error_log',str(dt.today())+'.txt'),'w')
        f.write('duplicate error')
        f.close()
else:
    pass



f=open(os.path.join(BASE_DIR,'peerj','peerj.txt'),'a')
for i in newdata:
    f.write(str(i))
    f.write('\n')
f.close()



##deal with updating author dictionaries
from papers.name_last import name_last
from papers.name_first import name_first
from papers.unique_last import unique_last
from papers.unique_first import unique_first


pub_authors=[]
for i in newdata:
    for author in i[1]:
        pub_authors.append(author)



for i in pub_authors:
    i=i.replace(',','').replace('.','').lower()
    if i[:3]=='jr ':
        i=i[3:]
    if i[-3:]==' jr':
        i=i[:-3]
    if i[:3]=='sr ':
        i=i[3:]
    if i[-3:]==' sr':
        i=i[:-3]
    first_name=i.split()[0]
    last_name=i.split()[-1]
    if len(i.split())==2:
        middle_name=''
    else:
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




##update the database
for i in newdata:
    paper=Article(title=i[0],abstract=i[3],link=i[4])
    temp=i[2].split('-')
    paper.pub_date=dt(int(temp[0]),int(temp[1]),int(temp[2]))
    paper.save()
    temp=[]
    for author in i[1]:
        name=author.replace(',','').replace('.','')
        if name[:3].lower()=='jr ':
            name=name[3:]
        if name[-3:].lower()==' jr':
            name=name[:-3]
        if name[:3].lower()=='sr ':
            name=name[3:]
        if name[-3:].lower()==' sr':
            name=name[:-3]
        first_name=name.split()[0]
        last_name=name.split()[-1]
        if len(name.split())==2:
            middle_name=''
        else:
            middle_name=name.replace(first_name+' ','').replace(' '+last_name,'').strip()
        if middle_name!='':
            temp.append(first_name+' '+middle_name+' '+last_name)
        else:
            temp.append(first_name+' '+last_name)
        try:
            auth=Author.objects.get(first=first_name,middle=middle_name,last=last_name)
            paper.authors.add(auth)
        except:
            auth=Author.objects.create(first=first_name,middle=middle_name,last=last_name)
            paper.authors.add(auth)
    paper.author_list=str(temp)
    for affiliation in i[-1]:
        try:
            aff=Affiliation.objects.get(name=affiliation)
            paper.affiliations.add(aff)
        except:
            aff=Affiliation.objects.create(name=affiliation)
            paper.affiliations.add(aff)
    for t in i[-2]:
        try:
            tag=Tag.objects.get(name=t)
            paper.tags.add(tag)
        except:
            tag=Tag.objects.create(name=t)
            paper.tags.add(tag)
    paper.save()








##
##
##f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\figshare\figshare.txt')
##figshare=[eval(i.strip()) for i in f]
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
##for i in figshare:
##    paper=Article(title=i[0],abstract=i[3],link=i[4])
##    temp=i[2].split('T')[0].split('-')
##    paper.pub_date=date(int(temp[0]),int(temp[1]),int(temp[2]))
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

