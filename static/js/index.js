import { loginHandler } from "./login.js";
import { signupHandler } from "./signup.js";
import { burgerMenuHandler, modalCloseButtonHandler } from "./buttonHandlers.js";

document.addEventListener("DOMContentLoaded", () => {
    burgerMenuHandler();
    modalCloseButtonHandler();
    loginHandler();
    signupHandler();
})

