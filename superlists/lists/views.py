from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List


# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id=None):
    data = {}
    if list_id is None:
        items = Item.objects.all()
        data['items'] = items
    else:
        items = Item.objects.filter(list=list_id)
        list_ = List.objects.get(id=list_id)
        data['items'] = items
        data['list'] = list_

    return render(request, 'list.html', data)


def new_list(request):
    list_ = List.objects.create()
    res = Item.objects.create(text=request.POST["item_text"], list=list_)
    print(f'{res =}')
    print(f'{Item.objects.count() = }')
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f'/lists/{list_.id}/')
