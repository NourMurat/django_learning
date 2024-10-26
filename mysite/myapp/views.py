from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def index(request):
    items = Product.objects.all()
    return HttpResponse(items)

def contacts(request):
    return render(request, "myapp/contacts.html")

def about(request):
    return HttpResponse("ABOUT")