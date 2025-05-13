#from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests

from models.yugioh_card import YugiohCardRead
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
  query = request.GET.get('q', '').lower()

  #result = card_operations.select_card(name= "Blue-Eyes White Dragon", card_type = CardType.MONSTER, monster_type = MonsterType.DRAGON)
  result = card_operations.select_card(name="drag")
  for i in result:
    print(i)
    print(i.name)

  response = requests.get(URL)
  cards = response.json() 

  # Função de pesquisa funcional mas temporária 
  if query:
    cards = [card for card in cards if query in card['name'].lower()]
  print(query)

  if request.method == 'POST':
    ids = request.POST.getlist('cards') # Faz uma lista com os ids das cartas que foram marcadas no checkbox
    ids = list(map(int, ids)) 
    print(ids)
    return redirect('/make_exchange')
  
  template_name = 'select_cards.html'
  if request.htmx:
    template_name = f'{template_name}#select-partial'

  return render(request, template_name, {'cards': cards})

#########################################################################################
def make_exchange(request):
  """Page to make an exchange of cards"""
  # TODO: Alguma forma de armazenar as cartas selecionadas pelo usuário na tela anterior

  template_name = 'make_exchange.html'
  if request.htmx:
    template_name = f'{template_name}#make-exchange-partial'

  return render(request, template_name)

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