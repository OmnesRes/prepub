import unicodedata
f=open('abstracts.txt')
abstracts=eval(f.read())
unique={}
for index,i in enumerate(abstracts):
    try:
        str(i)
    except:
        for j in i:
            try:
                str(j)
            except:
                if j not in unique:
                    unique[j]=''
                    print j, unicodedata.normalize('NFKD',j).encode('ascii','ignore'), repr(j), index
