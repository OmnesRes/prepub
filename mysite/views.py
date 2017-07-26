from django.http import  Http404, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.syndication.views import Feed


from papers.models import Article
from papers.models import Author
from papers.models import Affiliation
from papers.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import re

def ad_au_query(first,middle,last):
    and_query = None
    if first:
        q = Q(**{"authors__%s__iexact" % "first": first})
        if and_query is None:
            and_query = q
        else:
            and_query = and_query & q
    if middle:
        q = Q(**{"authors__%s__iexact" % "middle": middle})
        if and_query is None:
            and_query = q
        else:
            and_query = and_query & q
    if last:
        q = Q(**{"authors__%s__iexact" % "last": last})
        if and_query is None:
            and_query = q
        else:
            and_query = and_query & q
    return and_query

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


class RSSFeed(Feed):
    def get_object(self, request, query):
        try:
            return str(query).lower()
        except:
            return ''

    def title(self, obj):
        return "Custom RSS Feed for PrePubMed"

    def link(self, obj):
        return ('/rss/'+obj+'/')

    def description(self, obj):
        return "Twenty most recent articles for the search: " + obj
    
    def items(self,obj):
        from papers.views import *
        mystring=get_mystring(obj)
        final_query=[]
        for i in mystring:
            if i in stopwords:
                pass
            else:
                final_query.append(i)
        try:
            return Article.objects.filter(tiab_query(final_query)).order_by('-pub_date')[:20]
        except:
            return Article.objects.none()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract

    def item_link(self, item):
        return item.link
        
        

def home(request):
    return render(request, 'home.html')

def monthly_stats(request):
    subject=request.GET.get('Subject',False)
    query=request.GET.get('query',False)
    if request.META.get('HTTP_REFERER',False):
        if query:
            try:
                query=str(request.GET['query']).strip().lower()
                from papers.views import *
                mystring=get_mystring(query)
                all_terms=''
                for i in mystring:
                    if i in stopwords:
                        pass
                    else:
                        all_terms+=i
                if all_terms!='':
                    return render(request, 'monthly_stats.html',{'subject': subject,'query': query})
                else:
                    return render(request, 'monthly_stats.html', {'stopwords':True})
            except:
                return render(request, 'monthly_stats.html', {'unicode':True})
        return render(request, 'monthly_stats.html',{'subject': subject,'query': query})
    else:
        return render(request, 'monthly_stats.html')


def my_help(request):
    return render(request, 'help.html')

def terms(request):
    return render(request, 'terms.html')

def grim_help(request):
    return render(request, 'grim_help.html')

def grimmer(request):
    return render(request, 'grimmer.html')

def rss_feed(request):
    if request.META.get('HTTP_REFERER',False):
        if 'q' in request.GET:
            try:
                query=str(request.GET['q']).strip().lower()
                from papers.views import *
                mystring=get_mystring(query)
                all_terms=''
                for i in mystring:
                    if i in stopwords:
                        pass
                    else:
                        all_terms+=i
                if all_terms!='':
                    return redirect('/articles/'+query+'/rss/')
                else:
                    return render(request, 'rss_feed.html', {'stopwords':True})
            except:
                return render(request, 'rss_feed.html', {'unicode':True})
        else:
            return render(request, 'rss_feed.html')
    else:
        return render(request, 'rss_feed.html')

def advanced_search(request):
    return render(request, 'advanced_search.html')


def round_up(number,places):
    if type(number)==type('string'):
        pass
    else:
        number=repr(number)
    if number[-1]=='5':
        decimals=len(number.split('.')[-1])
        if places<decimals:
            return round(float(number[:-1]+'6'),places)
        else:
            return round(float(number),places)
    else:
        return round(float(number),places)


def my_round(number,places,direction):
    if type(number)==type('string'):
        pass
    else:
        number=repr(number)
    if number[-1]=='5':
        decimals=len(number.split('.')[-1])
        if places<decimals:
            if direction=="Up":
                return round(float(number[:-1]+'6'),places)
            elif direction=="Down":
                return round(float(number[:-1]+'4'),places)
            else:
                if int(float(number))%2==0:
                    return round(float(number[:-1]+'4'),places)
                else:
                    return round(float(number[:-1]+'6'),places)
        else:
            return round(float(number),places)
    else:
        return round(float(number),places)

def grim_plot(request):
    if request.META.get('HTTP_REFERER',False):
        return render(request, 'grim_plot.html',{'mean':request.GET['mean'],'size':request.GET['size']})
    else:
        return redirect(grim_test)

def grim_test(request):
    if request.META.get('HTTP_REFERER',False):
        if 'size' in request.GET:
            try:
                mean=str(request.GET['mean']).strip()
                size=str(request.GET['size']).strip()
            except:
                return render(request, 'grim_test.html', {'unicode':True})
            try:
                direction=str(request.GET['direction']).strip()
            except:
                direction="Up"
            if '.' in mean:
                try:
                    float(mean)
                except:
                    return render(request, 'grim_test.html', {'mean_number':True})
                if len(mean.split('.')[-1])==2:
                    mean=float(mean)
                    if re.search('^[0-9]+$',size):
                        size=int(size)
                        if 1<=size<=100:
                            if my_round(round(mean*size,0)/size,2,direction)==mean:
                                return render(request, 'grim_test.html', {'no_error':True,'direction':direction,'consistent':True,'size':str(size),'mean':"%.2f" % round(mean,2)})
                            else:
                                return render(request, 'grim_test.html', {'no_error':True,'direction':direction,'consistent':False,'size':str(size),'mean':"%.2f" % round(mean,2)})
                        else:
                            return render(request, 'grim_test.html', {'size_wrong':True})
                    else:
                        return render(request, 'grim_test.html', {'size_number':True})
                else:
                    return render(request, 'grim_test.html', {'two_places':True})
            else:
                return render(request, 'grim_test.html', {'decimal':True})
        else:
            return render(request, 'grim_test.html',{'home':True})
    else:
        return render(request, 'grim_test.html',{'home':True,})


