from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
import requests
import json
from models.user import User
from models.yugioh_card import YugiohCardRead, CardType, MonsterType
from db.main import card_operations, user_operations, offer_operations, exchange_operations
from .decorators import user_login_required

HOST = '127.0.0.1'
PORT = 8001

URL = f'http://{HOST}:{PORT}'

PATHS = {
  'home': '/',
  'list': '/cards',
  'offers': '/offers',
}

#########################################################################################
def create_account(request):
  if request.method == 'POST':
    user_name = request.POST.get('name','')
    password = request.POST.get('password','')
    password_confirm = request.POST.get('passwordConfirm','')

    if password != password_confirm:
      return render(request, 'base.html', {"page": "create_account", 'error': 'As senhas não conferem.'})
    else:
      existing_users = user_operations.get_user(name=user_name)
      if existing_users:
        return render(request, 'base.html', {"page": "create_account", 'error': 'Usuário já existe.'})
      else:
        user_operations.create_user(name=user_name, password=password)
        return render(request, 'base.html', {"page": "login"})
  elif request.htmx:
    return render(request, 'create_account.html')
  else:
    return render(request, 'base.html', context={"page": "create_account"})


#########################################################################################
@never_cache
def home(request):
  if request.htmx:
    return render(request, 'home.html')

  return render(request, 'base.html')

def icon(request):
  return redirect("static/favicon.png", permanent=True)

#########################################################################################
@never_cache
def login_account(request):
  if request.method == 'POST':
    user_name = request.POST.get('name', '')
    password = request.POST.get('password', '')
    existing_users = user_operations.get_user(name=user_name)
    if not existing_users:
      return render(request, 'base.html', {"page": "login", 'error': 'Usuário não encontrado.'})
    elif existing_users[0].password != password:
      return render(request, 'base.html', {"page": "login", 'error': 'Senha incorreta.'})
    else:
      user = existing_users[0]
      response = redirect('offers')
      response.set_cookie('user_id', user.id, max_age=3600*24*7)
      return response
  elif request.htmx:
    return render(request, 'login.html')
  else:
     return render(request, 'base.html', context={"page": "login"})
 
##########################################################################################
def logout_account(request):
  response = HttpResponse()
  response.delete_cookie('user_id')
  response['HX-REFRESH'] = 'true' 
  print("Cookie 'user_id' removido, enviando instrução de refresh.")
  return response
#########################################################################################
@never_cache
@user_login_required
def select(request):
  user_id = request.COOKIES.get('user_id', '1') 
  cardsOnLeft = requests.get(f'{URL}/cards/').json()
  cardsOnRight = requests.get(f'{URL}/user/{user_id}/cards').json()
  userCards = requests.get(f'{URL}/user/{user_id}/cards').json()


  template = 'select_cards.html' if request.htmx else 'base.html'
  context = {'cardsLeft': cardsOnLeft, 'cardsRight': cardsOnRight, 'userCards': userCards, 'filters': "||"}
  if not request.htmx:
    context['page'] = 'select'
  return render(request, template, context)

def select_filter(request, filter = "||", isSideLeft = False):
  user_id = request.COOKIES.get('user_id', '1') 
  cards = ""
  template = ""
  context = {}
  if (isSideLeft == "true"):
    cards = requests.get(f'{URL}/cards/{filter}').json()
    template = 'select_cards_wanted.html' if request.htmx else 'base.html'
    context = {'cardsLeft': cards, 'filters': filter}
  else:
    cards = requests.get(f'{URL}/user/{user_id}/cards/{filter}').json()
    template = 'select_cards_offer.html' if request.htmx else 'base.html'
    context = {'cardsRight': cards, 'filters': filter}

  if not request.htmx:
    context['page'] = 'select_filter'
  return render(request, template, context)

def make_offer(request, cardsWanted, cardsOffered):
  user_id = request.COOKIES.get('user_id', '1') 
  stringCardsWanted = cardsWanted[:-3].split("-|-")
  stringCardsOffered = cardsOffered[:-3].split("-|-")
  listCardsWanted = []
  listCardsOffered = []
  for card in stringCardsWanted:
    card_attributes = card.split("|")
    if (card_attributes[2] == ""):
      card_attributes[2] = None
    listCardsWanted.append(card_operations.select_card(name=card_attributes[0], card_type=card_attributes[1], monster_type=card_attributes[2]))
  
  for card in stringCardsOffered:
    card_attributes = card.split("|")
    if (card_attributes[2] == ""):
      card_attributes[2] = None
    listCardsOffered.append(card_operations.select_card(name=card_attributes[0], card_type=card_attributes[1], monster_type=card_attributes[2]))

  offer_operations.create_offer(user_id=user_id, cards_given=listCardsOffered, cards_wanted=listCardsWanted)
  return render(request, template_name="select_cards.html", status=204)

