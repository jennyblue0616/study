from django.conf.urls import url

from back import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^index/', views.index, name='index'),
    url(r'^article/', views.article, name='article'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^category/', views.category, name='category'),
    url(r'^add_article/', views.add_article, name='add_article'),
    url(r'^update_article/(\d+)/', views.update_article, name='update-article'),
    url(r'^delete_article/(\d+)/', views.delete_article, name='delete-article'),


]