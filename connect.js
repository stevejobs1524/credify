// script.js
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("usernameForm");
    const usernameInput = document.getElementById("usernameInput");
    const resultDisplay = document.getElementById("result");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        const username = usernameInput.value.trim();

        if (username === "") {
            resultDisplay.textContent = "Please enter a username.";
            return;
        }

        try {
            const response = await fetch('https://credify-oq79.onrender.com/checkUsername', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username })
            });

            const data = await response.json();

            // Check if the backend response indicates if the username is fake or not
            if (data.isFake === true) {
                resultDisplay.textContent = "This is a fake account!";
            } else {
                resultDisplay.textContent = "This is a real account!";
            }
        } catch (error) {
            console.error("Error:", error);
            resultDisplay.textContent = "There was an error checking the username. Please try again later.";
        }
    });
});
