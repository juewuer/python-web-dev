from django.urls import path
from lists import views

urlpatterns = [
    path('all/', views.view_list),
]