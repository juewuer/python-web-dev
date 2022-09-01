from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item
# Create your views here.
def home_page(request):
    #return HttpResponse('<html><title>To-Do Lists</title></html>')
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')

        #return HttpResponse()
    items = Item.objects.all()
    #return render(request, 'home.html', {'new_item_text': new_item_text})
    return render(request, 'home.html', {'items': items})