from django.http import  Http404, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.shortcuts import redirect

from papers.models import Article
def home(request):
    return render(request, 'home.html')



def search_results(request):
    if request.META.get('HTTP_REFERER',False):
        if 'q' in request.GET:
            raw=request.GET['q'].strip()
            if raw!='':
                abstracts=article.objects.filter(abstract__contains=raw)
                if abstracts.exists():
                    return render(request, 'search_results.html', {'abstract':article.objects.all()[0].abstract.split('\n')})
                else:
                    return render(request, 'search_results.html', {'abstract':False})
            else:
                return redirect(home)
        else:
            return redirect(home)
    else:
        return redirect(home)
