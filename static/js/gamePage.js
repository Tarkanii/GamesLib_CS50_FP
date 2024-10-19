export function setGamePageBackground() {
    const bg = document.querySelector(".game-bg");
    if (!bg) return;

    const imageUrl = bg.getAttribute("data-url");
    if (window.innerWidth > 768) {
        setDesktopBg(bg, imageUrl);
    } else {
        setMobileBg(bg, imageUrl);
    }

    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) {
            setDesktopBg(bg, imageUrl);
        } else {
            setMobileBg(bg, imageUrl);
        }
    })
}

function setMobileBg(element, url) {
    element.style.backgroundImage = `linear-gradient(to bottom, rgba(0, 0, 0, 0.8), var(--body-bg) 90%), url(${url})`;
    element.style.backgroundRepeat = "no-repeat";
    element.style.backgroundSize = "cover";
    element.style.backgroundPosition = "top center";
}

function setDesktopBg(element, url) {
    element.style.backgroundImage = `linear-gradient(to bottom, rgba(0, 0, 0, 0.8), var(--body-bg)), url(${url})`;
    element.style.backgroundRepeat = "no-repeat";
    element.style.backgroundSize = "100%";
}