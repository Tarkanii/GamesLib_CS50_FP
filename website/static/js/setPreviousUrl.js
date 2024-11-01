import { LoadingHandler } from "./buttonHandlers.js";

export function setPrevUrl() {
    const gamesList = document.querySelector(".games-list");
    if (!gamesList) return;

    gamesList.querySelectorAll(".game-card__link").forEach((link) => {
        link.addEventListener("click", () => {
            sessionStorage.setItem("prevUrl", location.href);
            const loadBtn = new LoadingHandler(link, link.innerHTML);
            loadBtn.activate();
        })
    })
}