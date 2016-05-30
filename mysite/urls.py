"""prepubmed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^search_results/',views.search_results),
    url(r'^search_tag/',views.search_tag),
    url(r'^search_author/',views.search_author),
    url(r'^help/',views.my_help),
    url(r'^advanced_search/',views.advanced_search),
    url(r'^ad_search_results/',views.advanced_search_results),
    url(r'^grim_test/',views.grim_test),
    url(r'^make_plot/',views.make_plot),
    url(r'^grim_plot/',views.grim_plot),
    url(r'^general_grim/',views.general_grim),
    url(r'^rss_feed/',views.rss_feed),
    url(r'^articles/(.{1,50})/rss/',views.RSSFeed()),
    
]
