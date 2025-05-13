#from django.http import HttpResponse
import json
from django.shortcuts import render, redirect
import requests

from models.yugioh_card import YugiohCardRead, CardType, MonsterType
from db.main import card_operations

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
  filter_type = request.GET.get('filter_type', 'name')
  query = request.GET.get('q', '').lower()

  #result = card_operations.select_card(name= "Blue-Eyes White Dragon", card_type = CardType.MONSTER, monster_type = MonsterType.DRAGON)
  
  '''
  for i in result:
    print(i)
    print(i.name)
  '''

  if query:
    if filter_type == 'name':
      result = card_operations.select_card(name=query)
    elif filter_type == 'card_type':
      result = card_operations.select_card(card_type=CardType[query.upper()])
    elif filter_type == 'monster_type':
      result = card_operations.select_card(monster_type=MonsterType[query.upper()])
  else:
    result = card_operations.select_card()

  if request.method == 'POST':
    selected_cards = request.POST.getlist('cards') # Faz uma lista com os ids das cartas que foram marcadas no checkbox
    selected_cards = list(map(int, selected_cards)) 
    # TODO: send select_cards with the redirect
    return redirect('/make_exchange', {'selected_cards': selected_cards})
  
  template_name = 'select_cards.html'
  if request.htmx:
    template_name = f'{template_name}#select-partial'

  return render(request, template_name, {'cards':  result})

#########################################################################################
def make_exchange(request):
  """Page to make an exchange of cards"""
  # TODO: Alguma forma de armazenar as cartas selecionadas pelo usuário na tela anterior
  json_cards = json.loads(request.body) if request.method == 'POST' else []

  # You could fetch the card objects here if needed
  cards = card_operations.select_card()
  selected_cards = [c for c in cards if str(c.id) in json_cards['cards']]

  template_name = 'make_exchange.html'
  if request.htmx:
    template_name = f'{template_name}#make-exchange-partial'

  return render(
    request, 
    template_name, 
    {
      'cards':  selected_cards, 
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