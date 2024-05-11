window.addEventListener("load", function() {
    document.body.classList.add("loaded");
});
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("user_prompt_buton").addEventListener("click", sendUserPrompt);
});

function sendUserPrompt() {
    showLoading();

    userPrompt = document.getElementById("user_prompt").value;

    requestData = {
        "userPrompt": userPrompt
    }

    fetch("/api/jornada", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao enviar os dados');
        }
        return response.json();
    })
    .then(data => {
        window.location.href = '/select-category?categories=' + encodeURIComponent(JSON.stringify(data));

    })
    .catch(error => {
        console.error('Ocorreu um erro:', error);
    })
    .finally(() => {
        hideLoading();
      });

  }

function showLoading() {
    document.getElementById("loading").style.display = "block";
}

function hideLoading() {
    document.getElementById("loading").style.display = "none";
}