def general_grim(request):
    if request.META.get('HTTP_REFERER',False):
        if 'size' in request.GET:
            try:
                mean=str(request.GET['mean']).strip()
                size=str(request.GET['size']).strip()
                likert=str(request.GET['likert']).strip()
            except:
                return render(request, 'general_grim.html', {'unicode':True})
            try:
                direction=str(request.GET['direction']).strip()
            except:
                direction="Up"
            if '.' in mean:
                try:
                    float(mean)
                except:
                    return render(request, 'general_grim.html', {'mean_number':True})
                decimals=len(mean.split('.')[1])
                mean=float(mean)
                if re.search('^[0-9]+$',size):
                    size=int(size)
                    if re.search('^[0-9]+$',likert):
                        likert=int(likert)
                        if my_round(round(mean*size*likert,0)/(size*likert),decimals,direction)==mean:
                            return render(request, 'general_grim.html',\
                                          {'no_error':True,'consistent':True,\
                                           'size':size,\
                                           'mean':("%."+str(decimals)+"f") % round(mean,decimals),\
                                           'likert':likert,\
                                           'direction':direction})
                        else:
                            return render(request, 'general_grim.html',\
                                          {'no_error':True,\
                                           'consistent':False,\
                                           'size':size,\
                                           'mean':("%."+str(decimals)+"f") % round(mean,decimals),\
                                           'likert':likert,\
                                           'direction':direction})
                    else:
                        return render(request, 'general_grim.html', {'likert_number':True})
                else:
                    return render(request, 'general_grim.html', {'size_number':True})
            else:
                return render(request, 'general_grim.html', {'decimal':True})
        else:
            return render(request, 'general_grim.html',{'home':True})
    else:
        return render(request, 'general_grim.html',{'home':True,})



def grimmer_sd(request):
    import re
    import math
    import importlib
    var_precision=12
    if request.META.get('HTTP_REFERER',False):
        if 'size' in request.GET:
            try:
                mean=str(request.GET['mean']).strip()
                size=str(request.GET['size']).strip()
                sd=str(request.GET['sd']).strip()
            except:
                return render(request,'grimmer_sd.html', {'unicode':True})
            try:
                direction=str(request.GET['direction']).strip()
            except:
                direction="Up"
            if re.search('^[0-9]+$',size):
                size=int(size)
            else:
                return render(request,'grimmer_sd.html', {'size_number':True})
            if 'type' in request.GET:
                Type=str(request.GET['type']).strip()
                grim=False
                if 5<=size<=99:
                    mod=importlib.import_module('mysite.patterns.'+str(size))
                    pattern_zero=mod.pattern_zero[:]
                    pattern_even=mod.pattern_even[:]
                    pattern_odd=mod.pattern_odd[:]
                    averages_even=sorted(zip(mod.averages_even.copy().keys(),mod.averages_even.copy().values()))
                    averages_odd=sorted(zip(mod.averages_odd.copy().keys(),mod.averages_odd.copy().values()))
                    pattern_zero_rounded=[round_up('.'+repr(n).split('.')[1],5) for n in pattern_zero]
                    averages_zero={round_up('.'+repr(n).split('.')[1],5):mod.averages_even.copy()[n] for n in mod.averages_even.copy() if round_up('.'+repr(n).split('.')[1],5) in pattern_zero_rounded}
                    averages_zero=sorted(zip(averages_zero.copy().keys(),averages_zero.copy().values()))
                    def loop(low,high):
                        possibilities=[]
                        if low==0:
                            for index,i in enumerate(pattern_zero):
                                possibilities.append([i,index])
                            low=1
                        loop=0
                        X=True
                        if low%2==0:
                            pattern_1=pattern_even
                            pattern_2=pattern_odd
                        else:
                            pattern_1=pattern_odd
                            pattern_2=pattern_even
                        while True:
                            if X==True:
                                for index,i in enumerate(pattern_1):
                                    value=low+i+loop
                                    possibilities.append([value,index])
                                    if value>=high:
                                        X=False
                                        break
                                loop+=1
                                if X==False:
                                    break
                                for index,i in enumerate(pattern_2):
                                    value=low+i+loop
                                    possibilities.append([value,index])
                                    if value>=high:
                                        X=False
                                        break
                                loop+=1
                            else:
                                break
                        return possibilities
                    if mean:
                        if '.' in mean:
                            try:
                                float(mean)
                            except:
                                return render(request,'grimmer_sd.html', {'mean_number':True})
                            mean_decimals=len(mean.split('.')[1])
                            mean=float(mean)
                            if my_round(round_up(mean*size,0)/size,mean_decimals,direction)==mean:
                                grim=True
                            else:
                                return render(request, 'grimmer_sd.html', {'no_error':True,
                                                                        'consistent':False,
                                                                        'size':str(size),
                                                                        'type':Type,
                                                                        'direction':direction,
                                                                        'mean':("%."+str(mean_decimals)+"f") % round_up(mean,mean_decimals)})
                        else:
                            return render(request,'grimmer_sd.html', {'mean_number':True})
                    if '.' in sd:
                        try:
                            float(sd)
                        except:
                            return render(request,'grimmer_sd.html', {'sd_number':True})
                        sd_decimals=len(sd.split('.')[1])
                        sd=float(sd)
                        if sd>100:
                            return render(request,'grimmer_sd.html', {'sd_large':True,})
                        lower=sd-.5/(10**sd_decimals)
                        higher=sd+.5/(10**sd_decimals)
                        ##assume population SD first
                        low=math.floor(lower**2)
                        high=math.ceil(higher**2)
                        sample_count=0
                        population_count=0
                        if Type!='Sample':
                            possibilities=loop(low,high)
                            if grim:
                                for j in possibilities:
                                    if int(j[0])==0:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_zero[j[1]][1]]:
                                            if my_round(j[0]**.5,sd_decimals,direction)==sd:
                                                population_count+=1
                                    elif int(j[0])%2==0:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_even[j[1]][1]]:
                                            if my_round(j[0]**.5,sd_decimals,direction)==sd:
                                                population_count+=1
                                    else:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_odd[j[1]][1]]:
                                            if my_round(j[0]**.5,sd_decimals,direction)==sd:
                                                population_count+=1
                            else:
                                for j in possibilities:
                                    if my_round(j[0]**.5,sd_decimals,direction)==sd:
                                        population_count+=1
                        
##                        try:
####                            all_possibilities=[repr(i) for i in possibilities]
##                        except:
##                            all_possibilities=[]
                        if Type!='Population':
                            #recalculate low and high for sample variance
                            low=math.floor(low*(size-1)/size)
                            high=math.ceil(high*(size-1)/size)
                            possibilities=loop(low,high)
                            if grim:
                                for j in possibilities:
                                    if int(j[0])==0:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_zero[j[1]][1]]:
                                            if my_round((j[0]*size/(size-1))**.5,sd_decimals,direction)==sd:
                                                sample_count+=1
                                    elif int(j[0])%2==0:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_even[j[1]][1]]:
                                            if my_round((j[0]*size/(size-1))**.5,sd_decimals,direction)==sd:
                                                sample_count+=1
                                    else:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_odd[j[1]][1]]:
                                            if my_round((j[0]*size/(size-1))**.5,sd_decimals,direction)==sd:
                                                sample_count+=1
                            else:
                                for j in possibilities:
                                    if my_round((j[0]*size/(size-1))**.5,sd_decimals,direction)==sd:
                                        sample_count+=1
