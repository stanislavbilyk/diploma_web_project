document.addEventListener("DOMContentLoaded", function () {
    function showPopup(message, success = true) {
    let popup = document.getElementById("popup-message");
    let popupText = document.getElementById("popup-text");

    popupText.innerText = message;
    popup.style.backgroundColor = success ? "#4CAF50" : "#f44336";
    popup.style.display = "block";

    setTimeout(() => {
        console.log("Reloading page...");
        popup.style.display = "none";
        location.reload();
    }, 3000);
}

    document.querySelectorAll("#Accept_button, #Decline_button").forEach(input => {
        input.addEventListener("click", function (event) {
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

    if (data.accepted !== undefined) {
        message = "Refund accepted!";
    } else if (data.declined !== undefined) {
        message = "Refund declined!";
    } else {
        message = "Something went wrong!";
    }

    showPopup(message);
})
.catch(() => showPopup("Error connecting to server!", false));
        });
    });
});

