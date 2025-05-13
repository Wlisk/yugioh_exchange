
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

  if(searchInput) {
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

  ///////////////////////////////////////////////////////////////////////////////////////
  // loading indicator before each request
  document.body.addEventListener('htmx:beforeRequest', function (event) {
    // CSS on static/css
    runSpinner('main-content');
    //validSelection(event);
  });

  if(htmx) {
    htmx.defineExtension('debug', {
      onEvent: function (name, evt) {
        if (console.debug) console.debug(name, evt);
        else if (console) console.log("DEBUG:", name, evt);
        else throw "NO CONSOLE SUPPORTED";
      }
    });

    htmx.defineExtension('json-enc', {
      onEvent: function (name, evt) {
          if (name === "htmx:configRequest") {
              evt.detail.headers['Content-Type'] = "application/json";
          }
      },
      
      encodeParameters : function(xhr, parameters, elt) {
          xhr.overrideMimeType('text/json');
          return (JSON.stringify(parameters));
      }
  });
  }
});

function runSpinner(id) {
  document.getElementById(id).innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <div class="loading-text">Loading...</div>
    </div>
  `;
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