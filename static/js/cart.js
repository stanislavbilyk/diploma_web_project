$(document).ready(function() {
    let savedCartCount = localStorage.getItem("cart_count");
    let cartCounter = $("#cart-count");

    if (savedCartCount && savedCartCount > 0) {
        cartCounter.text(savedCartCount).show();
    } else {
        cartCounter.hide();
    }

    $(".Add_to_card").click(function(e) {
        e.preventDefault();
        var product_id = $(this).data("product-id");
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();

        console.log("Клик по кнопке Купить. ID товара:", product_id);

        $.ajax({
            url: "/cart_item/",
            type: "POST",
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                console.log("Ответ от сервера:", response);

                if (response.success) {
                    console.log("Обновляем счетчик:", response.cart_count);
                    $("#cart-count").text(response.cart_count);
                }
                let cartCount = response.cart_count;
                let cartCounter = $("#cart-count");

                if (cartCount > 0) {
                    cartCounter.text(cartCount).show();
                    localStorage.setItem("cart_count", cartCount);
                } else {
                    cartCounter.hide();
                    localStorage.removeItem("cart_count");
                }
            },
            error: function(xhr, status, error) {
                console.error("Ошибка AJAX-запроса:", error);
            }
        });
    });

    $(document).on("click", ".Delete", function () {
    let productId = $(this).data("product-id");
    let deleteButton = $(this);
    console.log("Клик по кнопке удаления, ID товара:", productId);

    $.ajax({
        url: `/cart/delete/${productId}/`,
        type: "POST",
        headers: { "X-CSRFToken": getCSRFToken() },
        success: function (data) {
            console.log("Ответ от сервера на удаление:", data);

            if (data.success) {
                let itemElement = deleteButton.closest("ul.Cart_items");
                console.log("Найден элемент для удаления:", itemElement);

                if (itemElement.length) {
                    console.log("Удаляем элемент:", itemElement);
                    itemElement.remove();
                } else {
                    console.warn("Не найден элемент для удаления!");
                }

                localStorage.setItem("cart_count", data.cart_count);
                $("#cart-count").text(data.cart_count);
            } else {
                console.warn("Удаление товара не удалось. Ответ сервера:", data);
            }
        },
        error: function (xhr, status, error) {
            console.error("Ошибка AJAX-запроса:", error);
        }
    });
});

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

});


