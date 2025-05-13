function toggleFields() {
  const filterType = document.getElementById("filterType").value;
  
  const searchField = document.getElementById("searchField");
  const cardTypeSelect = document.getElementById("cardTypeSelect");
  const monsterTypeSelect = document.getElementById("monsterTypeSelect");

  // Esconde todos os campos primeiro
  searchField.style.display = "none";
  cardTypeSelect.style.display = "none";
  monsterTypeSelect.style.display = "none";

  // Mostra apenas o campo relevante
  if (filterType === "name") {
    searchField.style.display = "inline-block";
  } else if (filterType === "card_type") {
    cardTypeSelect.style.display = "inline-block";
  } else if (filterType === "monster_type") {
    monsterTypeSelect.style.display = "inline-block";
  }
}

// Executa a função ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
  toggleFields(); // Inicializa os campos com base no valor atual
  document.getElementById("filterType").addEventListener("change", toggleFields); // Reage a mudanças
});

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

document.addEventListener("DOMContentLoaded", () => {
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
});