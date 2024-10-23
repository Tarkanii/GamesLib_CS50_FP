import { loginHandler } from "./login.js";
import { signupHandler } from "./signup.js";
import { burgerMenuHandler, modalCloseButtonHandler, readMoreButtonHandler, backButtonHandler, paginationButtonHandler } from "./buttonHandlers.js";
import { searchSubmitHandler } from "./search.js";
import { setPrevUrl } from "./setPreviousUrl.js";

document.addEventListener("DOMContentLoaded", () => {
    burgerMenuHandler();
    modalCloseButtonHandler();
    loginHandler();
    signupHandler();
    readMoreButtonHandler();
    searchSubmitHandler();
    backButtonHandler();
    paginationButtonHandler();
    setPrevUrl();
})