##                            all_possibilities+=[repr(i) for i in possibilities]
                        all_possibilities=[]
                        all_variables=[population_count,sample_count,mean,size,Type,sd]
                        if mean:
                            return render(request,'grimmer_sd.html', {'p_count':population_count,
                                                               's_count':sample_count,
                                                               'mean':("%."+str(mean_decimals)+"f") % round(mean,mean_decimals),
                                                               'size':size,
                                                               'type':Type,
                                                               'direction':direction,
                                                               'sd':("%."+str(sd_decimals)+"f") % round(sd,sd_decimals),
                                                               'no_error':True,
                                                               'consistent':True,
                                                                'possibilities':all_possibilities,
                                                                'all':all_variables,})
                        else:
                            return render(request,'grimmer_sd.html', {'p_count':population_count,
                                                               's_count':sample_count,
                                                               'size':size,
                                                               'type':Type,
                                                               'direction':direction,
                                                               'sd':("%."+str(sd_decimals)+"f") % round(sd,sd_decimals),
                                                               'no_error':True,
                                                               'consistent':True,
                                                                'possibilities':all_possibilities,
                                                                'all':all_variables,})
                    else:
                        if sd=='0':
                            return render(request,'grimmer_sd.html', {'zero':True,})
                        else:
                            return render(request,'grimmer_sd.html', {'sd_number':True,})
                else:
                    return render(request,'grimmer_sd.html', {'size_wrong':True,})
            else:
                return render(request,'grimmer_sd.html', {'type_wrong':True,'mean':mean,'size':size,'sd':sd})
        else:
            return render(request,'grimmer_sd.html', {'home':True,})
    else:
        return render(request,'grimmer_sd.html', {'home':True,})



def grimmer_var(request):
    import re
    import math
    import importlib
    var_precision=12
    if request.META.get('HTTP_REFERER',False):
        if 'size' in request.GET:
            try:
                mean=str(request.GET['mean']).strip()
                size=str(request.GET['size']).strip()
                sd=str(request.GET['sd']).strip()
            except:
                return render(request,'grimmer_var.html', {'unicode':True})
            try:
                direction=str(request.GET['direction']).strip()
            except:
                direction="Up"
            if re.search('^[0-9]+$',size):
                size=int(size)
            else:
                return render(request,'grimmer_var.html', {'size_number':True})
            if 'type' in request.GET:
                Type=str(request.GET['type']).strip()
                grim=False
                if 5<=size<=99:
                    mod=importlib.import_module('mysite.patterns.'+str(size))
                    pattern_zero=mod.pattern_zero[:]
                    pattern_even=mod.pattern_even[:]
                    pattern_odd=mod.pattern_odd[:]
                    averages_even=sorted(zip(mod.averages_even.copy().keys(),mod.averages_even.copy().values()))
                    averages_odd=sorted(zip(mod.averages_odd.copy().keys(),mod.averages_odd.copy().values()))
                    pattern_zero_rounded=[round_up('.'+repr(n).split('.')[1],5) for n in pattern_zero]
                    averages_zero={round_up('.'+repr(n).split('.')[1],5):mod.averages_even.copy()[n] for n in mod.averages_even.copy() if round_up('.'+repr(n).split('.')[1],5) in pattern_zero_rounded}
                    averages_zero=sorted(zip(averages_zero.copy().keys(),averages_zero.copy().values()))
                    def loop(low,high):
                        possibilities=[]
                        if low==0:
                            for index,i in enumerate(pattern_zero):
                                possibilities.append([i,index])
                            low=1
                        loop=0
                        X=True
                        if low%2==0:
                            pattern_1=pattern_even
                            pattern_2=pattern_odd
                        else:
                            pattern_1=pattern_odd
                            pattern_2=pattern_even
                        while True:
                            if X==True:
                                for index,i in enumerate(pattern_1):
                                    value=low+i+loop
                                    possibilities.append([value,index])
                                    if value>=high:
                                        X=False
                                        break
                                loop+=1
                                if X==False:
                                    break
                                for index,i in enumerate(pattern_2):
                                    value=low+i+loop
                                    possibilities.append([value,index])
                                    if value>=high:
                                        X=False
                                        break
                                loop+=1
                            else:
                                break
                        return possibilities
                    if mean:
                        if '.' in mean:
                            try:
                                float(mean)
                            except:
                                return render(request,'grimmer_var.html', {'mean_number':True})
                            mean_decimals=len(mean.split('.')[1])
                            mean=float(mean)
                            if my_round(round_up(mean*size,0)/size,mean_decimals,direction)==mean:
                                grim=True
                            else:
                                return render(request, 'grimmer_var.html', {'no_error':True,
                                                                        'consistent':False,
                                                                        'size':str(size),
                                                                        'mean':("%."+str(mean_decimals)+"f") % round_up(mean,mean_decimals)})
                        else:
                            return render(request,'grimmer_var.html', {'mean_number':True})
                    if '.' in sd:
                        try:
                            float(sd)
                        except:
                            return render(request,'grimmer_var.html', {'sd_number':True})
                        sd_decimals=len(sd.split('.')[1])
                        sd=float(sd)
                        lower=sd-.5/(10**sd_decimals)
                        higher=sd+.5/(10**sd_decimals)
                        ##assume population SD first
                        low=math.floor(lower)
                        high=math.ceil(higher)
                        sample_count=0
                        population_count=0
                        if Type!='Sample':
                            possibilities=loop(low,high)
                            if grim:
                                for j in possibilities:
                                    if int(j[0])==0:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_zero[j[1]][1]]:
                                            if my_round(j[0],sd_decimals,direction)==sd:
                                                population_count+=1
                                    elif int(j[0])%2==0:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_even[j[1]][1]]:
                                            if my_round(j[0],sd_decimals,direction)==sd:
                                                population_count+=1
                                    else:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_odd[j[1]][1]]:
                                            if my_round(j[0],sd_decimals,direction)==sd:
                                                population_count+=1
                            else:
                                for j in possibilities:
                                    if my_round(j[0],sd_decimals,direction)==sd:
                                        population_count+=1
                        
