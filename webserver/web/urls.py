from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('favicon.ico', views.icon, name='icon'),
  path('login/', views.login_account, name='login'),
  path('create_account/', views.create_account, name='create_account'),
  path('logout/', views.logout_account, name='logout'),
  path('select/', views.select, name='select'),
  path('select/<str:filter>/<str:isSideLeft>/', views.select_filter, name='select_filter'),
  path('make_offer/<str:cardsWanted>/<str:cardsOffered>', views.make_offer, name='make_offer'),
  path('exchanges/', views.exchanges, name='exchanges'),
  path('card_list/', views.card_list, {'list_type':'all'}, name='card_list'),
  path('card_list/<str:list_type>/', views.card_list, name='card_list_filtered'),
  path('card_list/<str:url>/user_cards/<int:card_id>/<str:isAdd>', views.change_user_card, name='change_user_card'),
  path('card_list/<str:url>/wishlist/<int:card_id>/<str:isAdd>', views.change_wishlist, name='change_wishlist'),
  path('set_user/', views.set_user, name='set_user'),
  path('offers/', views.offers, name='offers'),
  path('offers/respond/', views.respond_offer, name='respond_offer'),
]