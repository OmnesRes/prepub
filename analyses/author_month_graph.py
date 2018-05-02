

date_dict={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
           "July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
           "Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
           "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}


def clean_author(pub_author):
    i=pub_author.replace(',','').replace('.','').lower()
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
        return (first_name,last_name)
    else:
        return None

import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

f=open(os.path.join(BASE_DIR,'peerj','peerj.txt'))
peerj=[eval(i.strip()) for i in f]

f=open(os.path.join(BASE_DIR,'biorxiv','biorxiv.txt'))
biorxiv=[eval(i.strip()) for i in f]

f=open(os.path.join(BASE_DIR,'f1000research','f1000research.txt'))
f1000research=[eval(i.strip()) for i in f]

f=open(os.path.join(BASE_DIR,'arxiv','arxiv.txt'))
arxiv=[eval(i.strip()) for i in f]

f=open(os.path.join(BASE_DIR,'preprints','preprints.txt'))
preprints=[eval(i.strip()) for i in f]

f=open(os.path.join(BASE_DIR,'winnower','winnower.txt'))
winnower=[eval(i.strip()) for i in f]

f=open(os.path.join(BASE_DIR,'wellcome','wellcome.txt'))
wellcome=[eval(i.strip()) for i in f]

f=open(os.path.join(BASE_DIR,'nature','nature.txt'))
nature=[eval(i.strip()) for i in f]


import pylab as plt
import numpy as np
import datetime

##get all possible dates (year, month)
all_dates=[]
current_year=datetime.date.today().year
current_month=datetime.date.today().month
for i in range(2007,current_year):
    for j in range(1,13):
        all_dates.append((i,j))

for i in range(1,current_month+1):
    all_dates.append((current_year,i))


authors={}
for i in arxiv:
    temp=i[2].split('-')
    date=[int(temp[0]),int(temp[1])]
    if date[0]>=2007:
        authors[clean_author(i[1][-1])]=authors.get(clean_author(i[1][-1]),[])+[tuple(date)]
        
for i in peerj:
    temp=i[2].split('-')
    date=[int(temp[0]),int(temp[1])]
    authors[clean_author(i[1][-1])]=authors.get(clean_author(i[1][-1]),[])+[tuple(date)]

for i in f1000research:
    temp=i[2].split()
    date=[int(temp[2]),date_dict[temp[1]]]
    if i[1]==[]:
        pass
    else:
        authors[clean_author(i[1][-1])]=authors.get(clean_author(i[1][-1]),[])+[tuple(date)]

for i in biorxiv:
    temp=i[2].replace(',','').replace('.','').split()
    date=[int(temp[2]),date_dict[temp[0]]]
    if i[1]==[]:
        pass
    else:
        authors[clean_author(i[1][-1])]=authors.get(clean_author(i[1][-1]),[])+[tuple(date)]

for i in preprints:
    temp=i[2].split()
    date=[int(temp[2]),date_dict[temp[0]]]
    if i[1]==[]:
        pass
    else:
        authors[clean_author(i[1][-1])]=authors.get(clean_author(i[1][-1]),[])+[tuple(date)]

for i in winnower:
    temp=i[2].split()
    date=[int(temp[2]),date_dict[temp[0]]]
    if i[1]==[]:
        pass
    else:
        authors[clean_author(i[1][-1])]=authors.get(clean_author(i[1][-1]),[])+[tuple(date)]

for i in wellcome:
    temp=i[2].split('/')
    date=[int(temp[0]),int(temp[1])]
    if i[1]==[]:
        pass
    else:
        authors[clean_author(i[1][-1])]=authors.get(clean_author(i[1][-1]),[])+[tuple(date)]

for i in nature:
    temp=i[2].split('-')
    date=[int(temp[0]),int(temp[1])]
    if i[1]==[]:
        pass
    else:
        authors[clean_author(i[1][-1])]=authors.get(clean_author(i[1][-1]),[])+[tuple(date)]



author_dates={}
for i in authors:
    author_dates[sorted(authors[i])[0]]=author_dates.get(sorted(authors[i])[0],0)+1

for i in all_dates:
    if i not in author_dates:
        author_dates[i]=0
###plot the data with pylab
fig=plt.figure(figsize=(22.62372, 12))
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=.05)
fig.subplots_adjust(left=.05)
fig.subplots_adjust(right=.98)
fig.subplots_adjust(top=.9)

x=range(len(all_dates))
y=[i[1] for i in sorted(zip(author_dates.keys(),author_dates.values()))]

##
##plt.axhline(y=2000, xmin=0, xmax=len(x), linewidth=2, color = 'k',linestyle=':',zorder=-1)
##plt.axhline(y=4000, xmin=0, xmax=len(x), linewidth=2, color = 'k',linestyle=':',zorder=-1)
##plt.axhline(y=6000, xmin=0, xmax=len(x), linewidth=2, color = 'k',linestyle=':',zorder=-1)
##plt.axhline(y=8000, xmin=0, xmax=len(x), linewidth=2, color = 'k',linestyle=':',zorder=-1)
##plt.axhline(y=10000, xmin=0, xmax=len(x), linewidth=2, color = 'k',linestyle=':',zorder=-1)

ax.plot(x,y,lw=5)
ax.tick_params(axis='x',length=0,width=2,direction='out',labelsize=24)
ax.tick_params(axis='y',length=15,width=0,direction='out',labelsize=24,pad=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_linewidth(3)
ax.spines['bottom'].set_linewidth(3)
ax.spines['bottom'].set_position(['outward',0])
ax.spines['left'].set_position(['outward',-5])
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.set_xticks([i for i in x if i%12==0])
ax.set_xticklabels(['2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018'])
ax.set_yticks([100,200,300,400,500,600,700,800,900,1000,1100,1200])
ax.set_xlim(0,len(x)-2)
##ax.set_ylim(0,11000)
ax.set_title('New Senior Authors per Month',fontsize=50)


##plt.savefig('figure1.pdf')
plt.savefig('april_authors.png')
plt.show()
print y[-2]

f=open('author_data.txt','w')
for i in all_dates[:-1]:
    f.write(str(i[0])+'-'+str(i[1]))
    f.write('\t')
f.write('\n')
for i in y[:-1]:
    f.write(str(i))
    f.write('\t')
f.write('\n')
f.close()

