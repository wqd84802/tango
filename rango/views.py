from django.shortcuts import render

# Create your views here.

def index(request):
    message = "This is my first django"
    return render(request, 'rango/index.html', {'message' : message})

def about(request):
    return render(request, 'rango/about.html', {})