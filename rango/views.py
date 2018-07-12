from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
# Create your views here.

def index(request):

   category_list = Category.objects.order_by("-likes")[:5]
   return render(request, 'rango/index.html', {'categories' : category_list})

def about(request):
    return render(request, 'rango/about.html', {})

def category(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
    except Category.DoesNotExist:
        category = None
        pages = None
    return render(request, 'rango/category.html', {"category": category, "pages": pages})

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category= None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print(form.errors)

    return render(request, 'rango/add_page.html', {"form": form, "category": category})




