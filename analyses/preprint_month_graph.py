date_dict={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
           "July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
           "Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
           "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

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

##nature precedings counts were underestimates when scraping by subject, I have a file with counts from advanced search
f=open('nature_data.txt')
nature_data=eval(f.read())

##f=open(os.path.join(BASE_DIR,'nature','nature.txt'))
##nature=[eval(i.strip()) for i in f]


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


arxiv_counts={}
for i in arxiv:
    temp=i[2].split('-')
    date=[int(temp[0]),int(temp[1])]
    if date[0]>=2007:
        arxiv_counts[tuple(date)]=arxiv_counts.get(tuple(date),0)+1

for i in all_dates:
    if i not in arxiv_counts:
        arxiv_counts[i]=0


arxiv_data=sorted(zip(arxiv_counts.keys(),arxiv_counts.values()))


peerj_counts={}
for i in peerj:
    temp=i[2].split('-')
    date=[int(temp[0]),int(temp[1])]
    peerj_counts[tuple(date)]=peerj_counts.get(tuple(date),0)+1

for i in all_dates:
    if i not in peerj_counts:
        peerj_counts[i]=0
        
peerj_data=sorted(zip(peerj_counts.keys(),peerj_counts.values()))


f1000research_counts={}
for i in f1000research:
    temp=i[2].split()
    date=[int(temp[2]),date_dict[temp[1]]]
    f1000research_counts[tuple(date)]=f1000research_counts.get(tuple(date),0)+1

for i in all_dates:
    if i not in f1000research_counts:
        f1000research_counts[i]=0

f1000research_data=sorted(zip(f1000research_counts.keys(),f1000research_counts.values()))


biorxiv_counts={}
for i in biorxiv:
    temp=i[2].replace(',','').replace('.','').split()
    date=[int(temp[2]),date_dict[temp[0]]]
    biorxiv_counts[tuple(date)]=biorxiv_counts.get(tuple(date),0)+1

for i in all_dates:
    if i not in biorxiv_counts:
        biorxiv_counts[i]=0
        
biorxiv_data=sorted(zip(biorxiv_counts.keys(),biorxiv_counts.values()))

preprints_counts={}
for i in preprints:
    temp=i[2].split()
    date=[int(temp[2]),date_dict[temp[0]]]
    preprints_counts[tuple(date)]=preprints_counts.get(tuple(date),0)+1

for i in all_dates:
    if i not in preprints_counts:
        preprints_counts[i]=0
        
preprints_data=sorted(zip(preprints_counts.keys(),preprints_counts.values()))


winnower_counts={}
for i in winnower:
    temp=i[2].split()
    date=[int(temp[2]),date_dict[temp[0]]]
    winnower_counts[tuple(date)]=winnower_counts.get(tuple(date),0)+1

for i in all_dates:
    if i not in winnower_counts:
        winnower_counts[i]=0
        
winnower_data=sorted(zip(winnower_counts.keys(),winnower_counts.values()))

wellcome_counts={}
for i in wellcome:
    temp=i[2].split('/')
    date=[int(temp[0]),int(temp[1])]
    wellcome_counts[tuple(date)]=wellcome_counts.get(tuple(date),0)+1

for i in all_dates:
    if i not in wellcome_counts:
        wellcome_counts[i]=0
        
wellcome_data=sorted(zip(wellcome_counts.keys(),wellcome_counts.values()))

for i in all_dates:
    if i not in [j[0] for j in nature_data]:
        nature_data.append([i,0])


###plot the data with pylab
fig=plt.figure(figsize=(22.62372, 12))
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=.04)
fig.subplots_adjust(left=.04)
fig.subplots_adjust(right=.98)
fig.subplots_adjust(top=.95)

x1=range(len(all_dates))
y1=np.array([i[1] for i in arxiv_data])
x2_start=0
x2_end=0
for index, i in enumerate(nature_data):
    if i[1]==0:
        pass
    else:
        x2_start=index
        break

for index, i in enumerate(nature_data[::-1]):
    if i[1]==0:
        pass
    else:
        x2_end=len(x1)-index
        break

y2=y1+np.array([i[1] for i in nature_data])

for index, i in enumerate(f1000research_data):
    if i[1]==0:
        pass
    else:
        x3_start=index
        break

y3=y2+np.array([i[1] for i in f1000research_data])

for index, i in enumerate(peerj_data):
    if i[1]==0:
        pass
    else:
        x4_start=index
        break

y4=y3+np.array([i[1] for i in peerj_data])


