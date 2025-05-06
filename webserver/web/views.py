#from django.http import HttpResponse
from django.shortcuts import render
import requests

from models.yugioh_card import YugiohCardRead

HOST = '127.0.0.1'
PORT = 8001

URL = f'http://{HOST}:{PORT}'

def index(request):
  #return HttpResponse("Hello, world. You're at the index of the web server.")
  response = requests.get(URL)
  data: list[YugiohCardRead] = response.json() 

  return render(
    request, 
    'cards.html', 
    {
      'cards': data
    }
  )