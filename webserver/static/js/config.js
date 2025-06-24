/////////////////////////////////////////////////////////////////////////////////////////
function passwordVisibility(inputId, toggleButtonId, eyeOnId, eyeOffId) {
  const passwordInput = document.getElementById(inputId);
  const toggleButton = document.getElementById(toggleButtonId);
  const eyeOnIcon = document.getElementById(eyeOnId);
  const eyeOffIcon = document.getElementById(eyeOffId);

  if (!passwordInput || !toggleButton || !eyeOnIcon || !eyeOffIcon) {
    return;
  }

  toggleButton.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      eyeOnIcon.classList.remove('hidden');
      eyeOffIcon.classList.add('hidden');
    } else {
      passwordInput.type = 'password';
      eyeOnIcon.classList.add('hidden')
      eyeOffIcon.classList.remove('hidden');
    }
  });
}

function validatePasswordsOnInput() {
  const passwordInput = document.getElementById('password');
  const passwordConfirmInput = document.getElementById('passwordConfirm');
  const messageDiv = document.getElementById('password-match-message');
  const submitButton = document.getElementById('submit-button');

  if (!passwordInput || !passwordConfirmInput || !messageDiv || !submitButton) {
    return;
  }

  function checkPasswords() {
    const password = passwordInput.value;
    const passwordConfirm = passwordConfirmInput.value;

    // Não mostra mensagem se o campo de confirmação estiver vazio
    if (passwordConfirm === '') {
      messageDiv.textContent = '';
      submitButton.disabled = true; // Desabilita o botão se a confirmação estiver vazia
      submitButton.className = 'w-full px-4 py-3 font-bold text-white bg-purple-300 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors'; // Adiciona classe de botão desabilitado
      return;
    }

    // Se as senhas conferem
    if (password === passwordConfirm) {
      messageDiv.textContent = '';
      submitButton.disabled = false; // Habilita o botão para envio
      submitButton.className = 'w-full px-4 py-3 font-bold text-white bg-purple-900 rounded-md hover:bg-purple-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors'; // Adiciona classe de botão habilitado
    } 
    // Se as senhas não conferem
    else {
      messageDiv.textContent = 'As senhas não conferem.';
      messageDiv.style.color = 'red';
      submitButton.disabled = true; // Desabilita o botão
      submitButton.className = 'w-full px-4 py-3 font-bold text-white bg-purple-300 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors'; // Adiciona classe de botão desabilitado
    }
  }

  passwordInput.addEventListener('input', checkPasswords);
  passwordConfirmInput.addEventListener('input', checkPasswords);

  submitButton.disabled = true; 
  submitButton.className = 'w-full px-4 py-3 font-bold text-white bg-purple-300 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors';
}

function userDropdownMenu() {
  const dropdownButton = document.getElementById('user-dropdown-button');
  const dropdownMenu = document.getElementById('user-dropdown-menu');
  const arrowIcon = document.getElementById('user-menu-arrow-icon');

  if (!dropdownButton || !dropdownMenu) {
    return;
  }

  dropdownButton.addEventListener('click', function(event) {
    event.stopPropagation();
    dropdownMenu.classList.toggle('hidden');
    arrowIcon.classList.toggle('rotate-180');
  });

  window.addEventListener('click', function(event) {
    if (!dropdownMenu.classList.contains('hidden')) {
        dropdownMenu.classList.add('hidden');
        arrowIcon.classList.remove('rotate-180');
    }
  });
  
  dropdownMenu.addEventListener('click', function(event) {
    event.stopPropagation();
  });
}

function cardListDropdownMenu() {
  const dropdownButton = document.getElementById('dropdown-button');
  const dropdownMenu = document.getElementById('dropdown-menu');
  const arrowIcon = document.getElementById('menu-arrow-icon');

  if (!dropdownButton || !dropdownMenu) {
    return;
  }

  dropdownButton.addEventListener('click', function(event) {
    event.stopPropagation();
    dropdownMenu.classList.toggle('hidden');
    arrowIcon.classList.toggle('rotate-180');
  });

  window.addEventListener('click', function(event) {
    if (!dropdownMenu.classList.contains('hidden')) {
        dropdownMenu.classList.add('hidden');
        arrowIcon.classList.remove('rotate-180');
    }
  });
  
  dropdownMenu.addEventListener('click', function(event) {
    event.stopPropagation();
  });
}

let currentViewMode = 'grid'; 

