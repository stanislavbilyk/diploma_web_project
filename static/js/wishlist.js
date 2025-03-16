function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".Wishlist_Container").forEach(container => {
        if (container.getAttribute("data-in-wishlist") === "true") {
            container.classList.add("active");
        }
    });

    document.querySelectorAll(".Wishlist_Container").forEach(container => {
        container.addEventListener("click", function (event) {
            event.preventDefault();
            let productId = this.getAttribute("data-product-id");
            console.log(`▶ Клик! Отправляем запрос на /wishlist/toggle/${productId}/`);

            fetch(`/wishlist/toggle/${productId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ product_id: productId }),
            })
            .then(response => response.json())
            .then(data => {
                console.log("Ответ от сервера:", data);
                console.log(`🔄 Сердечко обновляем: ${data.added ? "Добавлено" : "Удалено"}`);

                if (data.added) {
                    this.classList.add("active");
                    this.setAttribute("data-in-wishlist", "true");
                } else {
                    this.classList.remove("active");
                    this.setAttribute("data-in-wishlist", "false");
                }
            })
            .catch(error => console.error("Ошибка:", error));
        });
    });
});





