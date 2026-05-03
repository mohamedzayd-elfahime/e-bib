document.getElementById("test-return").addEventListener("click", () => {
  fetch("/borrowings/3/return", {
    method: "POST",
    headers: {
      "X-CSRF-Token": document.querySelector('input[name="csrf_token"]').value,
      "X-Requested-With": "XMLHttpRequest"
    }
  });
});
