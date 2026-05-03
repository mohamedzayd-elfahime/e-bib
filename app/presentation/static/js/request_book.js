document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".request-btn");
  if (!btn || btn.disabled) return;

  e.preventDefault();

  const isbn = btn.dataset.bookId;
  const status = btn.dataset.status;
  const availableCopies = parseInt(btn.dataset.availableCopies, 10);
  const csrfToken = document.querySelector('input[name="csrf_token"]')?.value;

  if (!isbn || !csrfToken) {
    alert("Missing data");
    return;
  }

  let url = null;

  // ---------- DECISION ----------
  if (status === "borrowed") {
    return; // rien à faire
  }

  if (status === "reserved") {
    url = `/books/${isbn}/reserve/cancel`;
  } else if (availableCopies === 0) {
    url = `/books/${isbn}/reserve`;
  } else {
    url = `/borrow/${isbn}`;
  }

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRF-Token": csrfToken
      }
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Action failed");
      return;
    }

    // ---------- UX (simple) ----------
if (url.endsWith("/reserve/cancel")) {
  btn.querySelector("span").innerText = "Reserve";
  btn.dataset.status = "available"; // ou "idle" si tu veux être plus propre
} else if (url.endsWith("/reserve")) {
  btn.querySelector("span").innerText = "Cancel";
  btn.dataset.status = "reserved";
} else {
  btn.querySelector("span").innerText = "Borrowed";
  btn.disabled = true;
  btn.dataset.status = "borrowed";
}

  } catch {
    alert("Network error");
  }
});