function cardViewSwitcher() {
           
  const listViewBtn = document.getElementById('list-view-btn');
  const gridViewBtn = document.getElementById('grid-view-btn');
  const cardContainer = document.getElementById('card-container');

  if (!listViewBtn || !gridViewBtn || !cardContainer) {
    return;
  }

  const activeBtnClasses = ['text-purple-700', 'bg-purple-100'];
  const inactiveBtnClasses = ['text-gray-500', 'hover:bg-gray-200', 'hover:text-gray-800'];
  
  listViewBtn.addEventListener('click', () => {
      currentViewMode = 'list';
      listViewBtn.classList.add(...activeBtnClasses);
      listViewBtn.classList.remove(...inactiveBtnClasses);
      gridViewBtn.classList.add(...inactiveBtnClasses);
      gridViewBtn.classList.remove(...activeBtnClasses);

      cardContainer.className = 'flex flex-col gap-4';

      document.querySelectorAll('.card').forEach(card => {
          card.className = 'card bg-white rounded-lg overflow-hidden shadow-md hover:shadow-[0px_4px_8px_0px_rgba(0,_0,_0,_0.8)] transition-all duration-300 cursor-pointer flex items-center';
          
          const img = card.querySelector('.card-img');
          img.className = 'card-img w-40 h-auto object-cover';

          const details = card.querySelector('.card-details');
          details.className = 'card-details p-4';

          const buttons = card.querySelector('.card-buttons');
          buttons.className = 'card-buttons w-full py-2 px-4 rounded-b-lg flex justify-end items-center space-x-4'; 
      });
  });

  gridViewBtn.addEventListener('click', () => {
      currentViewMode = 'grid';
      gridViewBtn.classList.add(...activeBtnClasses);
      gridViewBtn.classList.remove(...inactiveBtnClasses);
      listViewBtn.classList.add(...inactiveBtnClasses);
      listViewBtn.classList.remove(...activeBtnClasses);

      cardContainer.className = 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6';
      
      document.querySelectorAll('.card').forEach(card => {
          card.className = 'card bg-white rounded-lg overflow-hidden shadow-md hover:shadow-[0px_4px_8px_0px_rgba(0,_0,_0,_0.8)] transition-all duration-300 cursor-pointer';

          const img = card.querySelector('.card-img');
          img.className = 'card-img w-full h-auto object-cover';

          const details = card.querySelector('.card-details');
          details.className = 'card-details p-4 bg-purple-400 text-black text-center';

          const buttons = card.querySelector('.card-buttons');
          buttons.className = 'card-buttons w-full py-2 px-4 rounded-b-lg content-around flex justify-center items-center space-x-4'; 
      });
  });
}

function clearFilters() {
  const clearButton = document.getElementById('clear-filters-btn');
  const filterForm = document.getElementById('filter-form');

  if (!clearButton || !filterForm) {
      return;
  }

  clearButton.addEventListener('click', () => {
      filterForm.reset();
      htmx.trigger(filterForm, 'submit');
  });
}

function check_offer_status(evt) {
  console.log('HTMX Response Event:', evt);
  
  // Check if this is a response to the offer endpoint
  if (evt.detail.elt.getAttribute('hx-post') === '/offers/respond/') {
    console.log('Response Status:', evt.detail.xhr.status);
    console.log('Response Text:', evt.detail.xhr.responseText);
    
    // Hide the loading indicator and show button text
    const button = evt.detail.elt;
    const buttonText = button.querySelector('.button-text');
    const indicator = button.querySelector('.htmx-indicator');
    
    if (buttonText) buttonText.style.display = 'inline';
    if (indicator) indicator.style.display = 'none';
    
    if (evt.detail.xhr.status === 200) {
      try {
        const response = JSON.parse(evt.detail.xhr.responseText);
        console.log('Parsed Response:', response);
        
        if (response.status === 'ok') {
          // Remove the entire offer card from the DOM
          const offerElement = evt.detail.elt.closest('[id^="offer-"]');
          if (offerElement) {
            offerElement.style.transition = 'opacity 0.5s ease-out';
            offerElement.style.opacity = '0';
            setTimeout(() => {
              offerElement.remove();
            }, 500);
          }
          alert('Oferta aceita com sucesso!');
        } else if (response.status === 'refused') {
          // Remove the entire offer card from the DOM
          const offerElement = evt.detail.elt.closest('[id^="offer-"]');
          if (offerElement) {
            offerElement.style.transition = 'opacity 0.5s ease-out';
            offerElement.style.opacity = '0';
            setTimeout(() => {
              offerElement.remove();
            }, 500);
          }
          alert('Oferta rejeitada com sucesso!');
        } else if (response.status === 'user_has_no_card') {
          alert('Você não possui todas as cartas necessárias para aceitar esta oferta!');
        } else {
          alert('Erro: ' + (response.message || 'Erro desconhecido'));
        }
      } catch (e) {
        console.error('Error parsing response:', e);
        alert('Erro ao processar resposta do servidor');
      }
    } else {
      // Handle HTTP error status codes
      alert('Erro do servidor: ' + evt.detail.xhr.status);
    }
  }
}
/////////////////////////////////////////////////////////////////////////////////////////
function initializePersistentComponents() {
  userDropdownMenu();
  cardListDropdownMenu();
  passwordVisibility(
    'password', 
    'togglePassword', 
    'eye-on-icon', 
    'eye-off-icon'
  );
  
  passwordVisibility(
    'passwordConfirm', 
    'togglePasswordConfirm', 
    'eye-on-icon-confirm', 
    'eye-off-icon-confirm'
  );
}