##                        try:
####                            all_possibilities=[repr(i) for i in possibilities]
##                        except:
##                            all_possibilities=[]
                        if Type!='Population':
                            #recalculate low and high for sample variance
                            low=math.floor(low*(size-1)/size)
                            high=math.ceil(high*(size-1)/size)
                            possibilities=loop(low,high)
                            if grim:
                                for j in possibilities:
                                    if int(j[0])==0:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_zero[j[1]][1]]:
                                            if my_round(j[0]*size/(size-1),sd_decimals,direction)==sd:
                                                sample_count+=1
                                            else:
                                                if round_up(round(j[0]*size/(size-1),10),sd_decimals)==sd:
                                                    sample_count+=1
                                    elif int(j[0])%2==0:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_even[j[1]][1]]:
                                            if my_round(j[0]*size/(size-1),sd_decimals,direction)==sd:
                                                sample_count+=1
                                            else:
                                                if round_up(round(j[0]*size/(size-1),10),sd_decimals)==sd:
                                                    sample_count+=1
                                    else:
                                        if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_odd[j[1]][1]]:
                                            if my_round(j[0]*size/(size-1),sd_decimals,direction)==sd:
                                                sample_count+=1
                                            else:
                                                if round_up(round(j[0]*size/(size-1),10),sd_decimals)==sd:
                                                    sample_count+=1
                            else:
                                for j in possibilities:
                                    if my_round(j[0]*size/(size-1),sd_decimals,direction)==sd:
                                        sample_count+=1
                                    else:
                                        if round_up(round(j[0]*size/(size-1),10),sd_decimals)==sd:
                                            sample_count+=1
##                            all_possibilities+=[repr(i) for i in possibilities]
                        all_possibilities=[]
                        all_variables=[population_count,sample_count,mean,size,Type,sd]
                        if mean:
                            return render(request,'grimmer_var.html', {'p_count':population_count,
                                                               's_count':sample_count,
                                                               'mean':("%."+str(mean_decimals)+"f") % round(mean,mean_decimals),
                                                               'size':size,
                                                               'type':Type,
                                                               'direction':direction,
                                                               'sd':("%."+str(sd_decimals)+"f") % round(sd,sd_decimals),
                                                               'no_error':True,
                                                               'consistent':True,
                                                                'possibilities':all_possibilities,
                                                                'all':all_variables,})
                        else:
                            return render(request,'grimmer_var.html', {'p_count':population_count,
                                                               's_count':sample_count,
                                                               'size':size,
                                                               'type':Type,
                                                               'direction':direction,
                                                               'sd':("%."+str(sd_decimals)+"f") % round(sd,sd_decimals),
                                                               'no_error':True,
                                                               'consistent':True,
                                                                'possibilities':all_possibilities,
                                                                'all':all_variables,})
                    else:
                        if sd=='0':
                            return render(request,'grimmer_var.html', {'zero':True,})
                        else:
                            return render(request,'grimmer_var.html', {'sd_number':True,})
                else:
                    return render(request,'grimmer_var.html', {'size_wrong':True,})
            else:
                return render(request,'grimmer_var.html', {'type_wrong':True,'mean':mean,'size':size,'sd':sd})
        else:
            return render(request,'grimmer_var.html', {'home':True,})
    else:
        return render(request,'grimmer_var.html', {'home':True,})


def grimmer_se(request):
    import re
    import math
    import importlib
    var_precision=12
    if request.META.get('HTTP_REFERER',False):
        if 'size' in request.GET:
            try:
                mean=str(request.GET['mean']).strip()
                size=str(request.GET['size']).strip()
                sd=str(request.GET['sd']).strip()
            except:
                return render(request,'grimmer_sd.html', {'unicode':True})
            try:
                direction=str(request.GET['direction']).strip()
            except:
                direction="Up"
            if re.search('^[0-9]+$',size):
                size=int(size)
            else:
                return render(request,'grimmer_se.html', {'size_number':True})
            grim=False
            if 5<=size<=99:
                mod=importlib.import_module('mysite.patterns.'+str(size))
                pattern_zero=mod.pattern_zero[:]
                pattern_even=mod.pattern_even[:]
                pattern_odd=mod.pattern_odd[:]
                averages_even=sorted(zip(mod.averages_even.copy().keys(),mod.averages_even.copy().values()))
                averages_odd=sorted(zip(mod.averages_odd.copy().keys(),mod.averages_odd.copy().values()))
                pattern_zero_rounded=[round_up('.'+repr(n).split('.')[1],5) for n in pattern_zero]
                averages_zero={round_up('.'+repr(n).split('.')[1],5):mod.averages_even.copy()[n] for n in mod.averages_even.copy() if round_up('.'+repr(n).split('.')[1],5) in pattern_zero_rounded}
                averages_zero=sorted(zip(averages_zero.copy().keys(),averages_zero.copy().values()))
                def loop(low,high):
                    possibilities=[]
                    if low==0:
                        for index,i in enumerate(pattern_zero):
                            possibilities.append([i,index])
                        low=1
                    loop=0
                    X=True
                    if low%2==0:
                        pattern_1=pattern_even
                        pattern_2=pattern_odd
                    else:
                        pattern_1=pattern_odd
                        pattern_2=pattern_even
                    while True:
                        if X==True:
                            for index,i in enumerate(pattern_1):
                                value=low+i+loop
                                possibilities.append([value,index])
                                if value>=high:
                                    X=False
                                    break
                            loop+=1
                            if X==False:
                                break
                            for index,i in enumerate(pattern_2):
                                value=low+i+loop
                                possibilities.append([value,index])
                                if value>=high:
                                    X=False
                                    break
                            loop+=1
                        else:
                            break
                    return possibilities
                if mean:
                    if '.' in mean:
                        try:
                            float(mean)
                        except:
                            return render(request,'grimmer_se.html', {'mean_number':True})
                        mean_decimals=len(mean.split('.')[1])
                        mean=float(mean)
                        if my_round(round_up(mean*size,0)/size,mean_decimals,direction)==mean:
                            grim=True
                        else:
                            return render(request, 'grimmer_se.html', {'no_error':True,
                                                                    'consistent':False,
                                                                    'size':str(size),
                                                                    'mean':("%."+str(mean_decimals)+"f") % round_up(mean,mean_decimals)})
                    else:
                        return render(request,'grimmer_se.html', {'mean_number':True})
                if '.' in sd:
                    try:
                        float(sd)
                    except:
                        return render(request,'grimmer_se.html', {'sd_number':True})
                    sd_decimals=len(sd.split('.')[1])
                    sd=float(sd)
                    if sd>100:
                        return render(request,'grimmer_se.html', {'sd_large':True,})
                    lower=sd-.5/(10**sd_decimals)
                    higher=sd+.5/(10**sd_decimals)
                    ##assume population SD first
                    low=math.floor((lower*size**.5)**2)
                    low=math.floor(low*(size-1)/size)
                    high=math.ceil((higher*size**.5)**2)
                    high=math.ceil(high*(size-1)/size)
                    count=0
                    possibilities=loop(low,high)
                    if grim:
                        for j in possibilities:
                            if int(j[0])==0:
                                if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_zero[j[1]][1]]:
                                    if my_round(((j[0]*size/(size-1))**.5)/size**.5,sd_decimals,direction)==sd:
                                        count+=1
                            elif int(j[0])%2==0:
                                if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_even[j[1]][1]]:
                                    if my_round(((j[0]*size/(size-1))**.5)/size**.5,sd_decimals,direction)==sd:
                                        count+=1
                            else:
                                if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [my_round(ave,mean_decimals,direction) for ave in averages_odd[j[1]][1]]:
                                    if my_round(((j[0]*size/(size-1))**.5)/size**.5,sd_decimals,direction)==sd:
                                        count+=1
                    else:
                        for j in possibilities:
                            if my_round(((j[0]*size/(size-1))**.5)/size**.5,sd_decimals,direction)==sd:
                                count+=1
                
