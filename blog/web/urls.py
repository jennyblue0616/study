from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^gbook/', views.gbook, name='gbook'),
    url(r'^info/', views.info, name='info'),
    url(r'^list/', views.list, name='list'),
    url(r'^infopic/', views.infopic, name='infopic'),
    url(r'^share/', views.share, name='share'),
    url(r'^about/', views.about, name='about'),
    url(r'^article/(\d+)/', views.article, name='article'),
]