function initializePageContent() {
  cardViewSwitcher();
  clearFilters();
}
/////////////////////////////////////////////////////////////////////////////////////////

// Add this at the top of your config.js file
function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) {
    return meta.getAttribute('content');
  }
  
  // Fallback to cookie method
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') {
      return value;
    }
  }
  
  return null;
}

document.addEventListener('DOMContentLoaded', function () {

  initializePersistentComponents();
  initializePageContent();
  document.body.removeEventListener('htmx:afterRequest', check_offer_status);

  validatePasswordsOnInput();

  document.body.addEventListener('htmx:afterSwap', initializePageContent);

  document.body.addEventListener('htmx:configRequest', (event) => {
    if (event.detail.elt.id === 'filter-form') {
        event.detail.parameters['view_mode'] = currentViewMode;
    }

    const csrfToken = getCsrfToken();
    if (csrfToken) {
      event.detail.headers['X-CSRFToken'] = csrfToken;
    }
  });

  window.addEventListener('popstate', function (event) {
    if (event.state && event.state.htmx) {
      htmx.ajax('GET', window.location.pathname, {
        target: '#main-content',
        swap: 'innerHTML'
      });
    }
  });

  document.body.addEventListener('htmx:beforeRequest', (event) => {
    //runSpinner('main-content');
    if (event.detail.requestConfig.url === '/set_user/') {
      window.location.reload();
    }
  });

  document.body.addEventListener('htmx:afterRequest', check_offer_status);

  document.body.addEventListener('refreshOffers', () => {
    htmx.ajax('GET', '/offers/', { target: '#main-content', swap: 'innerHTML' });
  });

  // Add error handling for HTMX requests
  document.body.addEventListener('htmx:responseError', (event) => {
    console.error('HTMX Response Error:', event.detail);
    alert('Erro de conexão com o servidor. Verifique sua conexão com a internet.');
  });

  document.body.addEventListener('htmx:sendError', (event) => {
    console.error('HTMX Send Error:', event.detail);
    alert('Erro ao enviar requisição. Verifique sua conexão com a internet.');
  });
});
////////////////////////////////////////////////////////////////////////////////////////////
//funções para select_cards.html

function hideFilter(div, arrow) {
  arrow.classList.toggle("rotate-180");
  div.style.display = div.style.display == 'none' ? div.style.display = 'block' : div.style.display = 'none';
}

function filterApply(card_name_field, card_type_field, monster_type_field, isClear, isLeft) {
  filterActiveL = JSON.parse(document.getElementById("filterActiveL").textContent);
  if (filterActiveL == "") filterActiveL = "||"
  filterActiveR = JSON.parse(document.getElementById("filterActiveR").textContent);
  if (filterActiveR == "") filterActiveR = "||"
  filters = "||"
  if (isClear) {
    // Setar os campos de pesquisa para valor padrão
    card_name_field.value = ""
    card_type_field.selectedIndex = 0
    monster_type_field.selectedIndex = 0
  } else {
    filters = encodeURI(card_name_field.value) + "|" + card_type_field.options[card_type_field.selectedIndex].value + "|" + monster_type_field.options[monster_type_field.selectedIndex].value;
  }
  if (isLeft) {
    //Foi preciso colocar esse timeout porque a função ativa antes das cartas aparecerem
    htmx.ajax('GET', '/select/' + filters + "/" + "true", { target: '#wantedCardList', swap: 'innerHTML' }).then(setTimeout(() => reloadColor(document.getElementById("wantedCardList")), 200));
  } else {
    htmx.ajax('GET', '/select/' + filters + "/" + "false" , { target: '#offerCardList', swap: 'innerHTML' }).then(setTimeout(() => reloadColor(document.getElementById("offerCardList")), 200));
  }
}

