from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name='index'),
    path('rango/about/', views.about, name='about'),
    path('rango/category/<slug:category_name_slug>/', views.show_category, name='category'),
    path('rango/add_category/', views.add_category, name='add_category'),
    path('rango/category/<slug:category_name_slug>/add_page', views.add_page, name='add_page'),
    path('rango/register/', views.register, name='register'),
    path('rango/login/', views.user_login, name='login'),
    path('rango/restriced/', views.register, name='restriced'),
    path('rango/logout/', views.user_logout, name='logout'),
]