from django.urls import path,re_path
from lists import views

urlpatterns = [
    path('all/', views.view_list),
    path('new', views.new_list),
    re_path(r'^(.*)/$', views.view_list),
]