##                        try:
####                            all_possibilities=[repr(i) for i in possibilities]
##                        except:
##                            all_possibilities=[]
                    all_possibilities=[]
                    all_variables=[count,mean,size,sd]
                    if mean:
                        return render(request,'grimmer_se.html', {'count':count,
                                                           'mean':("%."+str(mean_decimals)+"f") % round(mean,mean_decimals),
                                                           'size':size,
                                                           'direction':direction,
                                                           'sd':("%."+str(sd_decimals)+"f") % round(sd,sd_decimals),
                                                           'no_error':True,
                                                           'consistent':True,
                                                            'possibilities':all_possibilities,
                                                            'all':all_variables,})
                    else:
                        return render(request,'grimmer_se.html', {'count':count,
                                                           'size':size,
                                                           'direction':direction,
                                                           'sd':("%."+str(sd_decimals)+"f") % round(sd,sd_decimals),
                                                           'no_error':True,
                                                           'consistent':True,
                                                            'possibilities':all_possibilities,
                                                            'all':all_variables,})
                else:
                    if sd=='0':
                        return render(request,'grimmer_se.html', {'zero':True,})
                    else:
                        return render(request,'grimmer_se.html', {'sd_number':True,})
            else:
                return render(request,'grimmer_se.html', {'size_wrong':True,})
        else:
            return render(request,'grimmer_se.html', {'home':True,})
    else:
        return render(request,'grimmer_se.html', {'home':True,})




















