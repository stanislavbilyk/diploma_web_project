document.getElementById('delivery-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            fetch('/checkout/transfer-cart-items/', {
                method: 'POST',
                body: JSON.stringify({ purchase_id: data.purchase_id }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Cart items transferred successfully');
                    window.location.href = '{% url "checkout_payment" %}';  // Переход к оплате
                } else {
                    console.error('Error:', data.error);
                }
            });
        } else {
            console.error('Error:', data.error);
        }
    });
});
