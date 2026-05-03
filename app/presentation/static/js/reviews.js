document.addEventListener("DOMContentLoaded", async () => {
  const section = document.querySelector(".reviews-section");
  if (!section) return;

  const isbn = section.dataset.isbn;
  const loading = document.getElementById("reviews-loading");
  const container = document.getElementById("reviews-content");
  const cta = document.getElementById("open-review");
  const form = document.getElementById("review-form");
  const errorBox = document.getElementById("review-error");

  let reviewsData = null;
  let selectedRating = 0;

  /* =======================
     LOAD REVIEWS
     ======================= */
  try {
    const res = await fetch(`/api/books/${isbn}/reviews`);
    if (!res.ok) throw new Error();

    reviewsData = await res.json();
    renderReviews(reviewsData);

    loading.remove();
    container.hidden = false;
  } catch {
    loading.textContent = "Unable to load reviews.";
    return;
  }

  /* =======================
     OPEN FORM
     ======================= */
  cta?.addEventListener("click", () => {
    cta.remove();
    form.hidden = false;
  });

  /* =======================
     STAR RATING
     ======================= */
  const stars = form.querySelectorAll(".rating-stars span");
  stars.forEach(star => {
    star.addEventListener("click", () => {
      selectedRating = Number(star.dataset.value);
      stars.forEach(s =>
        s.classList.toggle("active", Number(s.dataset.value) <= selectedRating)
      );
    });
  });

  /* =======================
     SUBMIT (NO RELOAD)
     ======================= */
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.textContent = "";

    const comment = form.querySelector("textarea").value.trim();
    if (!selectedRating || !comment) {
      errorBox.textContent = "Rating and comment required.";
      return;
    }

    try {
      const res = await fetch(`/api/books/${isbn}/reviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json"
        ,
        "X-CSRF-Token": csrfToken
         },
        body: JSON.stringify({ rating: selectedRating, comment })
      });

      if (!res.ok) throw new Error();

      /* ===== UPDATE UI INSTANTLY ===== */
      const newReview = {
        email: "You",
        rating: selectedRating,
        comment
      };

      reviewsData.reviews.unshift(newReview);
      reviewsData.total += 1;
      reviewsData.average = (
        (reviewsData.average * (reviewsData.total - 1) + selectedRating) /
        reviewsData.total
      ).toFixed(1);

      renderReviews(reviewsData);

      form.reset();
      selectedRating = 0;
      stars.forEach(s => s.classList.remove("active"));
      form.hidden = true;

    } catch {
      errorBox.textContent = "Failed to submit review.";
    }
  });

  /* =======================
     RENDER FUNCTION
     ======================= */
  function renderReviews(data) {
    container.innerHTML = "";

    const stats = document.createElement("div");
    stats.className = "reviews-stats";
    stats.innerHTML = `
      <div class="average-rating">${data.average}</div>
      <div class="total-reviews">Based on ${data.total} reviews</div>
    `;

    const list = document.createElement("div");
    list.className = "review-items-container";

    data.reviews.forEach(r => {
      const item = document.createElement("div");
      item.className = "review-item";

      const header = document.createElement("div");
      header.className = "review-header";

      const email = document.createElement("strong");
      email.textContent = r.email;

      const stars = document.createElement("span");
      stars.textContent =
        "★".repeat(r.rating) + "☆".repeat(5 - r.rating);

      const text = document.createElement("p");
      text.className = "review-text";
      text.textContent = r.comment;

      header.append(email, stars);
      item.append(header, text);
      list.appendChild(item);
    });

    container.append(stats, list);
  }
});
