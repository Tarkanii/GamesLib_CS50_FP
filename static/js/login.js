import { LoadingButtonHandler } from "./buttonHandlers.js";

export function loginHandler() {
    const loginForm = document.querySelector("#loginForm");
    if (!loginForm) return;

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const email = loginForm.querySelector("[name=email]").value;
        const password = loginForm.querySelector("[name=password]").value;
        const emailHint = loginForm.querySelector("[data-hint=email]");
        const passwordHint = loginForm.querySelector("[data-hint=password]");
        const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        
        const emailValid = emailRegex.test(email);
        const passwordValid = password.length >= 1;

        if (!emailValid && !emailHint.classList.contains("show")) {
            emailHint.classList.add("show");
        } else if (emailValid && emailHint.classList.contains("show")) {
            emailHint.classList.remove("show");
        }

        if (!passwordValid && !passwordHint.classList.contains("show")) {
            passwordHint.classList.add("show");
        } else if (passwordValid && passwordHint.classList.contains("show")) {
            passwordHint.classList.remove("show");
        }

        if (!emailValid || !passwordValid) return;
        
        const requestSettings = {
            method: "POST", 
            body: JSON.stringify({ email, password }), 
            headers: {
                "Content-Type": "application/json"
            }
        }
        const loadBtn = new LoadingButtonHandler(loginForm.querySelector(".submit-button"), loginForm.querySelector(".submit-button").innerHTML);
        loadBtn.activate();

        try {
            const response = await fetch("http://127.0.0.1:5000/login", requestSettings);
            const data = await response.json();

            if (response.status != 200) {
                handleError(data.message);
            }

            loadBtn.deactivate();
        } catch (error) {
            console.log("Error", error);
            loadBtn.deactivate();
        }
    });
}

function handleError(message = "Error") {
    const modal = document.querySelector(".modal-bg");
    modal.querySelector(".message").innerHTML = message;

    if (!modal.classList.contains("open")) {
        modal.classList.add("open");
    }
}