from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('/login/')),  # redireciona / para /login/
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]

path('index/', views.index_view, name='index'),
