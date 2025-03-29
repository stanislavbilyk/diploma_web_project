document.addEventListener("DOMContentLoaded", function () {
    const stripe = Stripe("pk_test_51R1Sb3R3aVETsf5TuShdJeQkSabTE9UX4rxC6HnEeJdkA7jUsohu2Ne7r6vmQwx9xlKDUaWLuDuS1gqMw5czLhIE00LfdGL8U6");
    const elements = stripe.elements();

    const cardNumber = elements.create("cardNumber", { style: { base: { fontSize: "16px" } } });
    const cardExpiry = elements.create("cardExpiry", { style: { base: { fontSize: "16px" } } });
    const cardCvc = elements.create("cardCvc", { style: { base: { fontSize: "16px" } } });


    cardNumber.mount("#card-number");
    cardExpiry.mount("#card-expiry");
    cardCvc.mount("#card-cvc");

    const form = document.getElementById("payment-form");
    const submitButton = document.getElementById("submit-button");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        submitButton.disabled = true;

        const { token, error } = await stripe.createToken(cardNumber);

        if (error) {
            document.getElementById("card-errors").textContent = error.message;
            submitButton.disabled = false;
            return;
        }

        console.log("Stripe token:", token.id);

        const formData = new FormData();
        formData.append("stripeToken", token.id);

        const formAction = form.action;
const match = formAction.match(/\/checkout\/payment\/(\d+)\//);
const purchase_id = match ? match[1] : null;
console.log("Форма отправляется на:", form.action);
console.log("purchase_id:", purchase_id);
const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
console.log("CSRF Token:", csrfToken);
for (let [key, value] of formData.entries()) {
    console.log(key, value);
}
console.log("Sending request to:", `/checkout/payment/${purchase_id}/`);
if (!purchase_id) {
    console.error("Ошибка: не удалось определить purchase_id!");
} else {
    fetch(`/checkout/payment/${purchase_id}/`, {
    method: "POST",
    body: formData,
    headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        "Accept": "application/json",
    },
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    if (data.success) {
        alert("Payment successful!");
        localStorage.setItem("cart_count", "0");
        $("#cart-count").hide();
        window.location.href = data.redirect_url;
    } else {
        alert("Payment failed: " + data.error);
        submitButton.disabled = false;
    }
})
.catch(error => {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
    submitButton.disabled = false;
});
}

    });
});
