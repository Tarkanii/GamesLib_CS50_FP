export function buttonsHandler() {
    burgerMenuHandler();
    modalCloseButtonHandler();
    readMoreButtonHandler();
    backButtonHandler();
    paginationButtonHandler();
    libraryButtonsHandler();
}

function burgerMenuHandler() {
    const menuButton = document.querySelector(".header__menu-button");
    const menu = document.querySelector(".nav-menu");
    const header = document.querySelector(".header");

    menuButton.addEventListener("click", () => {
        if (menu.classList.contains("open")) {
            menu.classList.remove("move");
            setTimeout(() => menu.classList.remove("open"), 200);
            header.classList.remove("open")
            menuButton.querySelector("use").setAttribute("href", "/static/img/icons/icons.svg#icon-menu");
        } else {
            header.classList.add("open");
            menu.classList.add("open");
            setTimeout(() => menu.classList.add("move"), 0);
            menuButton.querySelector("use").setAttribute("href", "/static/img/icons/icons.svg#icon-cross");
        }
    })
}

function modalCloseButtonHandler() {
    const modalButton = document.querySelector("#modalCloseButton");
    const modal = document.querySelector(".modal-bg");

    modalButton.addEventListener("click", () => {
        modal.classList.toggle("open");
    })
}

function readMoreButtonHandler() {
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

function backButtonHandler() {
    const backButton = document.querySelector(".back-button");
    if (!backButton) return;

    const loadBtn = new LoadingHandler(backButton, backButton.innerHTML);
    backButton.addEventListener("click", () => loadBtn.activate())

    if (!sessionStorage.getItem("prevUrl")) return;
    backButton.setAttribute("href", sessionStorage.getItem("prevUrl"));
}

function paginationButtonHandler() {
    const paginationList = document.querySelector(".pagination-list");
    if (!paginationList) return;

    const paginationButtons = paginationList.querySelectorAll(".pagination-button:not(.active)");
    paginationButtons.forEach((element) => {
        element.addEventListener("click", () => {
            const loadBtn = new LoadingHandler(paginationList, paginationList.innerHTML);
            loadBtn.activate();
        })
    })
}

function libraryButtonsHandler() {
    const libraryButtonList = document.querySelectorAll(".library-button");
    if (!libraryButtonList.length) return;

    libraryButtonList.forEach((button) => {
        button.addEventListener("click", () => {
            const action =  button.getAttribute("data-action");
            const id = button.getAttribute("data-id");
            
            const loadBtn = new LoadingHandler(button, button.innerHTML);
            switch(action) {
                case "save":
                    loadBtn.activate();
                    fetch("/save-game", {
                        method: "POST",
                        body: JSON.stringify({ id })
                    })
                    .then(() => {
                        window.location.reload();
                    })
                    .catch(() => {
                        loadBtn.deactivate();
                    })
                case "delete":
                    loadBtn.activate();
                    fetch("/delete-game", {
                        method: "DELETE",
                        body: JSON.stringify({ id })
                    })
                    .then(() => {
                        window.location.reload();
                    })
                    .catch(() => {
                        loadBtn.deactivate();
                    })
                case "login":
                    window.location.href = "/login";
            }
        })
    })
}

export class LoadingHandler {
    text = "";
    element = null;

    constructor(element, text) {
        this.element = element;
        this.text = text;
    }

    activate() {
        this.element.innerHTML = '<span class="loader"></span>';
        this.element.setAttribute("disabled", "true");
        setTimeout(() => this.deactivate(), 5000);
    }

    deactivate() {
        this.element.innerHTML = this.text;
        this.element.removeAttribute("disabled");
    }
}