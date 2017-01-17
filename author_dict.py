

##create author dictionary


pub_authors=[]

##f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\figshare\figshare.txt')
##figshare=[eval(i.strip()) for i in f]
##for i in figshare:
##    for author in i[1]:
##        pub_authors.append(author)

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\peerj.txt')
peerj=[eval(i.strip()) for i in f]
for i in peerj:
    for author in i[1]:
        pub_authors.append(author)

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\biorxiv\biorxiv.txt')
biorxiv=[eval(i.strip()) for i in f]
for i in biorxiv:
    for author in i[1]:
        pub_authors.append(author)


f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\f1000research\f1000research.txt')
f1000research=[eval(i.strip()) for i in f]
for i in f1000research:
    for author in i[1]:
        pub_authors.append(author)



f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\arxiv\arxiv.txt')
arxiv=[eval(i.strip()) for i in f]
for i in arxiv:
    for author in i[1]:
        pub_authors.append(author)

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\winnower\winnower.txt')
winnower=[eval(i.strip()) for i in f]
for i in winnower:
    for author in i[1]:
        pub_authors.append(author)

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\preprints\preprints.txt')
preprints=[eval(i.strip()) for i in f]
for i in preprints:
    for author in i[1]:
        pub_authors.append(author)


f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\wellcome\wellcome.txt')
wellcome=[eval(i.strip()) for i in f]
for i in wellcome:
    for author in i[1]:
        pub_authors.append(author)

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\nature\nature.txt')
nature=[eval(i.strip()) for i in f]
for i in nature:
    for author in i[1]:
        pub_authors.append(author)

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


##i'm changing unique to include full first name 2016 04 19
##actually, need two unique lists, one for first name and one for last name
name_first={}
name_last={}
unique_last={}
unique_first={}
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





f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\papers\unique_last.py','w')
f.write('unique_last='+str(unique_last))
f.close()

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\papers\unique_first.py','w')
f.write('unique_first='+str(unique_first))
f.close()

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\papers\name_last.py','w')
f.write('name_last='+str(name_last))
f.close()

f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\papers\name_first.py','w')
f.write('name_first='+str(name_first))
f.close()










