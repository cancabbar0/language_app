document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("ask-count-form");
    const messageDiv = document.getElementById("message");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const askCountInput = document.getElementById("ask-count").value;

        fetch(window.location.href, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: new URLSearchParams({
                "status": "change_ask_count",
                "ask_count": askCountInput
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                messageDiv.textContent = `Error: ${data.result}`;
                messageDiv.style.color = "red";
            } else {
                messageDiv.textContent = data.result;
                messageDiv.style.color = "green";
            }
        })
        .catch(error => {
            messageDiv.textContent = `Error: ${error}`;
            messageDiv.style.color = "red";
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
