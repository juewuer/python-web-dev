from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item


# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    res = Item.objects.create(text= request.POST["item_text"])
    print(f'{res =}')
    print(f'{Item.objects.count() = }')
    return redirect('/lists/all/')