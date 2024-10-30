export function searchSubmitHandler() {
    const searchForm = document.querySelector("#searchForm");
    if (!searchForm) return;

    searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        document.querySelector(".search").value = document.querySelector(".search").value.trim();
        const url = new URL(location.href)
        if (url.searchParams.get("genres")) {
            window.location.href = `/games?search=${document.querySelector(".search").value}&genres=${url.searchParams.get("genres")}`;
        } else {
            window.location.href = `/games?search=${document.querySelector(".search").value}`;
        }
    })
}