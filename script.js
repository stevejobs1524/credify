async function checkUsername() {
  const username = document.getElementById("username").value;
  const resultDiv = document.getElementById("result");

  resultDiv.innerText = "Checking...";

  try {
    const response = await fetch("https://credify-oq79.onrender.com/checkUsername", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username }),
    });

    const data = await response.json();

    if (response.ok) {
      resultDiv.innerText = data.is_fake
        ? `⚠️ @${username} is likely FAKE`
        : `✅ @${username} appears REAL`;
    } else {
      resultDiv.innerText = "❌ Error: " + (data.detail || "Unable to check username.");
    }
  } catch (error) {
    resultDiv.innerText = "❌ Network error. Please try again.";
  }
}
