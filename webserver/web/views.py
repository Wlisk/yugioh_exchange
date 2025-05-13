from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from models.yugioh_card import YugiohCardRead, CardType, MonsterType
from db.main import card_operations

HOST = '127.0.0.1'
PORT = 8001

URL = f'http://{HOST}:{PORT}'

#########################################################################################
def home(request):
  return render(request, 'home_screen.html')

#########################################################################################
def select_cards(request):
  filter_type = request.GET.get('filter_type', 'name')
  query = request.GET.get('q', '').lower()
  card_type_form = request.GET.get('card_type_select', None)  
  monster_type_form = request.GET.get('monster_type_select', None)
  
  if filter_type == 'name' and query:
    result = card_operations.select_card(name=query)
  elif filter_type == 'card_type' and card_type_form:
    result = card_operations.select_card(card_type=CardType[card_type_form.upper()])
  elif filter_type == 'monster_type' and monster_type_form:
    result = card_operations.select_card(monster_type=MonsterType[monster_type_form.upper()])
  else:
    result = card_operations.select_card()

  if request.method == 'POST':
    
    selected_cards = request.POST.getlist('cards')
    response = redirect('/make_offer')
    response.set_cookie('selected_card_names', json.dumps(selected_cards))

    return response

  return render(request, 'select_cards.html', {'cards': result})

#########################################################################################
def make_offer(request):
  selected_names_str = request.COOKIES.get('selected_card_names', '[]')
  selected_names = json.loads(selected_names_str)
  cards_wants = []

  for name in selected_names:
    cards = list(card_operations.select_card(name=name))
    if cards:
      cards_wants.append(cards[0]) 

  user_cards = card_operations.select_card()

  if request.method == 'POST':
    cards_given = request.POST.getlist('cards')
    print(f"Cards given: {cards_given}")
    return redirect('/select')

  return render(request, 'make_offer.html', {'cards_want': cards_wants, 'user_cards': user_cards})

#########################################################################################
def exchanges(request):
  return render(request, 'exchanges.html')

#########################################################################################
def card_list(request):
  response = requests.get(URL)
  data: list[YugiohCardRead] = response.json() 

  return render(
    request, 
    'card_list.html', 
    {
      'cards': data
    }
  )