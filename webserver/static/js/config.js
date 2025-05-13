document.addEventListener('DOMContentLoaded', function() {
  // Handle back/forward navigation
  window.addEventListener('popstate', function(event) {
    if(event.state && event.state.htmx) {
          htmx.ajax('GET', window.location.pathname, {
              target: '#main-content',
              swap: 'innerHTML'
          });
    }
  });

  // used on onSubmit form method of select_cards
  function validSelection() {
    const checkboxes = document.querySelectorAll('input[name="cards"]:checked');
    const errorMessage = document.getElementById('errorMessage')

    if (checkboxes.length === 0) {
      errorMessage.textContent = "Select at least one card."
      errorMessage.style.display = "block"
      return false;
    }

    errorMessage.style.display = "block"
    return true;
  }

  // load all cards selected from the storage
  function loadMarks() {
    // Restaurar marcações
    const selected = JSON.parse(localStorage.getItem("selectedCards") || "[]");
    selected.forEach(id => {
      const checkbox = document.querySelector(`input[name="cards"][value="${id}"]`);
      if (checkbox) checkbox.checked = true;
    });

    // Salvar marcações
    const checkboxes = document.querySelectorAll('input[name="cards"]');
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

  document.addEventListener("DOMContentLoaded", () => {
    loadMarks();
    searchCardsByInput();
  });
  
  // loading indicator before each request
  document.body.addEventListener('htmx:beforeRequest', function(event) {
    // CSS on static/css
    document.getElementById('main-content').innerHTML = `
      <div class="loading">
        <div class="spinner"></div>
        <div class="loading-text">Loading...</div>
      </div>
    `;
  });

  htmx.defineExtension('debug', {
    onEvent: function (name, evt) {
      if (console.debug) console.debug(name, evt);
      else if (console) console.log("DEBUG:", name, evt);
      else throw "NO CONSOLE SUPPORTED";
    }
  });
});

