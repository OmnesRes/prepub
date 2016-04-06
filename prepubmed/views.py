from django.http import  Http404, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.shortcuts import redirect



from papers.models import Article
from papers.models import Author
from papers.models import Affiliation
from papers.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'home.html')



def search_results(request):
    if request.META.get('HTTP_REFERER',False):
        if 'q' in request.GET:
            raw=request.GET['q'].strip()
            if raw!='':
                articles=Article.objects.filter(abstract__contains=raw)
                if articles.exists():
                    return render(request, 'search_results.html', {'articles':articles})
                else:
                    return render(request, 'search_results.html', {'articles':False})
            else:
                return redirect(home)
        else:
            return redirect(home)
    else:
        return redirect(home)
