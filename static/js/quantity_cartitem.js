function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".Plus, .Minus").forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.getAttribute("data-product-id");
            let isAdding = this.classList.contains("Plus");

            console.log('Клик по кнопке:', productId);

            let url = `/cart/update/${productId}/`;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ action: isAdding ? "increase" : "decrease" }),
            })
            .then(response => response.json())
            .then(data => {
                console.log("Ответ от сервера:", data);
                let quantityElement = document.querySelector(`#quantity-${productId}`);
                console.log("Элемент найден?", quantityElement);
                if (data.quantity) {
                    quantityElement.textContent = data.quantity;
                    document.querySelector("#price-" + productId).textContent = data.item_total_price;
                    document.querySelector(".Price_excl_VAT .price_value").textContent = data.price_excl_vat;
                    document.querySelector(".Total_price .price_value").textContent = data.total_price;

                }
            })
            .catch(error => console.error("Ошибка:", error));
        });
    });
});


