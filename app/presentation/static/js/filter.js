console.log("filter.js loaded");

document.addEventListener("DOMContentLoaded", () => {

  let booksContainer = document.querySelector(".books-section");
  const sidebar = document.querySelector(".sidebar");

  let debounceTimer = null;

  function buildQuery(params) {
    return new URLSearchParams(params).toString();
  }

  async function loadBooks(params) {
    const query = buildQuery(params);
    const url = `/books?${query}`;

    const res = await fetch(url, {
      headers: { "X-Requested-With": "XMLHttpRequest" }
    });

    const html = await res.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");

    const newBooks = doc.querySelector(".books-section");
    if (!newBooks) return;

    booksContainer.replaceWith(newBooks);
    booksContainer = newBooks; // IMPORTANT
  }

  /* =========================
     CATEGORY FILTER
     ========================= */
  sidebar.addEventListener("change", (e) => {
    if (e.target.dataset.filter === "category") {
      loadBooks({
        category: e.target.value,
        page: 1
      });
    }
  });

  /* =========================
     SEARCH + AUTHOR (DEBOUNCE)
     ========================= */
  sidebar.addEventListener("input", (e) => {
    if (
      e.target.dataset.filter !== "search" &&
      e.target.dataset.filter !== "author"
    ) {
      return;
    }

    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(() => {
      const search = document.querySelector('[data-filter="search"]')?.value || "";
      const author = document.querySelector('[data-filter="author"]')?.value || "";

      loadBooks({
        search: search,
        author: author,
        page: 1
      });
    }, 400);
  });

  /* =========================
     PAGINATION
     ========================= */
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-page]");
    if (!btn) return;

    loadBooks({
      page: btn.dataset.page
    });
  });
  /* =========================
   RESET FILTERS (AJAX)
   ========================= */
sidebar.addEventListener("click", (e) => {
  const resetBtn = e.target.closest("[data-reset]");
  if (!resetBtn) return;

  const type = resetBtn.dataset.reset;

  // reset category
  if (type === "category") {
    sidebar
      .querySelectorAll('[data-filter="category"]')
      .forEach(input => input.checked = false);
  }

  // reset search
  if (type === "search") {
    const searchInput = sidebar.querySelector('[data-filter="search"]');
    if (searchInput) searchInput.value = "";
  }

  // reset author
  if (type === "author") {
    const authorInput = sidebar.querySelector('[data-filter="author"]');
    if (authorInput) authorInput.value = "";
  }

  // reload books without filters
  loadBooks({ page: 1 });
});


});
