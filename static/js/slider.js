document.addEventListener("DOMContentLoaded", function () {
    const leftArrow = document.querySelector(".Arrow.left");
    const rightArrow = document.querySelector(".Arrow.right");
    const categoriesContainer = document.querySelector(".Categories_container");
    const categoryItems = document.querySelectorAll(".Block_of_category");

    if (!categoriesContainer || categoryItems.length === 0) return;

    const categoryWidth = categoryItems[0].offsetWidth + 32;

    rightArrow.addEventListener("click", function () {
        categoriesContainer.scrollBy({ left: categoryWidth, behavior: "smooth" });
    });

    leftArrow.addEventListener("click", function () {
        categoriesContainer.scrollBy({ left: -categoryWidth, behavior: "smooth" });
    });
});
