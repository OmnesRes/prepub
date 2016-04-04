f=open('abstracts.txt')
abstracts=eval(f.read())
abstracts=abstracts[15:]
f=open(r'author_aff.txt')
author_affs=[]
for i in f:
    author_affs.append(eval(i.strip()))
author_affs=author_affs[15:]
f=open(r'authors.txt')
pub_authors=[]
for i in f:
    pub_authors.append(eval(i.strip()))
pub_authors=pub_authors[15:]
f=open(r'dates.txt')
dates=eval(f.read())
dates=dates[15:]
f=open(r'links.txt')
links=eval(f.read())
links=links[15:]
f=open(r'tags.txt')
tags=[]
for i in f:
    tags.append(eval(i.strip()))
tags=tags[15:]
f=open(r'titles.txt')
titles=eval(f.read())
titles=titles[15:]




f=open('abstracts2.txt')
abstracts2=eval(f.read())
f=open(r'author_aff2.txt')
author_affs2=[]
for i in f:
    author_affs2.append(eval(i.strip()))
f=open(r'authors2.txt')
pub_authors2=[]
for i in f:
    pub_authors2.append(eval(i.strip()))
f=open(r'dates2.txt')
dates2=eval(f.read())
f=open(r'links2.txt')
links2=eval(f.read())
f=open(r'tags2.txt')
tags2=[]
for i in f:
    tags2.append(eval(i.strip()))
f=open(r'titles2.txt')
titles2=eval(f.read())



f=open('abstracts3.txt')
abstracts3=eval(f.read())
f=open(r'author_aff3.txt')
author_affs3=[]
for i in f:
    author_affs3.append(eval(i.strip()))
f=open(r'authors3.txt')
pub_authors3=[]
for i in f:
    pub_authors3.append(eval(i.strip()))
f=open(r'dates3.txt')
dates3=eval(f.read())
f=open(r'links3.txt')
links3=eval(f.read())
f=open(r'tags3.txt')
tags3=[]
for i in f:
    tags3.append(eval(i.strip()))
f=open(r'titles3.txt')
titles3=eval(f.read())

final_abstracts=abstracts+abstracts2+abstracts3
final_author_affs=author_affs+author_affs2+author_affs3
final_pub_authors=pub_authors+pub_authors2+pub_authors3
final_dates=dates+dates2+dates3
final_links=links+links2+links3
final_tags=tags+tags2+tags3
final_titles=titles+titles2+titles3


f=open('titles.txt','w')
f.write(str(final_titles))
f.close()
f=open('tags.txt','w')
for i in final_tags:
    f.write(str(i))
    f.write('\n')
f.close()
f=open('links.txt','w')
f.write(str(final_links))
f.close()
f=open('authors.txt','w')
for i in final_pub_authors:
    f.write(str(i))
    f.write('\n')
f.close()

f=open('dates.txt','w')
f.write(str(final_dates))
f.close()
f=open('author_aff.txt','w')
for i in final_author_affs:
    f.write(str(i))
    f.write('\n')
f.close()
f=open('abstracts.txt','w')
f.write(str(final_abstracts))
f.close()




