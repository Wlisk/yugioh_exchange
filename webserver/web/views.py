#from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests

from models.yugioh_card import YugiohCardRead, CardType, MonsterType
from db.main import card_operations, offer_operations

HOST = '127.0.0.1'
PORT = 8001

URL = f'http://{HOST}:{PORT}'

#########################################################################################
def home(request):
  return render(request, 'home_screen.html')

#########################################################################################
def select(request):
  filter_type = request.GET.get('filter_type', 'name')
  query = request.GET.get('q', '').lower()

  #result = card_operations.select_card(name= "Blue-Eyes White Dragon", card_type = CardType.MONSTER, monster_type = MonsterType.DRAGON)
  #result = offer_operations.get_offer_from_id(1)
  #print(result)
  #for i in result:
  #  print(i)
  #  print(i.offer_id)
  #  print(i.user_name)
  #  print(i.given_card_name)
  #  print(i.wants_card_name)
  #  print("\n")
  #
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

    return redirect('/make_exchange')

  return render(request, 'select_cards.html', {'cards': result})

#########################################################################################
def make_exchange(request):
  # Alguma forma de armazenar as cartas selecionadas pelo usuário na tela anterior
  return render(request, 'make_exchange.html')

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