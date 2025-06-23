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

// function filterFieldToggle() {
//   const toggleButton = document.getElementById('filter-toggle-button');
//   const filterForm = document.getElementById('filter-form');
//   const arrowIcon = document.getElementById('filter-arrow-icon');

//   if (!toggleButton || !filterForm || !arrowIcon) {
//       return;
//   }

//   toggleButton.addEventListener('click', () => {
//       filterForm.classList.toggle('hidden');
//       arrowIcon.classList.toggle('rotate-180');
//   });
// }

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

function loadMarks() {
  // Restaurar marcações
  const selected = JSON.parse(localStorage.getItem("selectedCards") || "[]");
  selected.forEach(id => {
    const checkbox = document.querySelector(`input[name="cards"][value="${id}"]`);
    if (checkbox) checkbox.checked = true;
  });

  // Salvar marcações
  const checkboxes = document.querySelectorAll('input[name="cards"]') || [];
  checkboxes.forEach(cb => {
    cb.addEventListener("change", () => {
      const selectedIds = Array.from(document.querySelectorAll('input[name="cards"]:checked')).map(cb => cb.value);
      localStorage.setItem("selectedCards", JSON.stringify(selectedIds));
    });
  });
}

function searchCardsByInput() {
  const searchInput = document.getElementById("searchField");

  if (searchInput) {
    searchInput.addEventListener("input", () => {
      const query = searchInput.value.toLowerCase();
      const cards = document.querySelectorAll(".card-label");

      cards.forEach(card => {
        const name = card.textContent.toLowerCase();
        if (name.includes(query)) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  }
}

function toggleFields() {
  const filterEl = document.getElementById('filterType');

  if (!filterEl) {
    return;
  }

  if (filterEl) {
    const filterType = filterEl.value;
    // Esconde todos os campos
    document.getElementById('nameField').style.display = 'none';
    document.getElementById('cardTypeField').style.display = 'none';
    document.getElementById('monsterTypeField').style.display = 'none';

    // Exibe o campo correspondente com base na seleção
    if (filterType === 'name') {
      document.getElementById('nameField').style.display = 'block';
    } else if (filterType === 'card_type') {
      document.getElementById('cardTypeField').style.display = 'block';
    } else if (filterType === 'monster_type') {
      document.getElementById('monsterTypeField').style.display = 'block';
    }
  }
}

function check_offer_status(evt) {
  if (evt.detail.elt.getAttribute('hx-post') === '/offers/respond/') {
    const response = JSON.parse(evt.detail.xhr.responseText);
    
    if (response.status === 'ok') {
      // Show success message and refresh offers
      htmx.trigger('#main-content', 'refreshOffers');
      alert('Offer accepted successfully!');
    } else if (response.status === 'refused') {
      // Show refusal message and refresh offers
      htmx.trigger('#main-content', 'refreshOffers');
      alert('Offer rejected successfully!');
    } else if (response.status === 'user_has_no_card') {
      alert('You do not have all the required cards to accept this offer!');
    } else {
      alert('Error: ' + (response.message || 'Unknown error occurred'));
    }
  }

  document.body.addEventListener('refreshOffers', function() {
    htmx.ajax('GET', '/offers/', { target: '#main-content', swap: 'innerHTML' });
  });
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
  //filterFieldToggle();
  loadMarks();
  searchCardsByInput();
  toggleFields();
}
/////////////////////////////////////////////////////////////////////////////////////////
document.addEventListener('DOMContentLoaded', function () {

  initializePersistentComponents();
  initializePageContent();

  validatePasswordsOnInput();

  document.body.addEventListener('htmx:afterSwap', initializePageContent);

  document.body.addEventListener('htmx:configRequest', (event) => {
    if (event.detail.elt.id === 'filter-form') {
        event.detail.parameters['view_mode'] = currentViewMode;
    }
  });
  
  // Por algum motivo, remover essa linha de código faz com que aceitar ou esconder uma oferta fique carregando infinitamente
  // Não consegui descobrir porque isso acontece
  document.getElementById("filterType")?.addEventListener("change", toggleFields);

  window.addEventListener('popstate', function (event) {
    if (event.state && event.state.htmx) {
      htmx.ajax('GET', window.location.pathname, {
        target: '#main-content',
        swap: 'innerHTML'
      });
    }
  });

  document.body.addEventListener('htmx:afterRequest', (event) => {
    check_offer_status(event);
  });

  document.body.addEventListener('refreshOffers', () => {
    htmx.ajax('GET', '/offers/', { target: '#main-content', swap: 'innerHTML' });
  });
});
///////////////////////////////////////////////////////////////////////////////////////////

// TODO: validation not working yet
/*
// used on post form method of select_cards
function validSelection(event) {
  const form = event.target.closest("form");
  console.log("valid-form", form);
  if (form && form.id === "selectForm") {
    console.log("valid-in", form);
    const checkboxes = document.querySelectorAll('input[name="cards"]:checked');
    if (checkboxes.length === 0) {
      console.log("invalid-check", checkboxes);
      event.preventDefault();

      // Show error message
      const errorDiv = document.getElementById("errorMessage");
      if (errorDiv) errorDiv.innerHTML = "Select at least one card.";
    }
  }
}
*/

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
  const offeredList =  document.getElementById('selectedOfferedCards');

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

  cardsWanted = "";
  cardsOffered = "";


  for (i = 2; i < wantedList.children.length; i++) {
    cardsWanted += (wantedList.children[i].childNodes[1].childNodes[3].textContent);  //card_name
    cardsWanted += "|"
    cardsWanted += (wantedList.children[i].childNodes[1].childNodes[5].textContent);  //card_type
    cardsWanted += "|"
    cardsWanted += (wantedList.children[i].childNodes[1].childNodes[7].textContent);  //monster_type
    cardsWanted += "-|-"

    if (user_cards_name.includes(wantedList.children[i].childNodes[1].childNodes[3].textContent)) {
      alert("Não pode pedir uma carta que já possui");
      return;
    };
  }


  for (i = 2; i < offeredList.children.length; i++) {
    cardsOffered += (offeredList.children[i].childNodes[1].childNodes[3].textContent);
    cardsOffered += "|"
    cardsOffered += (offeredList.children[i].childNodes[1].childNodes[5].textContent);
    cardsOffered += "|"
    cardsOffered += (offeredList.children[i].childNodes[1].childNodes[7].textContent);
    cardsOffered += "-|-"
  }
  htmx.ajax('POST', '/make_offer/' + cardsWanted + "/" + cardsOffered , { target: this}).then(() => {alert("Oferta criada com sucesso")}, () => {alert("Erro ao criar a oferta")}).then(() => {console.log("ok")});
}

///////////////////////////////////////////////////////////
function setUserCard(card_id, hasCard, div) {
  if (!hasCard) {
    if(!confirm("Tem certeza que deseja\nremover essa carta da coleção?"))
      return;
    alertText = "Carta removida da coleção"
    isAdd = "false";
  } else {
    if (!confirm("Tem certeza que deseja\nadicionar essa carta na coleção?"))
      return;
    alertText = "Carta adicionada na coleção."
    isAdd = "true";
  }
  htmx.ajax('POST', "user_cards/" + card_id + "/" +  isAdd, { target: div}).then(() => {alert(alertText)}, () => {alert("Erro ao adicionar a carta")}).then(() => {console.log("ok")});
}

function setUserWishlist(card_id, hasCard, div) {
  if (!hasCard) {
    if(!confirm("Tem certeza que deseja\nremover essa carta da lista de desejos?"))
      return;
    alertText = "Carta removida da lista de desejos"
    isAdd = "false";
  } else {
    if (!confirm("Tem certeza que deseja\nadicionar essa carta na lista de desejos?"))
      return;
    alertText = "Carta adicionada na lista de desejos"
    isAdd = "true";
  }
  htmx.ajax('POST', "wishlist/" + card_id + "/" +  isAdd, { target: div}).then(() => {alert(alertText)}, () => {alert("Erro ao adicionar a carta")}).then(() => {console.log("ok")});
}
