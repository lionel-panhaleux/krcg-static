const icon_map = {
    "aus": "a",
    "obe": "b",
    "cel": "c",
    "dom": "d",
    "dem": "e",
    "for": "f",
    "san": "g",
    "thn": "h",
    "ani": "i",
    "pro": "j",
    "chi": "k",
    "val": "l",
    "mel": "m",
    "nec": "n",
    "obf": "o",
    "pot": "p",
    "qui": "q",
    "pre": "r",
    "ser": "s",
    "tha": "t",
    "vis": "u",
    "vic": "v",
    "abo": "w",
    "myt": "x",
    "dai": "y",
    "spi": "z",
    "AUS": "A",
    "OBE": "B",
    "CEL": "C",
    "DOM": "D",
    "DEM": "E",
    "FOR": "F",
    "SAN": "G",
    "THN": "H",
    "ANI": "I",
    "PRO": "J",
    "CHI": "K",
    "VAL": "L",
    "MEL": "M",
    "NEC": "N",
    "OBF": "O",
    "POT": "P",
    "QUI": "Q",
    "PRE": "R",
    "SER": "S",
    "THA": "T",
    "VIS": "U",
    "VIC": "V",
    "ABO": "W",
    "MYT": "X",
    "DAI": "Y",
    "SPI": "Z",
    "tem": "?",
    "TEM": "!",
    "str": "à",
    "STR": "á",
    "obt": "$",
    "OBT": "£",
    "mal": "â",
    "MAL": "ã",
    "conviction": "¤",
    "action": "0",
    "political": "2",
    "politics": "2",
    "politic": "2",
    "political action": "2",
    "ally": "3",
    "recruit": "3",
    "equipment": "5",
    "equip": "5",
    "retainer": "8",
    "employ": "8",
    "reaction": "7",
    "react": "7",
    "action modifier": "1",
    "modifier": "1",
    "mod": "1",
    "combat": "4",
    "reflex": "6",
    "flight": "^",
    "merged": "µ ",
    "merge": "µ ",
    "advanced": "|",
    "advance": "|",
    "adv": "|",
    "event": "[",
    "power": "§",
    "innocence": "#",
    "inn": "#",
    "defense": "@",
    "def": "@",
    "martyrdom": "&",
    "mar": "&",
    "justice": "%",
    "jus": "%",
    "vengeance": "(",
    "ven": "(",
    "vision": ")",
    "vin": ")",
    "redemption": "*",
    "red": "*",
    "1 blood": "'",
    "1 b": "'",
    "1b": "'",
    "2 blood": ";",
    "2 b": ";",
    "2b": ";",
    "3 blood": ".",
    "3 b": ".",
    "3b": ".",
    "4 blood": ",",
    "4 b": ",",
    "4b": ",",
    "x blood": "-",
    "x b": "-",
    "xb": "-",
    "X blood": "-",
    "X b": "-",
    "Xb": "-",
    "pool": "¦",
    "1 pool": "\"",
    "1 p": "\"",
    "1p": "\"",
    "2 pool": ":",
    "2 p": ":",
    "2p": ":",
    "3 pool": "/",
    "3 p": "/",
    "3p": "/",
    "4 pool": "\\",
    "4 p": "\\",
    "4p": "\\",
    "5 pool": "]",
    "5 p": "]",
    "5p": "]",
    "6 pool": "`",
    "6 p": "`",
    "6p": "`",
    "x pool": "_",
    "x p": "_",
    "xp": "_",
    "X pool": "_",
    "X p": "_",
    "X P": "_",
    "Xp": "_",
    "XP": "_",
}

const clan_map = {
    "abomination": "A",
    "abominations": "A",
    "abo": "A",
    "ahrimane": "B",
    "ahrimanes": "B",
    "akunanse": "C",
    "assamite": "n",
    "avenger": "1",
    "baali": "E",
    "banu haqim": "n",
    "banu": "n",
    "haqim": "n",
    "blood brother": "F",
    "blood brothers": "F",
    "brujah": "o",
    "brujah antitribu": "H",
    "!brujah": "H",
    "caitiff": "I",
    "daughter of cacophony": "J",
    "daughters of cacophony": "J",
    "daughter": "J",
    "daughters": "J",
    "defender": "2",
    "follower of set": "r",
    "followers": "r",
    "fos": "r",
    "followers of set": "r",
    "gangrel": "p",
    "gangrel antitribu": "M",
    "!gangrel": "M",
    "gargoyle": "N",
    "giovanni": "O",
    "giov": "O",
    "guruhi": "P",
    "harbinger of skulls": "Q",
    "harbinger": "Q",
    "hos": "Q",
    "innocent": "3",
    "ishtarri": "R",
    "ishtar": "R",
    "judge": "4",
    "kiasyd": "S",
    "lasombra": "w",
    "malkavian": "q",
    "malkavien": "q",
    "malk": "q",
    "malkavian antitribu": "V",
    "malkavian anti": "V",
    "malkavien antitribu": "V",
    "malkavien anti": "V",
    "!malkavian": "V",
    "!malkavien": "V",
    "!malk": "V",
    "martyr": "5",
    "ministry": "r",
    "nagaraja": "W",
    "naga": "W",
    "nosferatu": "s",
    "nosfe": "s",
    "nosferatu antitribu": "Y",
    "nosferatu anti": "Y",
    "nosfe antitribu": "Y",
    "nosfe anti": "Y",
    "!nosferatu": "Y",
    "!nosfe": "Y",
    "osebo": "Z",
    "pander": "a",
    "ravnos": "b",
    "redeemer": "6",
    "salubri": "c",
    "salu": "c",
    "salubri antitribu": "d",
    "salu antitribu": "d",
    "!salubri": "d",
    "!salu": "d",
    "samedi": "e",
    "toreador": "t",
    "toréador": "t",
    "toré": "t",
    "tore": "t",
    "toreador antitribu": "g",
    "toreador anti": "g",
    "toréador antitribu": "g",
    "toréador anti": "g",
    "toré antitribu": "g",
    "toré anti": "g",
    "tore antitribu": "g",
    "tore anti": "g",
    "!toreador": "g",
    "!tore": "g",
    "!toréador": "g",
    "!toré": "g",
    "tremere": "u",
    "tremere antitribu": "i",
    "tremere anti": "i",
    "!tremere": "i",
    "true brujah": "j",
    "tzimisce": "k",
    "ventrue": "v",
    "ventrue antitribu": "m",
    "ventrue anti": "m",
    "!ventrue": "m",
    "visionary": "7",
}

