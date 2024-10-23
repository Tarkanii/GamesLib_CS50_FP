import { loginHandler } from "./login.js";
import { signupHandler } from "./signup.js";
import { burgerMenuHandler, modalCloseButtonHandler, readMoreButtonHandler, backButtonHandler } from "./buttonHandlers.js";
import { setGamePageBackground } from "./gamePage.js";
import { searchSubmitHandler } from "./search.js";
import { setPrevUrl } from "./setPreviousUrl.js";

document.addEventListener("DOMContentLoaded", () => {
    burgerMenuHandler();
    modalCloseButtonHandler();
    loginHandler();
    signupHandler();
    setGamePageBackground();
    readMoreButtonHandler();
    searchSubmitHandler();
    backButtonHandler();
    setPrevUrl();
})