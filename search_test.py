import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from papers.models import Article
from papers.models import Tag
from papers.models import Affiliation
from papers.models import Author
from datetime import date

import re
import time
import string

from django.db.models import Q

stopwords='''a, about, again, all, almost, also, although, always, among, an, and, another, any, are, as, at,
be, because, been, before, being, between, both, but, by,
can, could,
did, do, does, done, due, during,
each, either, enough, especially, etc,
for, found, from, further,
had, has, have, having, here, how, however,
i, if, in, into, is, it, its, itself,
just,
kg, km,
made, mainly, make, may, mg, might, ml, mm, most, mostly, must,
nearly, neither, no, nor,
obtained, of, often, on, our, overall,
perhaps, pmid,
quite,
rather, really, regarding,
seem, seen, several, should, show, showed, shown, shows, significantly, since, so, some, such,
than, that, the, their, theirs, them, then, there, therefore, these, they, this, those, through, thus, to,
upon, use, used, using,
various, very,
was, we, were, what, when, which, while, with, within, without, would'''

stopwords=[i.strip() for i in stopwords.split(',')]

mypunctuation='!#"$%&\()*+,-./:;<=>?@\\^_`{|}~'

identity = string.maketrans('','')


	

def normalize_query(query_string):
    normspace=re.compile(r'\s{2,}').sub
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def tiab_query(query_string):
    query = None        
    terms = query_string
    for term in terms:
        or_query = None
        for field_name in ['title','abstract']:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


#example
name_test=[['John','Smith'],[['first','full'],['last','full']]]

def au_query(names):
    and_query = None
    for index, name in enumerate(names[0]):
        if names[1][index][1]=='full':
            q = Q(**{"authors__%s__iexact" % names[1][index][0]: name})
        else:
            q = Q(**{"authors__%s__istartswith" % names[1][index][0]: name})
        if and_query is None:
            and_query = q
        else:
            and_query = and_query & q
    return and_query


def super_query():
    pass




##create author dictionary


f=open(r'C:\Users\Jordan Anaya\Desktop\prepub\peerj\authors.txt')
pub_authors=[]
for i in f:
    pub_authors.append(eval(i.strip()))


def middle_function(name):
    if name=='':
        return ''
    else:
        return name[0]

def first_function(name):
    if '-' in name:
        name_split=name.split('-')
        return name_split[0][0]+name_split[1][0]
    else:
        return name[0]

name_first={}
name_last={}
unique={}
for i in pub_authors:
    for author in i:
        author=author.lower()
        first_name=author.split()[0]
        last_name=author.split()[-1]
        middle_name=author.strip(first_name).strip(last_name).strip()
        myauthor=(last_name,first_function(first_name),middle_function(middle_name))
        if myauthor not in unique:
            unique[(last_name,first_function(first_name),middle_function(middle_name))]=''
            name_first[first_name]=''
            name_last[last_name]=[name_last.get(last_name,[[],[]])[0]+[first_function(first_name)],\
                                  name_last.get(last_name,[[],[]])[1]+[middle_function(middle_name)]]



raw="this is a test".lower()


mystring=normalize_query(raw)


##for each author create a list that contains as much info as possible
##[the name (first),],[full or abb]]

#example
[['John','Smith'],[['first','full'],['last','full']]]


##need a function which will group authors together, and other names together


##def parsing_query(mystring):
##    while mystring:
##        for i in mystring:
##            if len(i.split())==1:
##                query=i.translate(identity,mypunctuation)
##                if query not in stopwords and query!='':
##                    if query in name_first:
##    return results
##                
##            






###'some string'.translate(identity,'aeiou')






##start=time.time()
##qs1=Article.objects.filter(tags__name="Animal Behavior").prefetch_related('authors')
##end=time.time()
##print end-start
##
##
##start=time.time()
##qs2=Tag.objects.get(name="Animal Behavior").article_set.all()
##end=time.time()
##print end-start
















