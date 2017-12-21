import time
import requests
from bs4 import BeautifulSoup
import unicodedata
titles=[]
links=[]
views=[]
downloads=[]

for index in range(1,231):
    print index
    r=requests.get("https://peerj.com/preprints-search/?page="+str(index))
    soup=BeautifulSoup(r.content)
    for i in soup.find_all("div", {"class":"search-item-title"}):
        if i.find_next_sibling("div")['class'][0]=="search-metrics-container":
            titles.append(i.text.strip())
            links.append('https://peerj.com'+i.find('a').get('href'))
    for i in soup.find_all("div", {"class":"search-label-metric search-label-metric-downloads"}):
        downloads.append(i.text.split('downloads')[0].strip())
    for i in soup.find_all("div", {"class":"search-label-metric search-label-metric-pageviews search-label-metric-arrow"}):
        views.append(i.text.split('views')[0].strip())


data=[]
for i,j,k,l in zip(titles,links,views,downloads):
    data.append([i,j,int(k.replace(',','')),int(l.replace(',',''))])
data.sort(key=lambda x:x[-2],reverse=True)


f=open('metrics_200.txt','w')   
for i in data[:200]:
    f.write(str(i))
    f.write('\n')
f.close()



