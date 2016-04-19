'''The code ran into a connection error so had to pick it up where it left off'''

f=open('abstracts1.txt')
abstracts1=eval(f.read())

f=open('abstracts2.txt')
abstracts2=eval(f.read())

f=open('affiliations1.txt')
affiliations1=[]
for i in f:
    affiliations1.append(eval(i.strip()))
    
f=open('affiliations2.txt')
affiliations2=[]
for i in f:
    affiliations2.append(eval(i.strip()))
    
f=open('authors1.txt')
authors=[]
for i in f:
    authors.append(eval(i.strip()))
    
f=open('dates1.txt')
dates1=eval(f.read())

f=open('dates2.txt')
dates2=eval(f.read())

f=open('links1.txt')
links=eval(f.read())

f=open('tags1.txt')
tags1=[]
for i in f:
    tags1.append(eval(i.strip()))

f=open('tags2.txt')
tags2=[]
for i in f:
    tags2.append(eval(i.strip()))

f=open('titles1.txt')
titles=eval(f.read())



abstracts=abstracts1+abstracts2

tags=tags1+tags2

dates=dates1+dates2

author_aff=affiliations1+affiliations2



f=open('biorxiv.txt','w')
for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        f.write(str([title,author,date,abstract,link,tag,author_af]))
        f.write('\n')
f.close()















