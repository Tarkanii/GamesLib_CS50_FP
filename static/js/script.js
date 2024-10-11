document.addEventListener("DOMContentLoaded", () => {
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
})