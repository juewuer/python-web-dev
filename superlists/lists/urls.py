from django.urls import path,re_path
from lists import views

urlpatterns = [
    #path('all/', views.view_list),
    re_path(r'^(\d*)/$', views.view_list),
    re_path(r'^(\d*)/add_item$', views.add_item),
    path('new', views.new_list),
]
