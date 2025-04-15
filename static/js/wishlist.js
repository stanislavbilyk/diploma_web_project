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
    $(document).on("click", ".Wishlist_delete", function () {
    let productId = $(this).data("product-id");
    let deleteButton = $(this);
    console.log("Клик по кнопке удаления, ID товара:", productId);
    console.log("Отправка AJAX-запроса:", `/wishlist/delete/${productId}/`);

    $.ajax({
    url: `/wishlist/delete/${productId}/`,
    type: "POST",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    success: function (data) {
        console.log("Ответ от сервера на удаление:", data);

        if (data.success) {
            let itemElement = deleteButton.closest("ul.Wishlist_item");
            console.log("Найден элемент для удаления:", itemElement);

            if (itemElement.length) {
                console.log("Удаляем элемент:", itemElement);
                itemElement.remove();
            } else {
                console.warn("Не найден элемент для удаления!");
            }

        } else {
            console.warn("Удаление товара не удалось. Ответ сервера:", data);
        }
    },
    error: function (xhr, status, error) {
        console.error("Ошибка AJAX-запроса:", error);
    }
});
});

});

document.addEventListener("DOMContentLoaded", function () {
    function showPopup(message, success = true) {
        let popup = document.getElementById("popup-message");
        let popupText = document.getElementById("popup-text");

        popupText.innerText = message;
        popup.style.backgroundColor = success ? "#4CAF50" : "#f44336";
        popup.style.display = "block";
        setTimeout(() => {
            popup.style.display = "none";
        }, 3000);
    }

    document.querySelectorAll(".Wishlist_button, .Cart_button").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            let form = this.closest("form");
            let formData = new FormData(form);

            fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                }
            })
            .then(response => response.json())
.then(data => {
    let message = "";

    if (data.added !== undefined) {
        // Это ответ от Wishlist
        message = data.added ? "Added to Wishlist!" : "Removed from Wishlist!";
    } else if (data.cart_count !== undefined) {
        // Это ответ от Cart
        message = "Added to Cart!";
    } else {
        message = "Something went wrong!";
    }

    showPopup(message);
})
.catch(() => showPopup("Error connecting to server!", false));
        });
    });
});