#########################################################################################
# def make_offer(request):
#   user_cards = card_operations.select_card()
#   cards_wants = []

#   if request.method == 'POST':
#     try:
#       json_cards = json.loads(request.body)
#       ncards = json_cards['cards']
#     except json.JSONDecodeError:
#       ncards = request.POST.get('selected_cards', '[]')

#     if isinstance(ncards, list):
#       cards_wants = [card for card in user_cards if str(card.id) in ncards]

#   else:
#     selected_names_str = request.COOKIES.get('selected_card_names', '[]')
#     selected_names = json.loads(selected_names_str)

#     for name in selected_names:
#       cards = list(card_operations.select_card(name=name))
#       if cards:
#         cards_wants.append(cards[0])

#   template = 'make_offer.html' if request.htmx else 'base.html'
#   context = {
#     'cards_want': cards_wants,
#     'user_cards': user_cards
#   }
#   if not request.htmx:
#     context['page'] = 'make_offer'

#   return render(request, template, context)

#########################################################################################
@never_cache
@user_login_required
def exchanges(request):
  user_id = request.COOKIES.get('user_id', '1')
  api_url = f"{URL}/exchanges"
  params = {'user_id': user_id}
  exchanges_data = []
  try:
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
      exchanges_data = response.json()
    else:
      error_message = f"Erro ao buscar trocas. Código: {response.status_code}"
      print(error_message)
  except requests.exceptions.RequestException as e:
      error_message = f"Não foi possível conectar à API: {e}"
      print(error_message)

  template = 'exchanges.html' if request.htmx else 'base.html'
  context = {
    'exchanges': exchanges_data
  } if request.htmx else {'page': 'exchanges'}

  return render(request, template, context)

#########################################################################################
@never_cache
@user_login_required
def card_list(request, list_type='all'):
  user_id = request.COOKIES.get('user_id', '1') 
  response = requests.get(f'{URL}/user/{user_id}/cards')
  user_cards: list[YugiohCardRead] = response.json()
  wishlist_cards = requests.get(f'{URL}/user/{user_id}/wishlist').json()

  if list_type == 'all':
    response = requests.get(f'{URL}{PATHS["list"]}')
    base_cards: list[YugiohCardRead] = response.json()
  elif list_type == 'user_cards':
    base_cards = user_cards
  elif list_type == 'wishlist':
    base_cards = wishlist_cards

  filtered_cards = search_cards(request, base_cards)

  title_map = {
    'all': "Lista de Todas as Cartas",
    'user_cards': "Minhas Cartas",
    'wishlist': "Minha Lista de Desejos",
  }
  page_title = title_map.get(list_type, "Lista de Cartas")

  view_mode = request.GET.get('view_mode', 'grid')

  is_filter_request = request.GET.get('source') == 'filter_form'

  if is_filter_request:
    template = '_card_grid.html' if request.htmx else 'base.html'
  else:
    template = 'card_list.html' if request.htmx else 'base.html'
  
  context = {
    'cards': filtered_cards,
    'user_cards': user_cards,
    'wishlist_cards': wishlist_cards,
    'page_title': page_title,
    'view_mode': view_mode,
  }

  if not request.htmx:
    context['page'] = 'card_list'

  return render(request, template, context)

#########################################################################################

def change_wishlist(request, url, card_id, isAdd):
  user_id = request.COOKIES.get('user_id', '1') 
  card = requests.get(f'{URL}/card/{card_id}').json()
  userCards = requests.get(f'{URL}/user/{user_id}/cards').json()
  template = '_card_buttons.html'

  if (isAdd == "true"):
    requests.post(url=f"{URL}/user/{user_id}/wishlist/{card_id}")
  else:
    requests.delete(url=f"{URL}/user/{user_id}/wishlist/{card_id}")
  
  wishlist_cards = requests.get(f'{URL}/user/{user_id}/wishlist').json() 

  context = {'card': card, 'user_cards': userCards, 'wishlist_cards': wishlist_cards}
  return render(request, template, context)

