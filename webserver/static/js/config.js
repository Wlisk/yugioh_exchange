
/////////////////////////////////////////////////////////////////////////////////////////
// load all cards selected from the storage
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

// List all the cards that has the input value in its string name
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

/////////////////////////////////////////////////////////////////////////////////////////
document.addEventListener('DOMContentLoaded', function () {
  // Handle back/forward navigation
  window.addEventListener('popstate', function (event) {
    if (event.state && event.state.htmx) {
      htmx.ajax('GET', window.location.pathname, {
        target: '#main-content',
        swap: 'innerHTML'
      });
    }
  });

  loadMarks();
  searchCardsByInput();

  toggleFields(); // Inicializa os campos com base no valor atual
  document.getElementById("filterType").addEventListener("change", toggleFields); // Reage a mudanças

  ///////////////////////////////////////////////////////////////////////////////////////
  // loading indicator before each request
  document.body.addEventListener('htmx:beforeRequest', function (event) {
    // CSS on static/css
    runSpinner('main-content');
    //validSelection(event);
    check_offer_status(event);

    if (evt.detail.requestConfig.url === '/set_user/') {
      // Reload to ensure cookie is applied
      window.location.reload();
    }
  });
});

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