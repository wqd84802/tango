from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def index(request):

   category_list = Category.objects.order_by("-likes")[:5]
   return render(request, 'rango/index.html', {'categories' : category_list})

def about(request):
    return render(request, 'rango/about.html', {})

def show_category(request, category_name_slug):
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
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    return render(request, 'rango/add_page.html', {"form": form, "category": category})


def register(request):

    registed = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES['picture']:
                profile.save()

                registed = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',{
        'user_form': user_form,
        'profile_form': profile_form,
        'registed': registed
    } )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                return HttpResponse("The user is invalid")
        else:

            print("the accont is avalid--{}--{}--".format(username, password))
            return HttpResponse('avalid account')

    else:
        return render(request, 'rango/login.html', {})


