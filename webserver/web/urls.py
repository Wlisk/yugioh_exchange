from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('select/', views.select, name='select'),
  path('make_offer/', views.make_offer, name='make_exchange'),
  path('exchanges/', views.exchanges, name='exchanges'),
  path('card_list/', views.card_list, name='card_list'),
]