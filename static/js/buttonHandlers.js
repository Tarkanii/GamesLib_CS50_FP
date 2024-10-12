export function burgerMenuHandler() {
    const menuButton = document.querySelector(".header__menu-button");
    const menu = document.querySelector(".nav-menu");

    menuButton.addEventListener("click", () => {
        menu.classList.toggle("open");

        if (menu.classList.contains("open")) {
            setTimeout(() => menu.classList.add("move"), 0);
            menuButton.querySelector("use").setAttribute("href", "/static/img/icons.svg#icon-cross")
        } else {
            menu.classList.remove("move");
            menuButton.querySelector("use").setAttribute("href", "/static/img/icons.svg#icon-menu")
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