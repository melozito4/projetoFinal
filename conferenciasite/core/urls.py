from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('submit/', views.submit_abstract, name='submit'),
    path('logout/', views.logout_view, name='logout'),
    path('review/', views.ver_submissoes, name='ver_submissoes'),
    path('review/<int:resumo_id>/', views.ver_resumo, name='ver_resumo'),
    path('checkout/', views.checkout, name='checkout'),
    path('sucesso/', views.pagamento_sucesso, name='pagamento_sucesso'),
    path('evento/', views.evento_registo_view, name='evento_registo')
]
