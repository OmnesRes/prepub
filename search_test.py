import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prepubmed.settings')

import django
django.setup()

from papers.models import Article
from papers.models import Tag
from papers.models import Affiliation
from papers.models import Author
from datetime import date

import re
import time


from django.db.models import Q

def normalize_query(query_string):
    normspace=re.compile(r'\s{2,}').sub
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    query = None        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
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


start=time.time()
qs=Article.objects.filter(abstract__contains="Presbyopia")
end=time.time()
print end-start

















