import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prepubmed.settings')

import django
django.setup()

from papers.models import Article
from papers.models import Tag
from papers.models import Affiliation
from papers.models import Author
from datetime import date
f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\abstracts.txt')
abstracts=eval(f.read())
f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\author_aff.txt')
author_affs=[]
for i in f:
    author_affs.append(eval(i.strip()))
f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\authors.txt')
pub_authors=[]
for i in f:
    pub_authors.append(eval(i.strip()))
f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\dates.txt')
dates=eval(f.read())
f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\links.txt')
links=eval(f.read())
f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\tags.txt')
tags=[]
for i in f:
    tags.append(eval(i.strip()))
f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\titles.txt')
titles=eval(f.read())

assert len(abstracts)==len(author_affs)==len(pub_authors)==len(dates)==len(links)==len(titles)==len(tags)


for i,j,k,l,m,n,o in zip(titles,abstracts,dates,pub_authors,tags,author_affs,links):
    paper=Article(title=i,abstract=j,link=o)
    temp=k.split('-')
    paper.pub_date=date(int(temp[0]),int(temp[1]),int(temp[2]))
    paper.save()
    for author in l:
        first_name=author.split()[0]
        last_name=author.split()[-1]
        middle_name=author.strip(first_name).strip(last_name).strip()
        try:
            auth=Author.objects.get(first=first_name,middle=middle_name,last=last_name)
            paper.authors.add(auth)
        except:
            auth=Author.objects.create(first=first_name,middle=middle_name,last=last_name)
            paper.authors.add(auth)
    for affiliation in n:
        try:
            aff=Affiliation.objects.get(name=affiliation)
            paper.affiliations.add(aff)
        except:
            aff=Affiliation.objects.create(name=affiliation)
            paper.affiliations.add(aff)
    for t in m:
        try:
            tag=Tag.objects.get(name=t)
            paper.tags.add(tag)
        except:
            tag=Tag.objects.create(name=t)
            paper.tags.add(tag)
    paper.save()
    