for index, i in enumerate(biorxiv_data):
    if i[1]==0:
        pass
    else:
        x5_start=index
        break

y5=y4+np.array([i[1] for i in biorxiv_data])

for index, i in enumerate(winnower_data):
    if i[1]==0:
        pass
    else:
        x6_start=index
        break

y6=y5+np.array([i[1] for i in winnower_data])

for index, i in enumerate(preprints_data):
    if i[1]==0:
        pass
    else:
        x7_start=index
        break

y7=y6+np.array([i[1] for i in preprints_data])

for index, i in enumerate(wellcome_data):
    if i[1]==0:
        pass
    else:
        x8_start=index
        break

y8=y7+np.array([i[1] for i in wellcome_data])


plt.axhline(y=200, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=400, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=600, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=800, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=1000, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=1200, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=1400, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=1600, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=1800, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=2000, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)
plt.axhline(y=2200, xmin=0, xmax=len(x1), linewidth=2, color = 'k',linestyle=':',zorder=-1)


ax.fill_between(x1,y1,0,color='#EC5f67',label='arXiv q-bio')
ax.fill_between(x1[x2_start:x2_end],y1[x2_start:x2_end],y2[x2_start:x2_end],color='#AB7967',label='Nature Precedings')
ax.fill_between(x1[x3_start:],y2[x3_start:],y3[x3_start:],color='#F99157',label='F1000Research')
ax.fill_between(x1[x4_start:],y3[x4_start:],y4[x4_start:],color='#FAC863',label='PeerJ Preprints')
ax.fill_between(x1[x5_start:],y4[x5_start:],y5[x5_start:],color='#99C794',label='bioRxiv')
ax.fill_between(x1[x6_start:],y5[x6_start:],y6[x6_start:],color='#5FB3B3',label='The Winnower')
ax.fill_between(x1[x7_start:],y6[x7_start:],y7[x7_start:],color='#6699CC',label='preprints.org')
ax.fill_between(x1[x8_start:],y7[x8_start:],y8[x8_start:],color='#C594C5',label='Wellcome Open Research')



ax.tick_params(axis='x',length=0,width=2,direction='out',labelsize=22)
ax.tick_params(axis='y',length=15,width=0,direction='out',labelsize=20,pad=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_linewidth(3)
ax.spines['bottom'].set_position(['outward',0])
ax.spines['left'].set_position(['outward',-5])
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.set_xticks([i for i in x1 if i%12==0])
ax.set_xticklabels(['2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018'])
ax.set_yticks([200,400,600,800,1000,1200,1400,1600,1800,2000,2200])
ax.set_xlim(0,len(x1)-2)
ax.set_ylim(0,2450)
ax.set_title('Preprints per Month',fontsize=30,y=1.01)

ax.legend(loc=2,frameon=False,fontsize=21,ncol=4)


##plt.savefig('chart.pdf')
plt.savefig('august_preprints.png')
#pillow might be needed for the jpg
##plt.savefig('chart.jpg')
plt.show()



##write the data to a file, exclude last month which is partial
f=open('preprint_data.txt','w')
f.write('\t')
for i in all_dates[:-1]:
    f.write(str(i[0])+'-'+str(i[1]))
    f.write('\t')
f.write('\n')
f.write('arXiv q-bio')
f.write('\t')
for i in arxiv_data[:-1]:
    f.write(str(i[1]))
    f.write('\t')
f.write('\n')
f.write('Nature Precedings')
f.write('\t')
for i in nature_data[:-1]:
    f.write(str(i[1]))
    f.write('\t')
f.write('\n')
f.write('F1000Research')
f.write('\t')
for i in f1000research_data[:-1]:
    f.write(str(i[1]))
    f.write('\t')
f.write('\n')
f.write('PeerJ Preprints')
f.write('\t')
for i in peerj_data[:-1]:
    f.write(str(i[1]))
    f.write('\t')
f.write('\n')
f.write('bioRxiv')
f.write('\t')
for i in biorxiv_data[:-1]:
    f.write(str(i[1]))
    f.write('\t')
f.write('\n')
f.write('Winnower')
f.write('\t')
for i in winnower_data[:-1]:
    f.write(str(i[1]))
    f.write('\t')
f.write('\n')
f.write('preprints.org')
f.write('\t')
for i in preprints_data[:-1]:
    f.write(str(i[1]))
    f.write('\t')
f.write('\n')
f.write('Wellcome Open Research')
f.write('\t')
for i in wellcome_data[:-1]:
    f.write(str(i[1]))
    f.write('\t')
f.write('\n')
f.close()








