import { loginHandler } from "./login.js";
import { signupHandler } from "./signup.js";
import { searchSubmitHandler } from "./search.js";
import { setPrevUrl } from "./setPreviousUrl.js";
import { buttonsHandler } from "./buttonHandlers.js";

document.addEventListener("DOMContentLoaded", () => {
    loginHandler();
    signupHandler();
    searchSubmitHandler();
    setPrevUrl();
    buttonsHandler();
})