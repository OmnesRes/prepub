
titles=[]
authors=[]
dates=[]
abstracts=[]
links=[]
tags=[]
author_aff=[]


f=open('titles.txt')
titles=eval(f.read())
f.close()
f=open('dates.txt')
dates=eval(f.read())
f.close()
f=open('abstracts.txt')
abstracts=eval(f.read())
f.close()
f=open('links.txt')
links=eval(f.read())
f.close()
f=open('tags.txt')
for i in f:
    tags.append(eval(i.strip()))
f.close()
f=open('authors.txt')
for i in f:
    authors.append(eval(i.strip()))
f.close()
f=open('author_aff.txt')
for i in f:
    author_aff.append(eval(i.strip()))
f.close()




if len(titles)==len(authors)==len(dates)==len(abstracts)==len(links)==len(tags)==len(author_aff):
    f=open('f1000research.txt','w')
    for title,author,date,abstract,link,tag,author_af in zip(titles,authors,dates,abstracts,links,tags,author_aff):
        f.write(str([title,author,date,abstract,link,tag,author_af]))
        f.write('\n')
    f.close()
else:
    print 'error'
