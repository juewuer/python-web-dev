from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List


# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id=None):
    if list_id is None:
        items = Item.objects.all()
    else:
        items = Item.objects.filter(list=list_id)
    return render(request, 'list.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    res = Item.objects.create(text=request.POST["item_text"], list=list_)
    print(f'{res =}')
    print(f'{Item.objects.count() = }')
    return redirect(f'/lists/{list_.id}/')
