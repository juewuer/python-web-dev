from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from lists.models import Item, List
from lists.forms import *


# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


@csrf_exempt
def view_list(request, list_id=None):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    data = {}
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST["text"], list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


@csrf_exempt
def new_list(request):
    form = ItemForm(data=request.POST)
    print(f'{form = }, {form.is_valid() = }')
    if form.is_valid():
        print(f'new_list: to create form')
        list_ = List.objects.create()
        print(f'new_list: {request.POST =}')
        item = Item.objects.create(text=request.POST["text"], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})
