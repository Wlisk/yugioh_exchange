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