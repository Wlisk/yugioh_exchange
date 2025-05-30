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
  'offers': '/offers',
}

#########################################################################################
def home(request):
  template = 'home_screen.html' if request.htmx else 'base.html'
  context = {'page': 'home'} if not request.htmx else {}
  return render(request, template, context)

#########################################################################################
def select(request):
  result = card_operations.select_card()

  template = 'select_cards.html' if request.htmx else 'base.html'
  context = {'cards': result} if not request.htmx else {'cards': result}
  if not request.htmx:
    context['page'] = 'select'
  return render(request, template, context)

#########################################################################################
def make_offer(request):
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

  template = 'make_offer.html' if request.htmx else 'base.html'
  context = {
    'cards_want': cards_wants,
    'user_cards': user_cards
  }
  if not request.htmx:
    context['page'] = 'make_offer'

  return render(request, template, context)

#########################################################################################
def exchanges(request):
  template = 'exchanges.html' if request.htmx else 'base.html'
  context = {} if request.htmx else {'page': 'exchanges'}
  return render(request, template, context)

#########################################################################################
def card_list(request):
  response = requests.get(f"{URL}/{PATHS['list']}")
  cards: list[YugiohCardRead] = response.json()

  template = 'card_list.html' if request.htmx else 'base.html'
  context = {'cards': cards}
  if not request.htmx:
    context['page'] = 'card_list'

  return render(request, template, context)

#########################################################################################
def set_user(request):
  if request.method != 'POST':
    return HttpResponse(status=400)

  user_id = request.POST.get('user_id')
  response = HttpResponse(status=200)
  response.set_cookie('user_id', user_id, max_age=3600*24*7)
  response.content = json.dumps({'user_id': user_id})
  return response

#########################################################################################
def offers(request):
  user_id = request.COOKIES.get('user_id', '1') # default to one

  response = requests.get(f'{URL}/user/{user_id}/cards')
  cards: list[YugiohCardRead] = response.json()

  # Get offers for the current user
  offers_response = requests.get(
    f"{URL}/{PATHS['offers']}",
    params={'user_id': user_id}
  )
  
  offers = []
  if offers_response.status_code == 200:
    raw_offers = offers_response.json()
    # Transform the offers to include only necessary owner info
    offers = [{
      'offer_id': offer['offer']['id'],
      'owner': {
        'id': offer['owner']['id'],
        'name': offer['owner']['name']
      },
      'cards_given': offer['cards_given'],
      'cards_wanted': offer['cards_wanted']
    } for offer in raw_offers]

  template = 'offers.html' if request.htmx else 'base.html'
  context = {
    'cards': cards,
    'offers': offers,
    'user_id': user_id
  }
  
  if not request.htmx:
    context['page'] = 'offers'

  return render(request, template, context)

#########################################################################################
def respond_offer(request):
  if request.method != 'POST':
    return HttpResponse(status=400)

  try:
    offer_id = int(request.POST.get('offer_id'))
    accepted = request.POST.get('accepted') == 'true'
    user_id = request.COOKIES.get('user_id', '1')
  except (ValueError, TypeError):
    return HttpResponse(status=400)

  # Make API call to respond to offer
  response = requests.post(
    f"{URL}/offers/respond",
    params={
      "offer_id": offer_id,
      "user_id": int(user_id),
      "accepted": accepted
    }
  )

  if response.status_code == 200:
    data = response.json()
    if data.get('ok'):
      if accepted:
        return HttpResponse(
          status=200,
          content=json.dumps({"status": "ok"}),
          content_type="application/json"
        )
      else:
        return HttpResponse(
          status=200,
          content=json.dumps({"status": "refused"}),
          content_type="application/json"
        )
    else:
      return HttpResponse(
        status=400,
        content=json.dumps({"status": "error", "message": data.get("message", "Unknown error")}),
        content_type="application/json"
      )
  elif response.status_code == 400:
    error_data = response.json()
    if "not found in your collection" in error_data.get("detail", ""):
      return HttpResponse(
        status=400,
        content=json.dumps({"status": "user_has_no_card"}),
        content_type="application/json"
      )
    return HttpResponse(
      status=400,
      content=json.dumps({"status": "error", "message": error_data.get("detail", "Bad request")}),
      content_type="application/json"
    )
  else:
    return HttpResponse(
      status=response.status_code,
      content=json.dumps({"status": "error", "message": "Server error"}),
      content_type="application/json"
    )
