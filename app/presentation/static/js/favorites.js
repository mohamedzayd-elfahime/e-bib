console.log("favorites.js loaded");

const csrfToken = document.querySelector(
  'input[name="csrf_token"]'
)?.value;

window.addEventListener("click", async (e) => {

  const btn = e.target.closest(".js-favorite-btn");
  if (!btn) return;

  console.log("FAVORITE CLICK DETECTED");

  e.preventDefault();

  const isbn = btn.dataset.bookId;
  if (!isbn) {
    console.error("Missing ISBN");
    return;
  }

  console.log("Favorite clicked for ISBN:", isbn);

  try {
    const res = await fetch("/favorites", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrfToken
      },
      body: JSON.stringify({ isbn })
    });

    if (!res.ok) throw new Error("Server error");

    btn.classList.toggle("active");

const textEl = btn.querySelector(".wishlist-text");
if (textEl && btn.dataset.textOn && btn.dataset.textOff) {
  textEl.textContent = btn.classList.contains("active")
    ? btn.dataset.textOn
    : btn.dataset.textOff;
}


  } catch (err) {
    console.error("Favorite failed:", err);
  }
});
