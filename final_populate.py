import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from papers.models import Article
from papers.models import Tag
from papers.models import Affiliation
from papers.models import Author
from datetime import date


##links for f1000 and biorxiv


##f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\figshare\figshare.txt')
##figshare=[eval(i.strip()) for i in f]

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\peerj.txt')
peerj=[eval(i.strip()) for i in f]

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\biorxiv\biorxiv.txt')
biorxiv=[eval(i.strip()) for i in f]

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\f1000research\f1000research.txt')
f1000research=[eval(i.strip()) for i in f]

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\arxiv\arxiv.txt')
arxiv=[eval(i.strip()) for i in f]

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\preprints\preprints.txt')
preprints=[eval(i.strip()) for i in f]

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\winnower\winnower.txt')
winnower=[eval(i.strip()) for i in f]

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\wellcome\wellcome.txt')
wellcome=[eval(i.strip()) for i in f]

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\nature\nature.txt')
nature=[eval(i.strip()) for i in f]


##work on dates
date_dict={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,\
           "July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
           "Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,\
           "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}


#figshare:
##do this .split('T')[0]
##
##for i in peerj:
##    print i[2]

##biorxiv
##do this
##    temp=i[2].replace(',','').replace('.','').split()
##    print temp[2],date_dict[temp[0]],temp[1]


##f1000research:
##do this
##    temp=i[2].split()
##    print temp[2],date_dict[temp[1]],temp[0]


for i in peerj:
    paper=Article(title=i[0],abstract=i[3],link=i[4])
    temp=i[2].split('-')
    paper.pub_date=date(int(temp[0]),int(temp[1]),int(temp[2]))
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


for i in f1000research:
    paper=Article(title=i[0].replace('\t',''),abstract=i[3].replace('\r\n',' '),link='http://f1000research.com'+i[4])
    temp=i[2].split()
    paper.pub_date=date(int(temp[2]),date_dict[temp[1]],int(temp[0]))
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


for i in biorxiv:
    paper=Article(title=i[0].replace('\n',' ').replace('\t',''),abstract=i[3].replace('\t',''),link='http://biorxiv.org'+i[4])
    temp=i[2].replace(',','').replace('.','').split()
    paper.pub_date=date(int(temp[2]),date_dict[temp[0]],int(temp[1]))
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


for i in arxiv:
    paper=Article(title=i[0].replace('\n ',''),abstract=i[3].replace('\n',' '),link=i[4])
    temp=i[2].split('-')
    paper.pub_date=date(int(temp[0]),int(temp[1]),int(temp[2]))
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



for i in preprints:
    paper=Article(title=i[0],abstract=i[3],link='https://www.preprints.org'+i[4])
    temp=i[2].split()
    paper.pub_date=date(int(temp[2]),date_dict[temp[0]],int(temp[1]))
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


for i in winnower:
    paper=Article(title=i[0].replace('\r\n',' '),abstract=i[3],link='https://thewinnower.com'+i[4])
    temp=i[2].split()
    paper.pub_date=date(int(temp[2]),date_dict[temp[0]],int(temp[1]))
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



for i in wellcome:
    paper=Article(title=i[0],abstract=i[3],link='https://wellcomeopenresearch.org'+i[4])
    temp=i[2].split('/')
    paper.pub_date=date(int(temp[0]),int(temp[1]),int(temp[2]))
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


for i in nature:
    paper=Article(title=i[0],abstract=i[3],link=i[4])
    temp=i[2].split('-')
    paper.pub_date=date(int(temp[0]),int(temp[1]),int(temp[2]))
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
