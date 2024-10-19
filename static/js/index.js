import { loginHandler } from "./login.js";
import { signupHandler } from "./signup.js";
import { burgerMenuHandler, modalCloseButtonHandler, readMoreButtonHandler } from "./buttonHandlers.js";
import { setGamePageBackground } from "./gamePage.js";

document.addEventListener("DOMContentLoaded", () => {
    burgerMenuHandler();
    modalCloseButtonHandler();
    loginHandler();
    signupHandler();
    setGamePageBackground();
    readMoreButtonHandler();
})