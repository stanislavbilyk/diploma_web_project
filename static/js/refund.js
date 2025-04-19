document.getElementById("Refund_button")?.addEventListener("click", function(event) {event.preventDefault();
    let purchaseId = this.dataset.purchaseId;

    fetch(`/refund_request/${purchaseId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        }
    }).then(response => response.json())
      .then(data => {
          alert(data.message);
          if (data.success) location.reload();
      }).catch(error => console.error("Ошибка:", error));
});