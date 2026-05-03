console.log("home_user.js loaded");
document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".filter-btn");
    const cards = document.querySelectorAll(".book-card");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const category = button.dataset.category;

            buttons.forEach(b => b.classList.remove("active"));
            button.classList.add("active");

            cards.forEach(card => {
                card.style.display =
                    card.dataset.category === category ? "block" : "none";
            });
        });
    });
});
