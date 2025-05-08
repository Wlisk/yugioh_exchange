from django.urls import path
from . import views

urlpatterns = [
  path('select/', views.select, name='select'),
  path('make_exchange/', views.make_exchange, name='make_exchange'),
  path('exchanges/', views.exchanges, name='exchanges'),
]