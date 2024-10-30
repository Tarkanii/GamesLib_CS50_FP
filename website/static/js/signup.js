import { LoadingHandler } from "./buttonHandlers.js";

export function signupHandler() {
    const signupForm = document.querySelector("#signupForm");
    if (!signupForm) return;

    signupForm.addEventListener("submit", () => {
        const loadBtn = new LoadingHandler(signupForm.querySelector(".submit-button"), signupForm.querySelector(".submit-button").innerHTML);
        loadBtn.activate();
    });
}