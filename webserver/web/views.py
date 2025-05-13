#from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests

from models.yugioh_card import YugiohCardRead, CardType, MonsterType
from db.main import card_operations

HOST = '127.0.0.1'
PORT = 8001

URL = f'http://{HOST}:{PORT}'

def home(request):
  return render(request, 'home_screen.html')

def select(request):

  query = request.GET.get('q', '').lower()

  #result = card_operations.select_card(name= "Blue-Eyes White Dragon", card_type = CardType.MONSTER, monster_type = MonsterType.DRAGON)
  #result = card_operations.select_card(card_type = CardType.TRAP)
  #for i in result:
  #  print(i)
  #  print(i.name)

  response = requests.get(URL)
  data = response.json() 

  # Função de pesquisa funcional mas temporária 
  if query:
    data = [card for card in data if query in card['name'].lower()]

  print(query)

  if request.method == 'POST':
    
    ids = request.POST.getlist('cards') # Faz uma lista com os ids das cartas que foram marcadas no checkbox
 
    ids = list(map(int, ids)) 

    print(ids)

    return redirect('/make_exchange')

  return render(request, 'select_cards.html', {'cards': data})

def make_exchange(request):

  # Alguma forma de armazenar as cartas selecionadas pelo usuário na tela anterior

  return render(request, 'make_exchange.html')

def exchanges(request):
  return render(request, 'exchanges.html')