def change_user_card(request, url, card_id, isAdd):
  user_id = request.COOKIES.get('user_id', '1') 
  card = requests.get(f'{URL}/card/{card_id}').json()
  wishlist_cards = requests.get(f'{URL}/user/{user_id}/wishlist').json() 
  template = '_card_buttons.html'

  if (isAdd == "true"):
    requests.post(url=f"{URL}/user/{user_id}/cards/{card_id}")
  else:
    requests.delete(url=f"{URL}/user/{user_id}/cards/{card_id}")

  userCards = requests.get(f'{URL}/user/{user_id}/cards').json()
  context = {'card': card, 'user_cards': userCards, 'wishlist_cards': wishlist_cards}

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
@never_cache
@user_login_required
def offers(request):
  user_id = request.COOKIES.get('user_id', '1') # default to one

  # Get offers for the current user
  offers_response = requests.get(
    f"{URL}/{PATHS['offers']}",
    params={'user_id': user_id}
  )

  # Get user cards for the current user
  user_cards_response = requests.get(
    f"{URL}/user/{user_id}/cards"
  )

  user_cards = []
  if user_cards_response.status_code == 200:
    user_cards = user_cards_response.json()
  
  offers = []
  if offers_response.status_code == 200:
    raw_offers = offers_response.json()
    filtered_offers = []
    # Transform the offers to include only necessary owner info
    # and filter out offers made by the current user
    for offer in raw_offers:
      if str(offer['owner']['id']) != user_id:
        formatted_offer = {
          'offer_id': offer['offer']['id'],
          'owner': offer['owner'],
          'cards_given': offer['cards_given'],
          'cards_wanted': offer['cards_wanted']
        }
        filtered_offers.append(formatted_offer)

    offers = filtered_offers

  template = 'offers.html' if request.htmx else 'base.html'
  context = {
    'offers': offers,
    'user_cards': user_cards,
    'user_id': user_id
  }
  
  if not request.htmx:
    context['page'] = 'offers'

  return render(request, template, context)

#########################################################################################]
@never_cache
@user_login_required
def my_offers(request):
  user_id_str = request.COOKIES.get('user_id', '1')
  user_id = int(user_id_str)
    
  my_offers_list = []
  error_message = None

  try:
    exchanges_response = requests.get(f"{URL}/exchanges")
    exchanges_response.raise_for_status() 
    all_exchanges = exchanges_response.json()

    for exchange_data in all_exchanges:
      if exchange_data['offering_user']['id'] == user_id:
        my_offers_list.append({
            "status": "Aceita",
            "data": exchange_data
        })

    open_offers_response = requests.get(f"{URL}/offers")
    open_offers_response.raise_for_status()
    all_open_offers = open_offers_response.json()
        
    for offer_data in all_open_offers:
      if offer_data['owner']['id'] == user_id:
        my_offers_list.append({
            "status": "Em Aberto",
            "data": offer_data
        })
  except requests.exceptions.RequestException as e:
    error_message = f"Não foi possível conectar à API: {e}"
    print(error_message)

  print(my_offers_list)

  template = 'my_offers.html' if request.htmx else 'base.html'
  context = { 
    'processed_offers': my_offers_list,
    'user_id': user_id,
  }
  if not request.htmx:
    context['page'] = 'my_offers'
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

#########################################################################################
def search_cards(request, base_cards):
  name_query = request.GET.get('name_query', '').strip()
  card_type_str = request.GET.get('card_type', '')
  monster_type_str = request.GET.get('monster_type', '')

  card_type_enum = None
  if card_type_str:
    card_type_enum = CardType(card_type_str)

  monster_type_enum = None
  if monster_type_str:
    monster_type_enum = MonsterType(monster_type_str)

  filtered_cards = base_cards

  if name_query:
    filtered_cards = [card for card in filtered_cards if name_query.lower() in card.get('name', '').lower()]

  if card_type_enum:
    filtered_cards = [card for card in filtered_cards if card.get('card_type') == card_type_enum]
  
  if monster_type_enum:
    filtered_cards = [card for card in filtered_cards if card.get('monster_type') == monster_type_enum]
  
  return filtered_cards
