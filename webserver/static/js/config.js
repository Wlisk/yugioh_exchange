/////////////////////////////////////////////////////////////////////////////////////////
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

function runSpinner(id) {
  document.getElementById(id).innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <div class="loading-text">Loading...</div>
    </div>
  `;
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

function setUserIdCookie() {
  const userIdInput = document.getElementById('user-id');
  const userId = userIdInput.value || '1';

  // Set the cookie: name=value; expires=...
  const expirationDays = 7;
  const date = new Date();
  date.setTime(date.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
  const expires = "expires=" + date.toUTCString();

  document.cookie = `user_id=${userId}; ${expires}; path=/`;

  alert(`User ID set to ${userId}`);
}
/////////////////////////////////////////////////////////////////////////////////////////
function initializePersistentComponents() {
  cardListDropdownMenu();
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

  document.body.addEventListener('htmx:afterSwap', initializePageContent);

  document.body.addEventListener('htmx:configRequest', (event) => {
    if (event.detail.elt.id === 'filter-form') {
        event.detail.parameters['view_mode'] = currentViewMode;
    }
  });
  
  // Por algum motivo, remover essa linha de código faz com que aceitar ou esconder uma oferta fique carregando infinitamente
  // Não consegui descobrir porque isso acontece
  document.getElementById("filterType").addEventListener("change", toggleFields);

  window.addEventListener('popstate', function (event) {
    if (event.state && event.state.htmx) {
      htmx.ajax('GET', window.location.pathname, {
        target: '#main-content',
        swap: 'innerHTML'
      });
    }
  });

  document.body.addEventListener('htmx:beforeRequest', (event) => {
    runSpinner('main-content');
    if (event.detail.requestConfig.url === '/set_user/') {
      window.location.reload();
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

