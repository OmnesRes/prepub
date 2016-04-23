from django.http import  Http404, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext


from papers.models import Article
from papers.models import Author
from papers.models import Affiliation
from papers.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


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

def home(request):
    return render(request, 'home.html')

def my_help(request):
    return render(request, 'help.html')

def advanced_search(request):
    return render(request, 'advanced_search.html')


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
            raw=request.GET['q']
            if raw!='':
                articles=Article.objects.filter(tags__name=raw).order_by('-pub_date')
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


def search_author(request):
    if request.META.get('HTTP_REFERER',False):
        if 'q' in request.GET:
            raw=request.GET['q']
            if raw!='':
                author=raw
                first_name=author.split()[0]
                last_name=author.split()[-1]
                if len(author.split())==2:
                    middle_name=''
                else:
                    middle_name=author.replace(first_name+' ','').replace(' '+last_name,'').strip()
                middle_name=author.strip(first_name).strip(last_name).strip()
                ##lenient on middle due to punctuation differences
                if middle_name:
                    articles=Article.objects.filter(authors__first=first_name,authors__last=last_name,authors__middle__startswith=middle_name[0]).order_by('-pub_date')
                else:
                    articles=Article.objects.filter(authors__first=first_name,authors__last=last_name).order_by('-pub_date')
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
                        qs=Article.objects.filter(tiab_query(request.GET['tiab1']))
                    else:
                        qs=qs.filter(tiab_query(request.GET['tiab1']))
                if request.GET['tiab2']:
                    if qs==None:
                        qs=Article.objects.filter(tiab_query(request.GET['tiab2']))
                    else:
                        qs=qs.filter(tiab_query(request.GET['tiab2']))
                if request.GET['aff1']:
                    if qs==None:
                        qs=Article.objects.filter(affiliations__name__icontains=request.GET['aff1'])
                    else:
                        qs=qs.filter(affiliations__name__icontains=request.GET['aff1'])
                if request.GET['aff2']:
                    if qs==None:
                        qs=Article.objects.filter(affiliations__name__icontains=request.GET['aff2'])
                    else:
                        qs=qs.filter(affiliations__name__icontains=request.GET['aff2'])
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



def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

