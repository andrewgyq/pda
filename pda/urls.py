from django.conf.urls import patterns, include, url
from django.contrib import admin
import os
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pda.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),

    url( r'^js/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': os.path.dirname(globals()["__file__"])+'/js' }
    ),

    url( r'^css/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': os.path.dirname(globals()["__file__"])+'/css' }
    ),

    url( r'^img/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': os.path.dirname(globals()["__file__"])+'/img' }
    ),

     url( r'^download/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': os.path.dirname(globals()["__file__"])+'/download' }
    ),

    url(r'^$', views.index, name='index'),

    url(r'^data', views.data, name='data'),

    url(r'^crawl', views.crawl, name='crawl'),

    url(r'^savetwitter', views.save, name='save'),

    url(r'^statistic', views.statistic, name='statistic'),

    url(r'^sentiment', views.sentiment, name='sentiment'),

    url(r'^getData', views.get_data, name='getData'),

    url(r'^wordcloud', views.wordcloud, name='wordcloud'),

    url(r'^getwordcloud', views.get_wordcloud, name='getwordcloud'),

    url(r'^getstatistic', views.get_statistic, name='getstatistic'),

    url(r'^getsentiment', views.get_sentiment, name='getsentiment'),

    url(r'^savesina', views.savesina, name='savesina'),

    url(r'^removedb', views.removedb, name='removedb'),



)
