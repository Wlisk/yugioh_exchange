from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from models.yugioh_card import YugiohCardRead, CardType, MonsterType
from db.main import card_operations, offer_operations, exchange_operations

HOST = '127.0.0.1'
PORT = 8001

URL = f'http://{HOST}:{PORT}'

PATHS = {
  'home': '/',
  'list': '/cards',
}

#########################################################################################
def home(request):
  """Home page"""

  template_name = 'home_screen.html'
  if request.htmx:
    template_name = f'{template_name}#home-partial'

  return render(request, template_name)

#########################################################################################
def select(request):
  """Page to select cards for exchange"""
  """
  filter_type = request.GET.get('filter_type', 'name')
  query = request.GET.get('q', '').lower()

  #result = card_operations.select_card(name= "Blue-Eyes White Dragon", card_type = CardType.MONSTER, monster_type = MonsterType.DRAGON)
  #result = offer_operations.get_offer_from_id(1)
  #result = exchange_operations.get_exchange()
  #print(result)
  #for i in result:
  #  print(i)
  #  print(i.offer_id)
  #  print(i.user_name)
  #  print(i.given_card_name)
  #  print(i.wants_card_name)
  #  print("\n")
  #
  card_type_form = request.GET.get('card_type_select', None)  
  monster_type_form = request.GET.get('monster_type_select', None)
  
  if filter_type == 'name' and query:
    result = card_operations.select_card(name=query)
  elif filter_type == 'card_type' and card_type_form:
    result = card_operations.select_card(card_type=CardType[card_type_form.upper()])
  elif filter_type == 'monster_type' and monster_type_form:
    result = card_operations.select_card(monster_type=MonsterType[monster_type_form.upper()])
  else:
    
  """
  result = card_operations.select_card()
  """
  if request.method == 'POST':
    selected_cards = request.POST.getlist('cards') # Faz uma lista com os ids das cartas que foram marcadas no checkbox
    selected_cards = list(map(int, selected_cards)) 

    response = redirect('/make_offer', {'selected_cards': selected_cards})
    response.set_cookie('selected_card_names', json.dumps(selected_cards))
    return response
  """
  template_name = 'select_cards.html'
  if request.htmx:
    template_name = f'{template_name}#select-partial'

  return render(request, template_name, {'cards':  result})

#########################################################################################
def make_offer(request):
  """Page to make an exchange of cards"""
  user_cards = card_operations.select_card()
  cards_wants = []

  if request.method == 'POST':
    try:
      json_cards = json.loads(request.body)
      ncards = json_cards['cards']
    except json.JSONDecodeError:
      ncards = request.POST.get('selected_cards', '[]')
    
    if isinstance(ncards, list):
      cards_wants = [card for card in user_cards if str(card.id) in ncards]

  else:
    selected_names_str = request.COOKIES.get('selected_card_names', '[]')
    selected_names = json.loads(selected_names_str)
    
    for name in selected_names:
      cards = list(card_operations.select_card(name=name))
      if cards:
        cards_wants.append(cards[0]) 
  
  template_name = 'make_offer.html'
  if request.htmx:
    template_name = f'{template_name}#make-offer-partial'

  return render(
    request, 
    template_name, 
    {
      'cards_want': cards_wants, 
      'user_cards': user_cards,
    }
  )

#########################################################################################
def exchanges(request):
  """Page to list the available exchange offers"""

  template_name = 'exchanges.html'
  if request.htmx:
    template_name = f'{template_name}#exchange-partial'

  return render(request, template_name)

#########################################################################################
def card_list(request):
  """Page to list all Yu-gi-oh cards"""
  response = requests.get(f"{URL}/{PATHS['list']}") 
  cards: list[YugiohCardRead] = response.json() 

  template_name = 'card_list.html'
  if request.htmx:
    template_name = f'{template_name}#cards-partial'

  return render(
    request, 
    template_name, 
    {
      'cards': cards
    }
  )