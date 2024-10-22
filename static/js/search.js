export function searchSubmitHandler() {
    const searchForm = document.querySelector("#searchForm");
    if (!searchForm) return;

    searchForm.addEventListener("submit", () => {
        document.querySelector(".search").value = document.querySelector(".search").value.trim();
    })
}