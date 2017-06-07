##preprints.org changed their author html so I have to reindex authors
import time
import requests
import unicodedata
import re
from bs4 import BeautifulSoup


f=open('preprints.txt')
data=[eval(i.strip()) for i in f]
##f=open('preprints2.txt')
##data2=[eval(i.strip()) for i in f]



##there are retracted articles, not going to update their authors

##f=open('to_be_fixed.txt','w')
##for i,j in zip(data,data2):
##    if i[1]==[]:
##        if j[1]!=[]:
##            f.write(str([j[0]]+[j[1]]+j[2]))
##            f.write('\n')
##f.close()       

data2=[]
for i in data:
    if i[1]==[]:
        authors=[]
        print i[-3]
        r=requests.get('http://preprints.org'+i[-3])
        soup=BeautifulSoup(r.content,'html.parser')
        author_temp=[[k.get('name'),k.get('content')] for k in soup.find_all('meta')]
        for j in author_temp:
            if j[0]=='citation_author':
                authors.append(unicodedata.normalize('NFKD',j[1]).encode('ascii','ignore'))
        data2.append([i[0]]+[authors]+i[2:])
    else:
        data2.append(i)

f=open('preprints2.txt','w')
for i in data2:
    f.write(str(i))
    f.write('\n')
f.close()
        



