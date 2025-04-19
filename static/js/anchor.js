document.addEventListener("DOMContentLoaded", function() {
    if (window.location.href.includes("page=") || window.location.href.includes("discount_page=")) {
        let targets = document.querySelectorAll(".Our_items, .Discounts_section");
        if (targets.length) {
            targets[0].scrollIntoView({ behavior: "smooth" });
        }
    }
});


