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




###########################################################################################peerj
##
##
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
##            print 'index',index
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
##                print index2
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
    f=open(os.path.join(BASE_DIR,'peerj','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
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
            f=open(os.path.join(BASE_DIR,'peerj','update_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
            for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
                if link not in all_links:
                    f.write(str([title,author,date,abstract,link,tag,author_af]))
                    f.write('\n')
                    newdata.append([title,author,date,abstract,link,tag,author_af])
            f.close()
        else:
            f=open(os.path.join(BASE_DIR,'peerj','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
            f.write('length error')
            f.close()
    else:
        f=open(os.path.join(BASE_DIR,'peerj','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
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

update_authors(pub_authors)


##update the database
for i in newdata:
    paper=Article(title=i[0],abstract=i[3],link=i[4])
    temp=i[2].split('-')
    paper.pub_date=dt(int(temp[0]),int(temp[1]),int(temp[2]))
    paper.save()
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




############################################################################################figshare

##no longer indexing 20170117
##titles=[]
##authors=[]
##dates=[]
##abstracts=[]
##links=[]
##tags=[]
##author_aff=[]
##templinks=[]
##
##
##f=open(os.path.join(BASE_DIR,'figshare','figshare.txt'))
##data=[eval(i.strip()) for i in f]
##newdata=[]
##unique={}
##for i in data:
##    unique[i[-3].split('/')[-1]]=''
##
##        
##r=requests.get("https://api.figshare.com/v2/articles?page=1&order=modified_date&order_direction=desc&page_size=1000")
##
##
##for i in r.json():
##    if i['url'].split('/')[-1] not in unique:
##        unique[i['url'].split('/')[-1]]=''
##        if 'figshare' in i['doi']:
##            templinks.append(i['url'])
##
##from figshare_categories import categories
##
##error=False
##try:
##    for index, i in enumerate(templinks):
##        r=requests.get(i)
##        myjson=r.json()
####        print index, i
##        try:
##            if 'figshare' in myjson['citation'] and 'Taylor & Francis' not in myjson['citation']:
##                abstract=BeautifulSoup(myjson['description']).find('p').text.strip()
##                if len(abstract)>250:
##                    if ' de ' not in abstract and ' el ' not in abstract and ' y ' not in abstract:
##                        date=myjson['created_date'].strip()
##                        link=myjson['figshare_url'].strip()
##                        title=myjson['title'].strip()
##                        if 'Figure' not in title and '.' not in title and 'Supplement' not in title:
##                            temp=[]
##                            for j in myjson['categories']:
##                                temp.append(j['title'].replace(' not elsewhere classified',''))
##                            tag=temp
##                            temp=[]
##                            for j in myjson['authors']:
##                                temp.append(unicodedata.normalize('NFKD',j['full_name']).encode('ascii','ignore'))
##                            author=temp
##                            author_aff.append([])
##                            abstracts.append(abstract)
##                            dates.append(date)
##                            links.append(link)
##                            tags.append(tag)
##                            authors.append(author)
##                            titles.append(title)
##        except:
##            pass
##
##except Exception as e:
##    error=True
##    f=open(os.path.join(BASE_DIR,'figshare','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
##    f.write(str(e))
##    f.close()
##
##
##
##if error==False:
##    if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
##        f=open(os.path.join(BASE_DIR,'figshare','update_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
##        for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
##            if int(date.split('-')[0])>=2014:
##                for j in tag:
##                    if j in categories:
##                        f.write(str([title,author,date,abstract,link,tag,author_af]))
##                        f.write('\n')
##                        newdata.append([title,author,date,abstract,link,tag,author_af])
##                        break
##        f.close()
##    else:
##        f=open(os.path.join(BASE_DIR,'figshare','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
##        f.write('length error')
##        f.close()
##else:
##    pass
##
##
##
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
##update_authors(pub_authors)
##
##for i in newdata:
##    paper=Article(title=i[0],abstract=i[3],link=i[4])
##    temp=i[2].split('T')[0].split('-')
##    paper.pub_date=dt(int(temp[0]),int(temp[1]),int(temp[2]))
##    paper.save()
##    temp=[]
##    for author in i[1]:
##        name=author.replace(',','').replace('.','')
##        if name!='':
##            if name[:3].lower()=='jr ':
##                name=name[3:]
##            if name[-3:].lower()==' jr':
##                name=name[:-3]
##            if name[:3].lower()=='sr ':
##                name=name[3:]
##            if name[-3:].lower()==' sr':
##                name=name[:-3]
##            first_name=name.split()[0]
##            last_name=name.split()[-1]
##            if len(name.split())==2:
##                middle_name=''
##            else:
##                middle_name=name.replace(first_name+' ','').replace(' '+last_name,'').strip()
##            if middle_name!='':
##                temp.append(first_name+' '+middle_name+' '+last_name)
##            else:
##                temp.append(first_name+' '+last_name)
##            try:
##                auth=Author.objects.get(first=first_name,middle=middle_name,last=last_name)
##                paper.authors.add(auth)
##            except:
##                auth=Author.objects.create(first=first_name,middle=middle_name,last=last_name)
##                paper.authors.add(auth)
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



########################################################################################biorxiv



f=open(os.path.join(BASE_DIR,'biorxiv','biorxiv.txt'))

data=[eval(i.strip()) for i in f]
newdata=[]
unique={}
all_links=[]
for i in data:
    unique[i[4].split('/')[-1].split('.')[0]]=''
    all_links.append(i[4])


for attempt in range(3):
    error=False
    titles=[]
    authors=[]
    dates=[]
    abstracts=[]
    links=[]
    tags=[]
    author_aff=[]
    X=True
    try:
        for index in range(380):
            if X==False:
                break
    ##        print 'index',index
            if index==0:
                r=requests.get("http://biorxiv.org/content/early/recent")
            else:
                r=requests.get("http://biorxiv.org/content/early/recent?page="+str(index))
            soup=BeautifulSoup(r.content)
            for i in soup.find_all("span", {"class":"highwire-cite-title"})[::2]:
                titles.append(i.text.strip())
            for i in soup.find_all('div',{'class':'highwire-cite-authors'}):
                temp=[]    
                for j,k in zip(i.find_all('span',{'class':'nlm-given-names'}),i.find_all('span',{'class':'nlm-surname'})):
                    given=unicodedata.normalize('NFKD',j.text.strip()).encode('ascii','ignore')
                    sur=unicodedata.normalize('NFKD',k.text.strip()).encode('ascii','ignore')
                    temp.append(given+' '+sur)
                authors.append(temp)
            for i in soup.find_all('a',{'class':'highwire-cite-linked-title'}):
                if i.get('href').strip() not in all_links:
                    links.append(i.get('href').strip())
                else:
                    X=False
                    break
        duplicates=[]
        while len(titles)!=len(set(titles)):
            count={}
            for i in titles:
                count[i]=count.get(i,0)+1
            for i in count:
                if count[i]>1:
                    duplicate=i
                    duplicates.append(i)
                    break
            index=titles.index(duplicate)
            titles=titles[:index]+titles[index+1:]
            authors=authors[:index]+authors[index+1:]
            links=links[:index]+links[index+1:]   
        for index2,i in enumerate(links):
    ##        print index2
            r=requests.get('http://biorxiv.org'+i)
            soup=BeautifulSoup(r.content)
            dates.append(soup.find('li',{'class':"published"}).text.strip('Posted').strip())
            try:
                abstracts.append(soup.find('p',{'id':"p-2"}).text.strip())
            except:
                abstracts.append(soup.find('p',{'id':"p-1"}).text.strip())
            temp=[]
            unique_aff={}
            for j in soup.find_all('span',{'class':'nlm-aff'}):
                if j.text.strip() not in unique_aff:
                    unique_aff[j.text.strip()]=''
                    temp.append(j.text.strip())
            author_aff.append(temp)
            temp=[]
            for j in soup.find_all('span',{'class':'highwire-article-collection-term'}):
                temp.append(j.text.strip())
            tags.append(temp)
            
    except Exception as e:
        error=True
        if attempt==2:
            f=open(os.path.join(BASE_DIR,'biorxiv','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
            f.write(str(e))
            f.write('\n')
            f.write(r.content)
            f.close()
    if error==False:
        break
    time.sleep(60)
    
if error==False:
    f=open(os.path.join(BASE_DIR,'biorxiv','update_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        if link.split('/')[-1].split('.')[0] not in unique:
            f.write(str([title,author,date,abstract,link,tag,author_af]))
            f.write('\n')
            newdata.append([title,author,date,abstract,link,tag,author_af])
    f.close()
else:
    pass

if duplicates!=[]:
    f=open(os.path.join(BASE_DIR,'biorxiv','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
    f.write(str(duplicates))
    f.close()

f=open(os.path.join(BASE_DIR,'biorxiv','biorxiv.txt'),'a')
for i in newdata:
    f.write(str(i))
    f.write('\n')
f.close()



####deal with updating author dictionaries
from papers.name_last import name_last
from papers.name_first import name_first
from papers.unique_last import unique_last
from papers.unique_first import unique_first


pub_authors=[]
for i in newdata:
    for author in i[1]:
        pub_authors.append(author)

update_authors(pub_authors)


for i in newdata:
    paper=Article(title=i[0].replace('\n',' ').replace('\t',''),abstract=i[3].replace('\t',''),link='http://biorxiv.org'+i[4])
    temp=i[2].replace(',','').replace('.','').split()
    paper.pub_date=dt(int(temp[2]),date_dict[temp[0]],int(temp[1]))
    paper.save()
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




f=io.open(os.path.join(BASE_DIR,'biorxiv','biorxiv_licenses.tsv'),'a',encoding='utf8')

licenses=[]
for article in newdata:
    r=requests.get('http://biorxiv.org'+article[4]+'.article-info')
    soup=BeautifulSoup(r.content)
    try:
        bio_license=soup.find('span',{'class':'license-type'}).text
    except:
        bio_license=soup.find('span',{'class':'license-type-none'}).text
    licenses.append([article[4],article[2],article[-2],bio_license,article[0],article[1],article[-1]])
    
for i in licenses:
    f.write(u'http://dx.doi.org/10.1101/'+i[0].split('/')[-1].split('.')[0])
    f.write(u'\t')
    temp=i[1].replace(',','').replace('.','').split()
    f.write(unicode(dt(int(temp[2]),date_dict[temp[0]],int(temp[1]))))
    f.write(u'\t')
    for index,j in enumerate(i[2]):
        f.write(unicode(j))
        if index+1==len(i[2]):
            break
        f.write(u'|')
    f.write(u'\t')
    match = re.search(r'CC[ -]BY\S*', i[3])
    if match:
        abbreviation = match.group()
        abbreviation = abbreviation.replace('CC-BY', 'CC BY')
        f.write(abbreviation)
    f.write(u'\t')
    f.write(i[4].replace('\n','').replace('\t',''))
    f.write(u'\t')
    for index,j in enumerate(i[5]):
        f.write(unicode(j))
        if index+1==len(i[5]):
            break
        f.write(u'|')
    f.write(u'\t')
    for index,j in enumerate(i[6]):
        f.write(j.replace('\n','').replace('\t',''))
        if index+1==len(i[6]):
            break
        f.write(u'|')
    f.write(u'\n')
f.close()



################################################################f1000research



f=open(os.path.join(BASE_DIR,'f1000research','f1000research.txt'))
data=[eval(i.strip()) for i in f]
newdata=[]
all_links=[i[4] for i in data]
unique_links=[i[4].split('/')[-2] for i in data]
unique_links+=['5-25']
titles=[]
authors=[]
dates=[]
links=[]
tags=[]
error=False


try:
    X=True
    for index in range(1,10):
        if X==False:
            break
        r=requests.get("https://f1000research.com/browse/articles??selectedDomain=articles&show=20&page="+str(index))

        soup=BeautifulSoup(r.content)
        
        if soup.find_all('div',{'class':'search-result-message-text search-results-empty browse'}):
            break
        for i in soup.find_all("span", {"class":"article-title"}):
            titles.append(i.text.strip())
            tags.append([])

        for i in soup.find_all('div',{'class':'article-detail-text'}):
            temp=[]
            for j in i.find_all('span',{'class':'author-listing-formatted'}):
                name=j.text.split('\n')[1].strip().strip(',')
                temp.append(unicodedata.normalize('NFKD',name).encode('ascii','ignore'))
            authors.append(temp)
                            
        for i in soup.find_all('div',{'class':'article-title-text'}):
            links.append(i.find('a').get('href').strip().split('https://f1000research.com')[1])

        for i in soup.find_all("div",{'class':"article-bottom-bar"}):
            dates.append(i.text.replace("PUBLISHED ","").split("\n")[1].strip())
        for i in links:
            if i in all_links:
                X=False
except Exception as e:
    error=True
    f=open(os.path.join(BASE_DIR,'f1000research','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
    f.write(str(e))
    f.close()     

temp_data=zip(titles,authors,dates,links,tags)
temp_newdata=[]
for i in temp_data:
    if i[3].split('/')[-2] not in unique_links:
        temp_newdata.append(i)


try:
    for index,i in enumerate(temp_newdata):
        r=requests.get('http://f1000research.com'+i[3])
        soup=BeautifulSoup(r.content)
        abstract=soup.find('div',{'class':"abstract-text is-expanded"}).text.strip()
        temp=[]
        affiliation_source=soup.find('div',{'class':'expanded-details affiliations is-hidden'}).text.strip().split('\n')
        for index,j in enumerate(affiliation_source):
            if re.search('^[0-9]+$',j.strip()):
                temp.append(affiliation_source[index+1].strip())
        newdata.append(list(i)[:3]+[abstract]+[i[3]]+[i[-1]]+[temp])
except Exception as e:
    error=True
    f=open(os.path.join(BASE_DIR,'f1000research','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
    f.write(str(e))
    f.close()   



if error==False:
    if len(newdata)==len(set([i[0] for i in newdata])):
        f=open(os.path.join(BASE_DIR,'f1000research','update_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        for i in newdata:
            f.write(str(i))
            f.write('\n')
        f.close()
    else:
        f=open(os.path.join(BASE_DIR,'f1000research','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        f.write('length error')
        f.close()
        error=True


if error==True:
    newdata=[]
else:
    f=open(os.path.join(BASE_DIR,'f1000research','f1000research.txt'),'a')
    for i in newdata:
        f.write(str(i))
        f.write('\n')
    f.close()



######deal with updating author dictionaries
from papers.name_last import name_last
from papers.name_first import name_first
from papers.unique_last import unique_last
from papers.unique_first import unique_first


pub_authors=[]
for i in newdata:
    for author in i[1]:
        pub_authors.append(author)

update_authors(pub_authors)


for i in newdata:
    paper=Article(title=i[0].replace('\t',''),abstract=i[3].replace('\r\n',' '),link='http://f1000research.com'+i[4])
    temp=i[2].split()
    paper.pub_date=dt(int(temp[2]),date_dict[temp[1]],int(temp[0]))
    paper.save()
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



################################################################arxiv



f=open(os.path.join(BASE_DIR,'arxiv','arxiv.txt'))
data=[eval(i.strip()) for i in f]
unique_links=[i[4].split('/')[-1].split('v')[0] for i in data]
titles=[]
authors=[]
dates=[]
abstracts=[]
links=[]
tags=[]
author_aff=[]
error=False



categories={'q-bio.BM':'Biomolecules','q-bio.CB':'Cell Behavior','q-bio.GN':'Genomics','q-bio.MN':'Molecular Networks',\
            'q-bio.NC':'Neurons and Cognition','q-bio.OT':'Other','q-bio.PE':'Populations and Evolution',\
            'q-bio.QM':'Quantitative Methods','q-bio.SC':'Subcellular Processes','q-bio.TO':'Tissues and Organs'}




try: 
    for cat in categories:
        X=True
        index=0
        while X==True:
##            print cat, index
            r=requests.get("http://export.arxiv.org/api/query?search_query="\
                           +"cat:"+cat+"&max_results=20&sortBy=submittedDate&sortOrder=descending&start="+str(index))
            templinks=[]
            soup=BeautifulSoup(r.content)
            for entry in soup.find_all('entry'):
                titles.append(entry.find('title').text.strip().replace('\n',' ').replace('   ',' '))
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
                abstracts.append(entry.find('summary').text.strip().replace('\n',' ').replace('   ',' '))
                links.append(entry.find('link',{'type':'text/html'}).get('href').strip())
                templinks.append(entry.find('link',{'type':'text/html'}).get('href').strip().split('/')[-1].split('v')[0])
                author_aff.append(temp_aff)
                tags.append([categories[cat]])
            for i in templinks:
                if i in unique_links:
                    X=False
                    break
            index+=20
            time.sleep(3)
except Exception as e:
    error=True
    f=open(os.path.join(BASE_DIR,'arxiv','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
    f.write(str(e))
    f.close()     





if error==False:
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
            if article_id not in unique_links:
                if article_id not in all_articles:
                    newdata.append(i[:5]+[unique[article_id]]+[i[-1]])
                    all_articles[article_id]=''
        f=open(os.path.join(BASE_DIR,'arxiv','update_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        for i in newdata:
            f.write(str(i))
            f.write('\n')
        f.close()
    else:
        f=open(os.path.join(BASE_DIR,'arxiv','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        f.write('length error')
        f.close()
        error=True


if error==True:
    newdata=[]
else:
    f=open(os.path.join(BASE_DIR,'arxiv','arxiv.txt'),'a')
    for i in newdata:
        f.write(str(i))
        f.write('\n')
    f.close()



######deal with updating author dictionaries
from papers.name_last import name_last
from papers.name_first import name_first
from papers.unique_last import unique_last
from papers.unique_first import unique_first


pub_authors=[]
for i in newdata:
    for author in i[1]:
        pub_authors.append(author)

update_authors(pub_authors)

for i in newdata:
    paper=Article(title=i[0].replace('\n ',''),abstract=i[3].replace('\n',' '),link=i[4])
    temp=i[2].split('-')
    paper.pub_date=dt(int(temp[0]),int(temp[1]),int(temp[2]))
    paper.save()
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

###############################################################################winnower

f=open(os.path.join(BASE_DIR,'winnower','winnower.txt'))
data=[eval(i.strip()) for i in f]
unique_links=[i[4] for i in data]
titles=[]
authors=[]
dates=[]
abstracts=[]
links=[]
tags=[]
author_aff=[]
error=False


categories=['biological-sciences','engineering','medicine','chemistry','humanities','computer-sciences','earth-sciences',\
            'mathematics','physics','reddit','science-and-society','social-sciences']

base='https://thewinnower.com/topics/'

try:
    for cat in categories:
        index=1
        templinks=[]
        X=True
        while True:
            r=requests.get(base+cat+'?page='+str(index))
            soup=BeautifulSoup(r.content,'html.parser')
            for i in soup.find_all("h3", {'class':'alt'}):
                if i.find('a').get('href') in unique_links:
                    X=False
                else:
                    templinks.append(i.find('a').get('href'))
            if X==False:
                break
            if soup.find_all("a", {'class':'load_more green button'}):
                index+=1
            else:
                break
        for i in templinks:
            r=requests.get('https://thewinnower.com'+i)
            soup=BeautifulSoup(r.content,'html.parser')
            if 'Paper' in str(soup.find('ul',{'class','paper-meta'}).find_all('li')):
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
except Exception as e:
    error=True
    f=open(os.path.join(BASE_DIR,'winnower','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
    f.write(str(e))
    f.close()


if error==False: 
    if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
        data=[]
        for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
            data.append([title,author,date,abstract,link,tag,author_af])
        f=open(os.path.join(BASE_DIR,'winnower','update_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        for i in data:
            f.write(str(i))
            f.write('\n')
        f.close()
    else:
        f=open(os.path.join(BASE_DIR,'winnower','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        f.write('length error')
        f.close()
        error=True



if error==True:
    data=[]
else:
    f=open(os.path.join(BASE_DIR,'winnower','winnower.txt'),'a')
    for i in data:
        f.write(str(i))
        f.write('\n')
    f.close()

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
    paper=Article(title=i[0].replace('\r\n',' '),abstract=i[3],link='https://thewinnower.com'+i[4])
    temp=i[2].split()
    paper.pub_date=dt(int(temp[2]),date_dict[temp[0]],int(temp[1]))
    paper.save()
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

###############################################################################preprints

f=open(os.path.join(BASE_DIR,'preprints','preprints.txt'))
data=[eval(i.strip()) for i in f]
unique_links=[i[4] for i in data]
unique={}
for i in unique_links:
    unique[i.split('/')[-2]]=''
titles=[]
authors=[]
dates=[]
abstracts=[]
links=[]
tags=[]
author_aff=[]
error=False


categories=['biology','medicine_pharmacology','life_sciences']

base='http://preprints.org/subject/browse/'

try:
    for cat in categories:
        index=1
        templinks=[]
        tempdates=[]
        tempabstracts=[]
        temptags=[]
        while True:
            r=requests.get(base+cat+'?page_num='+str(index)+'&page_length=100')
            count=0
            soup=BeautifulSoup(r.content,'html.parser')
            for i in soup.find_all("a", {'class':'title'}):
                if i.get('href') in unique_links:
                    break
                else:
                    templinks.append(i.get('href'))
            for i in soup.find_all('div',{'class','search-content-box'}):
                tempdate=i.find('div',{'class','show-for-large-up'}).text.strip().split('Online: ')[1].split(' (')[0].strip().split()
                tempdates.append(tempdate[1]+' '+tempdate[0]+' '+tempdate[2])
                count+=1
            for i in soup.find_all('div',{'class','abstract-content'}):
                tempabstracts.append(i.text)
            for i in soup.find_all('div',{'class','search-content-box'}):
                temptags.append([i.find_all('div')[4].text.strip().split(', ')[1].split(';')[0].strip()])
            if len(templinks)>len(temptags):
                templinks=templinks[:-1]
            if count==100:
                index+=1
            else:
                break
        for i,j,k,m in zip(templinks,tempdates,tempabstracts,temptags):
            if i.split('/')[-2] not in unique:
                r=requests.get('http://preprints.org'+i)
                soup=BeautifulSoup(r.content,'html.parser')
                if soup.find('span',{'class','type-span'}).text in ['Review','Article']:
                    dates.append(j)
                    titles.append(soup.find('h1').text.strip())
                    abstracts.append(k)
                    links.append(i)
                    temp_authors=[]
                    author_temp=[[l.get('name'),l.get('content')] for l in soup.find_all('meta')]
                    for ii in author_temp:
                        if ii[0]=='citation_author':
                            temp_authors.append(unicodedata.normalize('NFKD',ii[1]).encode('ascii','ignore'))
                    temp_aff=[]
                    for aff in soup.find('div',{'class','manuscript-affiliations'}).find_all('li'):
                        temp_aff.append(aff.text)
                    author_aff.append(temp_aff)
                    authors.append(temp_authors)
                    tags.append(m)    
                else:
                    pass
except Exception as e:
    error=True
    f=open(os.path.join(BASE_DIR,'preprints','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
    f.write(str(e))
    f.close()


if error==False: 
    if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
        data=[]
        for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
            data.append([title,author,date,abstract,link,tag,author_af])
        f=open(os.path.join(BASE_DIR,'preprints','update_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        for i in data:
            f.write(str(i))
            f.write('\n')
        f.close()
    else:
        f=open(os.path.join(BASE_DIR,'preprints','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        f.write('length error')
        f.close()
        error=True



if error==True:
    data=[]
else:
    f=open(os.path.join(BASE_DIR,'preprints','preprints.txt'),'a')
    for i in data:
        f.write(str(i))
        f.write('\n')
    f.close()

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
    paper=Article(title=i[0],abstract=i[3],link='https://www.preprints.org'+i[4])
    temp=i[2].split()
    paper.pub_date=dt(int(temp[2]),date_dict[temp[0]],int(temp[1]))
    paper.save()
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


#################################################################wellcome

f=open(os.path.join(BASE_DIR,'wellcome','wellcome.txt'))
data=[eval(i.strip()) for i in f]
newdata=[]
all_links=[i[4] for i in data]
unique_links=[i[4].split('/')[-2] for i in data]
titles=[]
authors=[]
links=[]
tags=[]
error=False

try: 
    X=True
    for index in range(1,10):
        if X==False:
            break
        r=requests.get("https://wellcomeopenresearch.org/browse?selectedDomain=articles&show=20&page="+str(index))
        soup=BeautifulSoup(r.content)
        
        if soup.find_all('div',{'class':'search-result-message-text search-results-empty browse'}):
            break

        for i in soup.find_all("span", {"class":"article-title"}):
            titles.append(i.text.strip())
            tags.append([])

        for i in soup.find_all('div',{'class':'article-detail-text'}):
            temp=[]
            for j in i.find_all('span',{'class':'author-listing-formatted'}):
                name=j.text.split('\n')[1].strip().strip(',')
                temp.append(unicodedata.normalize('NFKD',name).encode('ascii','ignore'))
            authors.append(temp)
                            
        for i in soup.find_all('div',{'class':'article-title-text'}):
            links.append(i.find('a').get('href').strip().split('https://wellcomeopenresearch.org')[1])

        for i in links:
            if i in all_links:
                X=False
except Exception as e:
    error=True
    f=open(os.path.join(BASE_DIR,'wellcome','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
    f.write(str(e))
    f.close()     

temp_data=zip(titles,authors,links,tags)
temp_newdata=[]
for i in temp_data:
    if i[2].split('/')[-2] not in unique_links:
        temp_newdata.append(i)


try:
    for index,i in enumerate(temp_newdata):
        r=requests.get('https://wellcomeopenresearch.org'+i[2])
        soup=BeautifulSoup(r.content)
        abstract=soup.find('div',{'class':"abstract-text is-expanded"}).text.strip()
        temp=[]
        affiliation_source=soup.find('div',{'class':'expanded-details affiliations is-hidden'}).text.strip().split('\n')
        for index,j in enumerate(affiliation_source):
            if re.search('^[0-9]+$',j.strip()):
                temp.append(affiliation_source[index+1].strip())
        date_temp=[[k.get('name'),k.get('content')] for k in soup.find_all('meta')]
        for j in date_temp:
            if j[0]=='citation_date':
                date=j[1]
        
        newdata.append(list(i)[:2]+[date]+[abstract]+[i[2]]+[i[-1]]+[temp])
except Exception as e:
    error=True
    f=open(os.path.join(BASE_DIR,'wellcome','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
    f.write(str(e))
    f.close()   



if error==False:
    if len(newdata)==len(set([i[0] for i in newdata])):
        f=open(os.path.join(BASE_DIR,'wellcome','update_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        for i in newdata:
            f.write(str(i))
            f.write('\n')
        f.close()
    else:
        f=open(os.path.join(BASE_DIR,'wellcome','error_log',str(datetime.now()).split('.')[0].replace(' ','-').replace(':','-')+'.txt'),'w')
        f.write('length error')
        f.close()
        error=True


if error==True:
    newdata=[]
else:
    f=open(os.path.join(BASE_DIR,'wellcome','wellcome.txt'),'a')
    for i in newdata:
        f.write(str(i))
        f.write('\n')
    f.close()



######deal with updating author dictionaries
from papers.name_last import name_last
from papers.name_first import name_first
from papers.unique_last import unique_last
from papers.unique_first import unique_first


pub_authors=[]
for i in newdata:
    for author in i[1]:
        pub_authors.append(author)

update_authors(pub_authors)


for i in newdata:
    paper=Article(title=i[0],abstract=i[3],link='https://wellcomeopenresearch.org'+i[4])
    temp=i[2].split('/')
    paper.pub_date=dt(int(temp[0]),int(temp[1]),int(temp[2]))
    paper.save()
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





    
