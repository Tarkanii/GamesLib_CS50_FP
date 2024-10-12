export function handleError(message = "Error") {
    const modal = document.querySelector(".modal-bg");
    modal.querySelector(".message").innerHTML = message;

    if (!modal.classList.contains("open")) {
        modal.classList.add("open");
    }
}