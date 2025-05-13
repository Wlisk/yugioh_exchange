from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home_screen'),
  path('select/', views.select, name='select'),
  path('make_exchange/', views.make_exchange, name='make_exchange'),
  path('exchanges/', views.exchanges, name='exchanges'),
  path('card_list/', views.card_list, name='card_list'),
]