import { LoadingHandler } from "./buttonHandlers.js";

export function loginHandler() {
    const loginForm = document.querySelector("#loginForm");
    if (!loginForm) return;

    loginForm.addEventListener("submit", () => {
        const loadBtn = new LoadingHandler(loginForm.querySelector(".submit-button"), loginForm.querySelector(".submit-button").innerHTML);
        loadBtn.activate();
    });
}