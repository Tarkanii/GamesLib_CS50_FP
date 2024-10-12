import { loginHandler } from "./login.js";
import { burgerMenuHandler, modalCloseButtonHandler } from "./buttonHandlers.js";

document.addEventListener("DOMContentLoaded", () => {
    burgerMenuHandler();
    modalCloseButtonHandler();
    loginHandler();
})

