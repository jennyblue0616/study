from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    #首页
    url(r'^index/', (views.index), name='index'),
    url(r'^logout/', (views.logout), name='logout'),

]