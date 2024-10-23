export function setPrevUrl() {
    const gamesList = document.querySelector(".games-list");
    if (!gamesList) return;

    gamesList.querySelectorAll(".game-card__link").forEach((link) => {
        link.addEventListener("click", () => {
            sessionStorage.setItem("prevUrl", location.href);
        })
    })
}