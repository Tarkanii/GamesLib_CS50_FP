import { LoadingButtonHandler } from "./buttonHandlers.js";
import { handleError } from "./helpers.js";

export function signupHandler() {
    const signupForm = document.querySelector("#signupForm");
    if (!signupForm) return;

    signupForm.addEventListener("submit", async (e) => {
        console.log("submit");
        e.preventDefault();
        
        const email = signupForm.querySelector("[name=email]").value;
        const password = signupForm.querySelector("[name=password]").value;
        const confirmation = signupForm.querySelector("[name=confirmation]").value;

        const emailHint = signupForm.querySelector("[data-hint=email]");
        const passwordHint = signupForm.querySelector("[data-hint=password]");
        const confirmationHint = signupForm.querySelector("[data-hint=confirmation]");

        const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        
        const emailValid = emailRegex.test(email);
        const passwordValid = password.length >= 8 && !password.includes(" ");
        const confirmationValid = confirmation === password;

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

        if (!confirmationValid && !confirmationHint.classList.contains("show")) {
            confirmationHint.classList.add("show");
        } else if (confirmationValid && confirmationHint.classList.contains("show")) {
            confirmationHint.classList.remove("show");
        }

        if (!emailValid || !passwordValid || !confirmationValid) return;
        
        const requestSettings = {
            method: "POST", 
            body: JSON.stringify({ email, password }), 
            headers: {
                "Content-Type": "application/json"
            }
        }
        const loadBtn = new LoadingButtonHandler(signupForm.querySelector(".submit-button"), signupForm.querySelector(".submit-button").innerHTML);
        loadBtn.activate();

        try {
            const response = await fetch("http://127.0.0.1:5000/signup", requestSettings);
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