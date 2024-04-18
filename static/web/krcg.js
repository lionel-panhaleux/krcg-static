function getName(elem) {
    if (elem.dataset.name) {
        return elem.dataset.name
    }
    return elem.textContent
}

function clickCard() {
    document.getElementById("krcg-click-image").src = nameToImage(getName(this))
    document.getElementById("krcg-click-modal").style.display = "block"
}

function overCard() {
    if (window.matchMedia("(hover: none)").matches) {
        return
    }
    document.getElementById("krcg-over-image").src = nameToImage(getName(this))
    document.getElementById("krcg-over-modal").style.display = "block"
}

function outCard(e) {
    if (e.relatedTarget && e.relatedTarget.classList.contains("krcg-modal-image")) {
        e.relatedTarget.addEventListener("mouseout", outCard)
        return
    }
    document.getElementById("krcg-over-modal").style.display = "none"
}

function nameToImage(text) {
    if (!text) {
        return undefined
    }
    text = text.toLowerCase()
    if (text.startsWith("the ")) {
        text = text.substr(4, text.length) + "the"
    }
    text = text
        .replace(/™/g, "tm")
        .replace(/\s|,|\.|-|—|'|’|:|\(|\)|"|\/| |!/g, "")
        .replace(/ö|ó|ø/g, "o")
        .replace(/é|ë|è/g, "e")
        .replace(/œ/g, "oe")
        .replace(/ç/g, "c")
        .replace(/á|ã|å|ä|à/g, "a")
        .replace(/í|î|ï/g, "i")
        .replace(/ñ/g, "n")
        .replace(/ü|ú/g, "u")
    return "https://static.krcg.org/card/".concat(text, ".jpg")
}

function krcgCards() {
    // add modals
    let click_modal = document.createElement("div")
    click_modal.id = "krcg-click-modal"
    click_modal.addEventListener("click", (e) => {
        click_modal.style.display = "none"
    })
    let click_image = document.createElement("img")
    click_image.id = "krcg-click-image"
    click_image.classList.add("krcg-modal-image")
    click_modal.appendChild(click_image)
    let over_modal = document.createElement("div")
    over_modal.id = "krcg-over-modal"
    let over_image = document.createElement("img")
    over_image.id = "krcg-over-image"
    over_image.classList.add("krcg-modal-image")
    over_modal.appendChild(over_image)
    document.body.insertBefore(over_modal, document.body.firstChild)
    document.body.insertBefore(click_modal, document.body.firstChild)
    // add events listeners on all page elements marked as cards
    for (elem of document.querySelectorAll(".krcg-card")) {
        elem.addEventListener("click", clickCard.bind(elem))
        if (!elem.dataset.nohover) {
            elem.addEventListener("mouseover", overCard.bind(elem))
            elem.addEventListener("mouseout", outCard)
        }
    }
}

window.addEventListener("load", (e) => krcgCards())