//Função que adiciona ou remove cartas das listas de cartas que deseja trocar
function select_card(card_element, isLeft) {
  const wantedList = document.getElementById('selectedWantedCards');
  const offeredList =  document.getElementById('selectedOfferedCards');
  if (isLeft) {
    card_element_list = wantedList;
  } else {
    card_element_list = offeredList;
  }
  //Se for um clone, só remove ele da lista
  if (card_element.id.slice(-6) == "_clone" ) {
    card_element.remove();
    document.getElementById(card_element.id.slice(0,-6)).style.backgroundColor = ""
  } else {
    //Se a cor de fundo não for verde, não foi selecionado ainda
    if ((card_element.style.backgroundColor == "")) {
      
      //Ajustar o tamanho do clone pra não ficar muito grande
      var clone = card_element.cloneNode(true)
      clone.id = card_element.id + "_clone"
      clone.style.width = "25%"
      clone.style.marginLeft = "0.75rem"
      clone.style.marginTop = "0.5rem"
      clone.style.marginBottom = "0.5rem"
      clone.style.minWidth = "25%"
      clone.childNodes[1].childNodes[1].style.width = "50px"  //Largura da carta
      card_element_list.appendChild(clone)  //Adicionar clone a lista
      card_element.style.backgroundColor = "rgba(5, 197, 5, 0.66)"
    } else {
      card_element.style.backgroundColor = ""
      document.getElementById(card_element.id + "_clone").remove();
    }
  }
  if (card_element_list.children.length === 2) {
    card_element_list.children[0].hidden = false;
  } else {
    card_element_list.children[0].hidden = true;
    card_element_list.children[1].hidden = true;
  }
}

function reloadColor(cardList) {
  for (i = 1; i < cardList.children.length; i++) {
    id = cardList.children[i].id + "_clone"
    if (document.getElementById(id) != null) {
      cardList.children[i].style.backgroundColor = "rgba(0,255,0,0.5)"
    }
  }
}

function submitOffer() {
  const wantedList = document.getElementById('selectedWantedCards');
  const offeredList = document.getElementById('selectedOfferedCards');

  user_cards = JSON.parse(document.getElementById("user-cards").text);
  user_cards_name = [];

  if (wantedList.children.length === 2) {
    wantedList.children[0].hidden = true;
    wantedList.children[1].hidden = false;
  }
  if (offeredList.children.length === 2) {
    offeredList.children[0].hidden = true;
    offeredList.children[1].hidden = false;
  }
  if ((offeredList.children.length === 2) || (wantedList.children.length === 2)) return;

  for (i of user_cards) {
    user_cards_name.push(i.name);
  }

  let cardsWanted = [];
  let cardsOffered = [];

  for (i = 2; i < wantedList.children.length; i++) {
    let card_name = wantedList.children[i].childNodes[1].childNodes[3].textContent;
    cardsWanted.push(card_name)

    if (user_cards_name.includes(card_name)) {
      alert("Não pode pedir uma carta que já possui");
      return;
    }
  }

  for (i = 2; i < offeredList.children.length; i++) {
    let card_name = offeredList.children[i].childNodes[1].childNodes[3].textContent;
    cardsOffered.push(card_name)
  }

  let body = JSON.stringify({
    'cardsWanted': cardsWanted,
    'cardsOffered': cardsOffered
  });

  htmx.ajax(
      "POST",
      "/make_offer/" + body,
      {target: this}
  ).then(
      () => {
        alert("Oferta criada com sucesso!");
        location.href = "/my_offers";
      },
      () => {alert("Erro ao criar a oferta")}
  )
}

///////////////////////////////////////////////////////////
function setUserCard(card_id, hasCard, div) {
  if (!hasCard) {
    if(!confirm("Tem certeza que deseja\nremover essa carta da coleção?"))
      return;
    isAdd = "false";
  } else {
    if (!confirm("Tem certeza que deseja\nadicionar essa carta na coleção?"))
      return;
    isAdd = "true";
  }
  htmx.ajax('POST', "user_cards/" + card_id + "/" +  isAdd, { target: div});
}

function setUserWishlist(card_id, hasCard, div) {
  if (!hasCard) {
    if(!confirm("Tem certeza que deseja\nremover essa carta da lista de desejos?"))
      return;
    isAdd = "false";
  } else {
    if (!confirm("Tem certeza que deseja\nadicionar essa carta na lista de desejos?"))
      return;
    isAdd = "true";
  }
  htmx.ajax('POST', "wishlist/" + card_id + "/" +  isAdd, { target: div});
}