async function fetchDeck(url) {
    const response = await fetch(encodeURI(`https://api.krcg.org/vdb`), {
        method: "POST",
        body: JSON.stringify({ url: url }),
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
    })
    if (!response.ok) {
        if (response.status >= 500 && response.status < 600) {
            throw Error("KRCG server error")
        } else if (response.status >= 404 && response.status < 600) {
            throw Error(`Deck #${id} not found.`)
        } else {
            throw Error(response.statusText)
        }
    }
    return await response.json()
}

function addCard(section, card_info) {
    let elem = document.createElement("li")
    elem.textContent = `${card_info.count} `
    let card = document.createElement("span")
    card.textContent = card_info.name
    card.classList.add("krcg-card")
    elem.appendChild(card)
    section.appendChild(elem)
}

function wrapText(text, maxlen) {
    if (!text) {
        return "(N/A)"
    }
    if (text.length > maxlen) {
        return text.substr(0, maxlen - 3) + "..."
    }
    return text
}

async function insert_decklist(elem, url) {
    const data = await fetchDeck(url)
    console.log(data)
    let decklist = document.createElement("div")
    decklist.classList.add("krcg-decklist")
    let deck_name = document.createElement("h3")
    decklist.appendChild(deck_name)
    let deck_link = document.createElement("a")
    deck_link.target = "_blank"
    deck_link.href = url
    deck_link.textContent = wrapText(data.name || "(No Name)", 25)
    deck_name.appendChild(deck_link)
    let row = document.createElement("div")
    row.classList.add("krcg-row")
    let column1 = document.createElement("div")
    column1.classList.add("krcg-column")
    let column2 = document.createElement("div")
    column2.classList.add("krcg-column")
    let crypt_header = document.createElement("h4")
    crypt_header.textContent = `Crypt (${data.crypt.count})`
    column1.appendChild(crypt_header)
    let crypt_list = document.createElement("ul")
    for (card_info of data.crypt.cards) {
        addCard(crypt_list, card_info)
    }
    column1.appendChild(crypt_list)
    let library_header = document.createElement("h4")
    library_header.textContent = `Library (${data.library.count})`
    column1.appendChild(library_header)
    let library_list = document.createElement("ul")
    for (const section of data.library.cards) {
        let header = document.createElement("li")
        let title = document.createElement("h5")
        title.textContent = `— ${section.type} (${section.count}) —`
        header.appendChild(title)
        library_list.appendChild(header)
        for (card_info of section.cards) {
            addCard(library_list, card_info)
        }
        if (section.type === "Master") {
            column1.appendChild(library_list)
            row.appendChild(column1)
            library_list = document.createElement("ul")
        }
    }
    column2.appendChild(library_list)
    row.appendChild(column2)
    decklist.appendChild(row)
    elem.after(decklist)
    elem.remove()
}

async function krcgBlogger() {
    // modify all spans with the "courier" font
    for (elem of document.querySelectorAll('span[style="font-family: courier;"]')) {
        const category = elem.textContent.split(":", 1)[0]
        const value = elem.textContent.slice(category.length + 1).trim()
        switch (category) {
            case "disc":
            case "discipline":
            case "icon":
                elem.removeAttribute("style")
                elem.setAttribute("class", "krcg-icon")
                elem.textContent = icon_map[value]
                break
            case "clan":
                elem.removeAttribute("style")
                elem.setAttribute("class", "krcg-clan")
                elem.textContent = clan_map[value.toLowerCase()]
                break
            case "card":
                elem.removeAttribute("style")
                elem.setAttribute("class", "krcg-card")
                elem.textContent = value
                break
            case "decklist":
                elem.removeAttribute("style")
                await insert_decklist(elem, value)
        }
    }
}

async function setup_krcg_blogger(e) {
    await krcgBlogger()
}

window.addEventListener("DOMContentLoaded", setup_krcg_blogger)