def make_plot(request):
    if 'size' in request.META['HTTP_REFERER'] and 'mean' in request.META['HTTP_REFERER']:
        from data import *
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.figure import Figure
        import matplotlib.pyplot as plt
        from matplotlib.patches import Ellipse
        import gc
        import numpy as np
        decimal=int(request.META['HTTP_REFERER'].split('mean=')[1].split('&')[0].split('.')[1])
        size=int(request.META['HTTP_REFERER'].split('size=')[1].strip())
        fig=Figure(figsize=(22.62372, 12),facecolor='white')
        fig.subplots_adjust(bottom=0.15)
        fig.subplots_adjust(left=0.06)
        fig.subplots_adjust(right=.99)
        fig.subplots_adjust(top=.99)
        ax=fig.add_subplot(111,)
        white_green = make_colormap({0:'#66ff66',1:'red'})
        Z=np.rot90(np.array(eval(final_data)),k=1)
        Z=Z[::-1]
        ax.pcolor(Z,cmap=white_green)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.set_xticks([i+.5 for i in range(100)])
        ax.set_xticklabels([str(i) for i in range(1,101)],rotation=270)
        ax.set_yticks([i-.5 for i in range(100)][::-1][::2])
        ax.set_yticklabels(["%02d" % i for i in range(-1,99)][::-1][::2])
        ax.set_ylabel('Decimal Value',fontsize=40,labelpad=10)
        ax.set_xlabel('Sample Size',fontsize=40,labelpad=0)
        ax.tick_params(axis='x',length=15,width=2,direction='out',labelsize=12,pad=15)
        ax.tick_params(axis='y',length=15,width=3,direction='out',labelsize=16,pad=20)
        circle1=Ellipse((size-.5,decimal+.5),width=1.06,height=2,color='k',fill=False,lw=4,clip_on=False)
        fig.gca().add_artist(circle1)
        canvas=FigureCanvasAgg(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        fig.clf()
        plt.close(fig)
        del canvas
        gc.collect()
        return response

    
def search_results(request):
    if request.META.get('HTTP_REFERER',False):
        if 'q' in request.GET:
            try:
                raw=str(request.GET['q'].strip().lower())
            except:
                ##put in a message about unicode
                return render(request, 'search_results.html', {'articles':False,'search':None,'unicode':True})
            if raw!='':
                from papers.views import *
                all_terms={'names':[],'terms':[]}
                all_terms=parsing_query(get_mystring(raw),all_terms)
                if all_terms=={'names':[],'terms':[]}:
                    return render(request, 'search_results.html', {'articles':False,'search':None,'stopwords':True})
                else:
                    if len(all_terms['names'])==1 and all_terms['terms']==[]:
                        q=single_au_query(all_terms['names'][0])
                        qs=Author.objects.filter(q)
                        articles=qs[0].article_set.all()
                        for a in qs[1:]:
                            articles=articles | a.article_set.all()
                        articles.order_by('-pub_date')
                    else:
                        articles=perform_query(all_terms).order_by('-pub_date')
                    if articles!=[]:
                        if articles.exists():
                            paginator = Paginator(articles, 20)
                            page = request.GET.get('page')
                            try:
                                Articles = paginator.page(page)
                                authors = [eval(j.author_list) for j in Articles]
                            except PageNotAnInteger:
                                Articles = paginator.page(1)
                                authors = [eval(j.author_list) for j in Articles]
                            except EmptyPage:
                                Articles = paginator.page(paginator.num_pages)
                                authors = [eval(j.author_list) for j in Articles]
                            return render_to_response('search_results.html', {'articles': Articles,'raw':raw,\
                                                                              'search':pretty_terms(all_terms),'authors':authors})
                        else:
                            return render(request, 'search_results.html', {'articles':False,'search':pretty_terms(all_terms)})
                    else:
                        return render(request, 'search_results.html', {'articles':False,'search':pretty_terms(all_terms)})
            else:
                return redirect(home)
        else:
            return redirect(home)
    else:
        return redirect(home)

def search_tag(request):
    if request.META.get('HTTP_REFERER',False):
        if 'q' in request.GET:
            if '%20' in request.META.get('QUERY_STRING'):
                raw=request.META.get('QUERY_STRING').replace('%20',' ').replace('q=','').split('&page=')[0]
            else:
                raw=request.GET['q']
            if raw!='':
                articles=Tag.objects.get(name=raw).article_set.all().order_by('-pub_date')
                if articles.exists():
                    paginator=Paginator(articles, 20)
                    page = request.GET.get('page')
                    try:
                        Articles = paginator.page(page)
                        authors = [eval(j.author_list) for j in Articles]
                    except PageNotAnInteger:
                        Articles = paginator.page(1)
                        authors = [eval(j.author_list) for j in Articles]
                    except EmptyPage:
                        Articles = paginator.page(paginator.num_pages)
                        authors = [eval(j.author_list) for j in Articles]
                    return render_to_response('search_results.html', {'articles':Articles,'raw':raw,'authors':authors})
                else:
                    return render(request, 'search_results.html', {'articles':False})
            else:
                return redirect(home)
        else:
            return redirect(home)
    else:
        return redirect(home)


def search_author(request):
    if request.META.get('HTTP_REFERER',False):
        if 'q' in request.GET:
            raw=request.GET['q']
            if raw!='':
                author=raw
                last_name=author.split()[-1]
                if len(author.split())==1:
                    first_name=''
                    middle_name=''
                elif len(author.split())==2:
                    first_name=author.split()[0]
                    middle_name=''
                else:
                    first_name=author.split()[0]
                    middle_name=author.replace(first_name+' ','').replace(' '+last_name,'').strip()
                middle_name=author.strip(first_name).strip(last_name).strip()
                ##lenient on middle due to punctuation differences
                if middle_name:
                    qs=Author.objects.filter(first=first_name,last=last_name,middle__startswith=middle_name[0])
                    articles=qs[0].article_set.all()
                    for a in qs[1:]:
                        articles=articles | a.article_set.all()
                    articles.order_by('-pub_date')
                else:
                    qs=Author.objects.filter(first=first_name,last=last_name)
                    articles=qs[0].article_set.all()
                    for a in qs[1:]:
                        articles=articles | a.article_set.all()
                    articles.order_by('-pub_date')
                if articles.exists():
                    paginator=Paginator(articles, 20)
                    page=request.GET.get('page')
                    try:
                        Articles = paginator.page(page)
                        authors = [eval(j.author_list) for j in Articles]
                    except PageNotAnInteger:
                        Articles = paginator.page(1)
                        authors = [eval(j.author_list) for j in Articles]
                    except EmptyPage:
                        Articles = paginator.page(paginator.num_pages)
                        authors = [eval(j.author_list) for j in Articles]
                    return render_to_response('search_results.html', {'articles':Articles,'raw':raw,'authors':authors})
                else:
                    return render(request, 'search_results.html', {'articles':False})
            else:
                return redirect(home)
        else:
            return redirect(home)
    else:
        return redirect(home)


def advanced_search_results(request):
    if request.META.get('HTTP_REFERER',False):
        if 'au1f' in request.GET:
            query_string='?au1f=%s&au1m=%s&au1l=%s&au2f=%s&au2m=%s&au2l=%s&ti1=%s&ti2=%s&ab1=%s&ab2=%s&tiab1=%s&tiab2=%s&aff1=%s&aff2=%s'\
                          % (request.GET['au1f'],request.GET['au1m'],request.GET['au1l'],\
                             request.GET['au2f'],request.GET['au2m'],request.GET['au2l'],\
                             request.GET['ti1'],request.GET['ti2'],request.GET['ab1'],request.GET['ab2'],\
                             request.GET['tiab1'],request.GET['tiab2'],\
                             request.GET['aff1'], request.GET['aff2'])
            if request.GET['au1f'] or request.GET['au1m'] or request.GET['au1l'] or\
               request.GET['au2f'] or request.GET['au2m'] or request.GET['au2l'] or\
               request.GET['ti1'] or request.GET['ti2'] or\
               request.GET['ab1'] or request.GET['ab2'] or\
               request.GET['tiab1'] or request.GET['tiab2'] or\
               request.GET['aff1'] or request.GET['aff2']:
                qs=None
                if request.GET['au1f'] or request.GET['au1m'] or request.GET['au1l']:
                    first=request.GET['au1f']
                    middle=request.GET['au1m']
                    last=request.GET['au1l']
                    qs=Article.objects.filter(ad_au_query(first,middle,last))
                if request.GET['au2f'] or request.GET['au2m'] or request.GET['au2l']:
                    first=request.GET['au2f']
                    middle=request.GET['au2m']
                    last=request.GET['au2l']
                    if qs==None:
                        qs=Article.objects.filter(ad_au_query(first,middle,last))
                    else:
                        qs=qs.filter(ad_au_query(first,middle,last))
                if request.GET['ti1']:
                    if qs==None:
                        qs=Article.objects.filter(title__icontains=request.GET['ti1'])
                    else:
                        qs=qs.filter(title__icontains=request.GET['ti1'])
                if request.GET['ti2']:
                    if qs==None:
                        qs=Article.objects.filter(title__icontains=request.GET['ti2'])
                    else:
                        qs=qs.filter(title__icontains=request.GET['ti2'])
                if request.GET['ab1']:
                    if qs==None:
                        qs=Article.objects.filter(abstract__icontains=request.GET['ab1'])
                    else:
                        qs=qs.filter(abstract__icontains=request.GET['ab1'])
                if request.GET['ab2']:
                    if qs==None:
                        qs=Article.objects.filter(abstract__icontains=request.GET['ab2'])
                    else:
                        qs=qs.filter(abstract__icontains=request.GET['ab2'])
                if request.GET['tiab1']:
                    if qs==None:
                        qs=Article.objects.filter(tiab_query([request.GET['tiab1']]))
                    else:
                        qs=qs.filter(tiab_query([request.GET['tiab1']]))
                if request.GET['tiab2']:
                    if qs==None:
                        qs=Article.objects.filter(tiab_query([request.GET['tiab2']]))
                    else:
                        qs=qs.filter(tiab_query([request.GET['tiab2']]))
                if request.GET['aff1']:
                    if qs==None:
                        qs=Article.objects.filter(affiliations__name__icontains=request.GET['aff1']).distinct()
                    else:
                        qs=qs.filter(affiliations__name__icontains=request.GET['aff1']).distinct()
                if request.GET['aff2']:
                    if qs==None:
                        qs=Article.objects.filter(affiliations__name__icontains=request.GET['aff2']).distinct()
                    else:
                        qs=qs.filter(affiliations__name__icontains=request.GET['aff2']).distinct()
                if qs.exists():
                    qs=qs.order_by('-pub_date')
                    paginator=Paginator(qs, 20)
                    page=request.GET.get('page')
                    try:
                        Articles = paginator.page(page)
                        authors = [eval(j.author_list) for j in Articles]
                    except PageNotAnInteger:
                        Articles = paginator.page(1)
                        authors = [eval(j.author_list) for j in Articles]
                    except EmptyPage:
                        Articles = paginator.page(paginator.num_pages)
                        authors = [eval(j.author_list) for j in Articles]
                    return render_to_response('search_results.html', {'articles':Articles,'query_string':query_string,\
                                                                      'authors':authors})
                else:
                    return render(request, 'search_results.html', {'articles':False})
            else:
                return redirect(advanced_search)
        else:
            return redirect(advanced_search)
    else:
        return redirect(advanced_search)

def subject_plot(request):
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    import gc
    import datetime
    import numpy as np
    if not request.META.get('HTTP_REFERER',False):
        return HttpResponse('something is wrong')
    else:
        raw=request.META.get('HTTP_REFERER').replace('+',' ').replace('%20',' ').replace('%2C',',').replace('%26','&')
        subject=raw.split('Subject=')[1]
        qs=Tag.objects.get(name=subject).article_set.all().filter(pub_date__gte=datetime.date(2014,1,1))
        data=[(i.pub_date,i.link) for i in qs]
        all_dates=[]
        current_year=datetime.date.today().year
        current_month=datetime.date.today().month
        for i in range(2014,current_year):
            for j in range(1,13):
                all_dates.append((i,j))
        for i in range(1,current_month+1):
            all_dates.append((current_year,i))
        arxiv_counts={}
        peerj_counts={}
        f1000research_counts={}
        biorxiv_counts={}
        preprints_counts={}
        winnower_counts={}
        wellcome_counts={}
        for i in data:
            date=(i[0].year,i[0].month)
            if 'arxiv.org' in i[1]:
                arxiv_counts[date]=arxiv_counts.get(date,0)+1
            elif 'peerj.com' in i[1]:
                peerj_counts[date]=peerj_counts.get(date,0)+1
            elif 'f1000research.com' in i[1]:
                f1000research_counts[date]=f1000research_counts.get(date,0)+1
            elif 'biorxiv.org' in i[1]:
                biorxiv_counts[date]=biorxiv_counts.get(date,0)+1
            elif 'preprints.org' in i[1]:
                preprints_counts[date]=preprints_counts.get(date,0)+1
            elif 'thewinnower.com' in i[1]:
                winnower_counts[date]=winnower_counts.get(date,0)+1
            elif 'wellcomeopenresearch.org' in i[1]:
                wellcome_counts[date]=wellcome_counts.get(date,0)+1
            else:
                pass

        for i in all_dates:
            if i not in arxiv_counts:
                arxiv_counts[i]=0
            if i not in peerj_counts:
                peerj_counts[i]=0
            if i not in f1000research_counts:
                f1000research_counts[i]=0
            if i not in biorxiv_counts:
                biorxiv_counts[i]=0
            if i not in preprints_counts:
                preprints_counts[i]=0
            if i not in winnower_counts:
                winnower_counts[i]=0
            if i not in wellcome_counts:
                wellcome_counts[i]=0

        
        arxiv_data=sorted(zip(arxiv_counts.keys(),arxiv_counts.values()))
        peerj_data=sorted(zip(peerj_counts.keys(),peerj_counts.values()))
        f1000research_data=sorted(zip(f1000research_counts.keys(),f1000research_counts.values()))
        biorxiv_data=sorted(zip(biorxiv_counts.keys(),biorxiv_counts.values()))
        preprints_data=sorted(zip(preprints_counts.keys(),preprints_counts.values()))
        winnower_data=sorted(zip(winnower_counts.keys(),winnower_counts.values()))
        wellcome_data=sorted(zip(wellcome_counts.keys(),wellcome_counts.values()))
            
                                                                  
        fig=Figure(figsize=(22.62372, 12),facecolor='white')
        ax=fig.add_subplot(111,)
        fig.subplots_adjust(bottom=.1)
        fig.subplots_adjust(left=.04)
        fig.subplots_adjust(right=.98)
        fig.subplots_adjust(top=.96)
        x1=range(len(all_dates))
        y1=np.array([i[1] for i in arxiv_data])

        x3_start=-1
        for index, i in enumerate(f1000research_data):
            if i[1]==0:
                pass
            else:
                x3_start=index
                break

        y3=y1+np.array([i[1] for i in f1000research_data])

        x4_start=-1
        for index, i in enumerate(peerj_data):
            if i[1]==0:
                pass
            else:
                x4_start=index
                break

        y4=y3+np.array([i[1] for i in peerj_data])

        x5_start=-1
        for index, i in enumerate(biorxiv_data):
            if i[1]==0:
                pass
            else:
                x5_start=index
                break

        x6_start=-1
        y5=y4+np.array([i[1] for i in biorxiv_data])

        for index, i in enumerate(winnower_data):
            if i[1]==0:
                pass
            else:
                x6_start=index
                break

        y6=y5+np.array([i[1] for i in winnower_data])

        x7_start=-1
        for index, i in enumerate(preprints_data):
            if i[1]==0:
                pass
            else:
                x7_start=index
                break

        y7=y6+np.array([i[1] for i in preprints_data])

        x8_start=-1
        for index, i in enumerate(wellcome_data):
            if i[1]==0:
                pass
            else:
                x8_start=index
                break

        y8=y7+np.array([i[1] for i in wellcome_data])

        ax.fill_between(x1,y1,0,color='#EC5f67')
        ax.fill_between(x1[x3_start:],y1[x3_start:],y3[x3_start:],color='#F99157')
        ax.fill_between(x1[x4_start:],y3[x4_start:],y4[x4_start:],color='#FAC863')
        ax.fill_between(x1[x5_start:],y4[x5_start:],y5[x5_start:],color='#99C794')
        ax.fill_between(x1[x6_start:],y5[x6_start:],y6[x6_start:],color='#5FB3B3')
        ax.fill_between(x1[x7_start:],y6[x7_start:],y7[x7_start:],color='#6699CC')
        ax.fill_between(x1[x8_start:],y7[x8_start:],y8[x8_start:],color='#C594C5')
        
        ax.plot([],[],color='#EC5f67',linewidth=15,label='arXiv q-bio')
        ax.plot([],[],color='#F99157',linewidth=15,label='F1000Research')
        ax.plot([],[],color='#FAC863',linewidth=15,label='PeerJ Preprints')
        ax.plot([],[],color='#99C794',linewidth=15,label='bioRxiv')
        ax.plot([],[],color='#5FB3B3',linewidth=15,label='The Winnower')
        ax.plot([],[],color='#6699CC',linewidth=15,label='preprints.org')
        ax.plot([],[],color='#C594C5',linewidth=15,label='Wellcome Open Research')



        ax.tick_params(axis='x',length=0,width=2,direction='out',labelsize=22,pad=10)
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
        ax.set_xticklabels(['2014','2015','2016','2017'])
        ax.set_xlim(0,len(x1)-1)
        ax.set_title(subject +' Preprints per Month',fontsize=30,y=1.01)
        ax.legend(loc=2,frameon=False,fontsize=21,ncol=4)
        canvas=FigureCanvasAgg(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        fig.clf()
        plt.close(fig)
        del canvas
        gc.collect()
        return response


def query_plot(request):
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    import gc
    import datetime
    import numpy as np
    if not request.META.get('HTTP_REFERER',False):
        return HttpResponse('something is wrong')
    else:
        raw=request.META.get('HTTP_REFERER').replace('+',' ').replace('%20',' ').replace('%2C',',').replace('%26','&').replace('%22','"')
        query=raw.split('query=')[1]
        from papers.views import *
        mystring=get_mystring(str(query))
        final_query=[]
        for i in mystring:
            if i in stopwords:
                pass
            else:
                final_query.append(i)
        if final_query!=[]:
            qs=Article.objects.filter(tiab_query(final_query)).filter(pub_date__gte=datetime.date(2014,1,1))
            data=[(i.pub_date,i.link) for i in qs]
            all_dates=[]
            current_year=datetime.date.today().year
            current_month=datetime.date.today().month
            for i in range(2014,current_year):
                for j in range(1,13):
                    all_dates.append((i,j))
            for i in range(1,current_month+1):
                all_dates.append((current_year,i))
            arxiv_counts={}
            peerj_counts={}
            f1000research_counts={}
            biorxiv_counts={}
            preprints_counts={}
            winnower_counts={}
            wellcome_counts={}
            for i in data:
                date=(i[0].year,i[0].month)
                if 'arxiv.org' in i[1]:
                    arxiv_counts[date]=arxiv_counts.get(date,0)+1
                elif 'peerj.com' in i[1]:
                    peerj_counts[date]=peerj_counts.get(date,0)+1
                elif 'f1000research.com' in i[1]:
                    f1000research_counts[date]=f1000research_counts.get(date,0)+1
                elif 'biorxiv.org' in i[1]:
                    biorxiv_counts[date]=biorxiv_counts.get(date,0)+1
                elif 'preprints.org' in i[1]:
                    preprints_counts[date]=preprints_counts.get(date,0)+1
                elif 'thewinnower.com' in i[1]:
                    winnower_counts[date]=winnower_counts.get(date,0)+1
                elif 'wellcomeopenresearch.org' in i[1]:
                    wellcome_counts[date]=wellcome_counts.get(date,0)+1
                else:
                    pass

            for i in all_dates:
                if i not in arxiv_counts:
                    arxiv_counts[i]=0
                if i not in peerj_counts:
                    peerj_counts[i]=0
                if i not in f1000research_counts:
                    f1000research_counts[i]=0
                if i not in biorxiv_counts:
                    biorxiv_counts[i]=0
                if i not in preprints_counts:
                    preprints_counts[i]=0
                if i not in winnower_counts:
                    winnower_counts[i]=0
                if i not in wellcome_counts:
                    wellcome_counts[i]=0

            
            arxiv_data=sorted(zip(arxiv_counts.keys(),arxiv_counts.values()))
            peerj_data=sorted(zip(peerj_counts.keys(),peerj_counts.values()))
            f1000research_data=sorted(zip(f1000research_counts.keys(),f1000research_counts.values()))
            biorxiv_data=sorted(zip(biorxiv_counts.keys(),biorxiv_counts.values()))
            preprints_data=sorted(zip(preprints_counts.keys(),preprints_counts.values()))
            winnower_data=sorted(zip(winnower_counts.keys(),winnower_counts.values()))
            wellcome_data=sorted(zip(wellcome_counts.keys(),wellcome_counts.values()))
                
                                                                      
            fig=Figure(figsize=(22.62372, 12),facecolor='white')
            ax=fig.add_subplot(111,)
            fig.subplots_adjust(bottom=.1)
            fig.subplots_adjust(left=.04)
            fig.subplots_adjust(right=.98)
            fig.subplots_adjust(top=.96)
            x1=range(len(all_dates))
            y1=np.array([i[1] for i in arxiv_data])

            x3_start=-1
            for index, i in enumerate(f1000research_data):
                if i[1]==0:
                    pass
                else:
                    x3_start=index
                    break

            y3=y1+np.array([i[1] for i in f1000research_data])

            x4_start=-1
            for index, i in enumerate(peerj_data):
                if i[1]==0:
                    pass
                else:
                    x4_start=index
                    break

            y4=y3+np.array([i[1] for i in peerj_data])

            x5_start=-1
            for index, i in enumerate(biorxiv_data):
                if i[1]==0:
                    pass
                else:
                    x5_start=index
                    break

            x6_start=-1
            y5=y4+np.array([i[1] for i in biorxiv_data])

            for index, i in enumerate(winnower_data):
                if i[1]==0:
                    pass
                else:
                    x6_start=index
                    break

            y6=y5+np.array([i[1] for i in winnower_data])

            x7_start=-1
            for index, i in enumerate(preprints_data):
                if i[1]==0:
                    pass
                else:
                    x7_start=index
                    break

            y7=y6+np.array([i[1] for i in preprints_data])

            x8_start=-1
            for index, i in enumerate(wellcome_data):
                if i[1]==0:
                    pass
                else:
                    x8_start=index
                    break

            y8=y7+np.array([i[1] for i in wellcome_data])

            ax.fill_between(x1,y1,0,color='#EC5f67')
            ax.fill_between(x1[x3_start:],y1[x3_start:],y3[x3_start:],color='#F99157')
            ax.fill_between(x1[x4_start:],y3[x4_start:],y4[x4_start:],color='#FAC863')
            ax.fill_between(x1[x5_start:],y4[x5_start:],y5[x5_start:],color='#99C794')
            ax.fill_between(x1[x6_start:],y5[x6_start:],y6[x6_start:],color='#5FB3B3')
            ax.fill_between(x1[x7_start:],y6[x7_start:],y7[x7_start:],color='#6699CC')
            ax.fill_between(x1[x8_start:],y7[x8_start:],y8[x8_start:],color='#C594C5')
            
            ax.plot([],[],color='#EC5f67',linewidth=15,label='arXiv q-bio')
            ax.plot([],[],color='#F99157',linewidth=15,label='F1000Research')
            ax.plot([],[],color='#FAC863',linewidth=15,label='PeerJ Preprints')
            ax.plot([],[],color='#99C794',linewidth=15,label='bioRxiv')
            ax.plot([],[],color='#5FB3B3',linewidth=15,label='The Winnower')
            ax.plot([],[],color='#6699CC',linewidth=15,label='preprints.org')
            ax.plot([],[],color='#C594C5',linewidth=15,label='Wellcome Open Research')


            ax.tick_params(axis='x',length=0,width=2,direction='out',labelsize=22,pad=10)
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
            ax.set_xticklabels(['2014','2015','2016','2017'])
            ax.set_xlim(0,len(x1)-1)
            ax.set_title(''.join([i+j for i,j in zip(final_query,[' ']*len(final_query))])+'Preprints per Month',fontsize=30,y=1.01)
            ax.legend(loc='upper left',frameon=False,fontsize=21,ncol=4)
            canvas=FigureCanvasAgg(fig)
            response=HttpResponse(content_type='image/png')
            canvas.print_png(response)
            fig.clf()
            plt.close(fig)
            del canvas
            gc.collect()
            return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

