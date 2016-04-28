f=open('f1000research_backup.txt')
data=[eval(i.strip()) for i in f]


unique_tags={}
for i in data:
    unique_tags[i[4].split('/')[-2]]=unique_tags.get(i[4].split('/')[-2],[])+i[-2]


unique={}

f=open('f1000research.txt','w')

for i in data:
    if i[4].split('/')[-2] not in unique:
        f.write(str(i[:-2]+[unique_tags[i[4].split('/')[-2]]]+[i[-1]]))
        f.write('\n')
        unique[i[4].split('/')[-2]]=''

f.close()
