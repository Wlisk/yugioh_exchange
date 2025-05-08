#from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests

from models.yugioh_card import YugiohCardRead

HOST = '127.0.0.1'
PORT = 8001

URL = f'http://{HOST}:{PORT}'

def initial(request):
  return render(request, 'initial_screen.html')

def select(request):

  response = requests.get(URL)
  data = response.json() 

  '''
  query = request.GET.get('q') # Faz a pesquisa na API (ainda precisa implementar corretamente)

  if query:
    response = requests.get(URL, params={'q': query})
  else:
    response = requests.get(URL)

  data = response.json() 

  '''

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