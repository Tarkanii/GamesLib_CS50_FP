export function burgerMenuHandler() {
    const menuButton = document.querySelector(".header__menu-button");
    const menu = document.querySelector(".nav-menu");

    menuButton.addEventListener("click", () => {
        menu.classList.toggle("open");

        if (menu.classList.contains("open")) {
            setTimeout(() => menu.classList.add("move"), 0);
            menuButton.querySelector("use").setAttribute("href", "/static/img/icons/icons.svg#icon-cross")
        } else {
            menu.classList.remove("move");
            menuButton.querySelector("use").setAttribute("href", "/static/img/icons/icons.svg#icon-menu")
        }
    })
}

export function modalCloseButtonHandler() {
    const modalButton = document.querySelector("#modalCloseButton");
    const modal = document.querySelector(".modal-bg");

    modalButton.addEventListener("click", () => {
        modal.classList.toggle("open");
    })
}

export function readMoreButtonHandler() {
    const description = document.querySelector(".about-description");
    if (!description) return;

    const full_text = description.innerHTML;
    const readMoreButton = document.querySelector(".read-more-btn");
    if (full_text.length < 255) {
        readMoreButton.style.display = "none";
        return;
    }

    description.innerHTML = full_text.slice(0, 255) + "...";
    readMoreButton.addEventListener("click", () => {
        description.classList.toggle("open");

        if (description.classList.contains("open")) {
            description.innerHTML = full_text;
            readMoreButton.innerHTML = "Show less";
        } else {
            description.innerHTML = full_text.slice(0, 255) + "...";
            readMoreButton.innerHTML = "Read more";
        }
        
    })
}

export function backButtonHandler() {
    const backButton = document.querySelector(".back-button");
    if (!backButton) return;

    if (!sessionStorage.getItem("prevUrl")) return;
    backButton.setAttribute("href", sessionStorage.getItem("prevUrl"));
}

export class LoadingButtonHandler {
    text = "";
    element = null;

    constructor(element, text) {
        this.element = element;
        this.text = text;
    }

    activate() {
        this.element.innerHTML = '<span class="loader"></span>';
        this.element.setAttribute("disabled", "true");
    }

    deactivate() {
        this.element.innerHTML = this.text;
        this.element.removeAttribute("disabled");
    }
}