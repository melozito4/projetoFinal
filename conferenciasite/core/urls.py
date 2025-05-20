from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('submit/', views.submit_abstract, name='submit'),  # <- AQUI está a correção
    path('logout/', views.logout_view, name='logout'),
]
