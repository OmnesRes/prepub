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




def home(request):
    return render(request, 'home.html')

def my_help(request):
    return render (request, 'help.html')

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
                articles=perform_query(all_terms)
                if articles.exists():
                    paginator = Paginator(articles, 20)
                    page = request.GET.get('page')
                    try:
                        Articles = paginator.page(page)
                    except PageNotAnInteger:
                        Articles = paginator.page(1)
                    except EmptyPage:
                        Articles = paginator.page(paginator.num_pages)
                    return render_to_response('search_results.html', {'articles': Articles,'raw':raw,'search':pretty_terms(all_terms)})
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
                articles=Article.objects.filter(tags__name=raw)
                if articles.exists():
                    paginator=Paginator(articles, 20)
                    page=request.GET.get('page')
                    try:
                        Articles = paginator.page(page)
                    except PageNotAnInteger:
                        Articles = paginator.page(1)
                    except EmptyPage:
                        Articles = paginator.page(paginator.num_pages)
                    return render_to_response('search_results.html', {'articles':Articles,'raw':raw})
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
                middle_name=author.strip(first_name).strip(last_name).strip()
                ##lenient on middle due to punctuation differences
                if middle_name:
                    articles=Article.objects.filter(authors__first=first_name,authors__last=last_name,authors__middle__startswith=middle_name[0])
                else:
                    articles=Article.objects.filter(authors__first=first_name,authors__last=last_name)
                if articles.exists():
                    paginator=Paginator(articles, 20)
                    page=request.GET.get('page')
                    try:
                        Articles = paginator.page(page)
                    except PageNotAnInteger:
                        Articles = paginator.page(1)
                    except EmptyPage:
                        Articles = paginator.page(paginator.num_pages)
                    return render_to_response('search_results.html', {'articles':Articles,'raw':raw})
                else:
                    return render(request, 'search_results.html', {'articles':False})
            else:
                return redirect(home)
        else:
            return redirect(home)
    else:
        return redirect(home)






def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

