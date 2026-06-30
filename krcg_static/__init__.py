"""Static files generator for third parties.

Produces static files for use in third parties softwares.
"""

import aiofile
import aiohttp
import argparse
import asyncio
import email.utils
import html.parser
import inspect
import json
import logging
import os
import pathlib
import re
import shutil
import sys
import zipfile

import msgspec

from krcg import loader
from krcg import twda

CARD_IMAGES_URL = "https://lackeyccg.com/vtes/high/cards/"
CARD_LIBRARY_BACK_URL = "https://lackeyccg.com/vtes/high/images/cardback.jpg"
VTES_PL_SETS_URLS = {
    "jyhad": "http://vtes.pl/cards/set/jyhad",
    "vampire-the-eternal-struggle": "http://vtes.pl/cards/set/vtes",
    "dark-sovereigns": "http://vtes.pl/cards/set/ds",
    "ancient-hearts": "http://vtes.pl/cards/set/ah",
    "sabbat": "http://vtes.pl/cards/set/sabbat",
    "sabbat-war": "http://vtes.pl/cards/set/sw",
    "final-nights": "http://vtes.pl/cards/set/fn",
    "bloodlines": "http://vtes.pl/cards/set/bl",
    "camarilla-edition": "http://vtes.pl/cards/set/ce",
    "anarchs": "http://vtes.pl/cards/set/anarchs",
    "black-hand": "http://vtes.pl/cards/set/bh",
    "gehenna": "http://vtes.pl/cards/set/gehenna",
    "tenth-anniversary": "http://vtes.pl/cards/set/tenth",
    "kindred-most-wanted": "http://vtes.pl/cards/set/kmw",
    "legacies-of-blood": "http://vtes.pl/cards/set/lob",
    "nights-of-reckoning": "http://vtes.pl/cards/set/nor",
    "third-edition": "http://vtes.pl/cards/set/3e",
    "sword-of-caine": "http://vtes.pl/cards/set/soc",
    "lords-of-the-night": "http://vtes.pl/cards/set/lotn",
    "blood-shadowed-court": "http://vtes.pl/cards/set/bsc",
    "twilight-rebellion": "http://vtes.pl/cards/set/tr",
    "keepers-of-tradition": "http://vtes.pl/cards/set/kot",
    "ebony-kingdom": "http://vtes.pl/cards/set/ek",
    "heirs-to-the-blood": "http://vtes.pl/cards/set/httb",
    "anthology": "http://vtes.pl/cards/set/anth",
    "lost-kindred": "http://vtes.pl/cards/set/lk",
    "sabbat-preconstructed": "http://vtes.pl/cards/set/sp",
    "twenty-fifth-anniversary": "http://vtes.pl/cards/set/25th",
    "first-blood": "http://vtes.pl/cards/set/fb",
    "promo": "http://vtes.pl/cards/set/promo",
    "demo-decks": "http://vtes.pl/cards/set/dd",
    "infernal-storyline": "http://vtes.pl/cards/set/isl",
    "cultists-storyline": "http://vtes.pl/cards/set/csl",
    "anarchs-and-alastor-storyline": "http://vtes.pl/cards/set/aa",
    "fall-edens-legacy-storyline": "http://vtes.pl/cards/set/el",
    "keepers-of-tradition-reprint": "http://vtes.pl/cards/set/kotr",
    "heirs-to-the-blood-reprint": "http://vtes.pl/cards/set/httbr",
    "humble-bundle": "http://vtes.pl/cards/set/promohb",
    "anthology-1": "http://vtes.pl/cards/set/anth1",
    "promo-pack-1": "http://vtes.pl/cards/set/pp1",
    # we have BCP cards images for the newest sets, do not sync them
    # "anthology-reprint": "http://vtes.pl/cards/set/anth1r",
    # "twenty-fifth-reprint": "http://vtes.pl/cards/set/25thr",
    # "promo-pack-2": "http://vtes.pl/cards/set/pp2",
    # "fifth-edition": "http://vtes.pl/cards/set/v5",
    # "fifth-edition-anarch": "http://vtes.pl/cards/set/v5a",
    # "fall-of-london": "http://vtes.pl/cards/set/fol",
    # "new-blood": "http://vtes.pl/cards/set/nb",
    # "shadows-of-berlin": "http://vtes.pl/cards/set/sob",
    # "echoes-of-gehenna": "http://vtes.pl/set/view/eog",
    # "new-blood-2": "http://vtes.pl/cards/set/nb2",
    # "fifth-edition-companion": "http://vtes.pl/cards/set/v5c",
    # "thirtieth-anniversary": "http://vtes.pl/cards/set/30th",
}
CARD_RENAME = {
    "abrahammellon": "abrahammellong6",
    "akhenatenthesunpharaohmummy": "akhenatenthesunpharaoh",
    "alinegadecke": "alinegadekeg6",
    "amamthedevourerbanemummy": "amamthedevourer",
    "ambrosiustheferrymanwraith": "ambrosiustheferryman",
    "brigittegebauerwraith": "brigittegebauer",
    "carltonvanwykhunter": "carltonvanwyk",
    "dauntainblackmagicianchangeling": "dauntainblackmagician",
    "draevensoftfootchangeling": "draevensoftfoot",
    "felixfixhessianwraith": "felixfixhessian",
    "gustaphebrunelle": "gustaphebrunnelle",
    "irisbennet": "irisbennett",
    "jakewashingtonhunter": "jakewashington",
    "kherebutubanemummy": "kherebutu",
    "khobartowers": "khobartowersalkhubar",
    "lutzvonhoenzollern": "lutzvonhohenzollern",
    "masquerwraith": "masquer",
    "mehemetoftheahlibatinmage": "mehemetoftheahlibatin",
    "mylanhorseedgoblin": "mylanhorseed",
    "neighborhoodwatchcommanderhunter": "neighborhoodwatchcommander",
    "nephandusmage": "nephandus",
    "niksicko": "niksikkog6",
    "pentexsubversion": "pentextmsubversion",
    "puppeteerwraith": "puppeteer",
    "qetutheevildoerbanemummy": "qetutheevildoer",
    "regomotus": "regomotum",
    "sacrecourcathedralfrance": "sacrecoeurcathedralfrance",
    "sebastiangoulet": "sebastiengoulet",
    "shadowcourtsatyrchangeling": "shadowcourtsatyr",
    "tarathehollowonemage": "tarathehollowone",
    "thadiuszhomage": "thadiuszho",
    "thefirsttraditionthemasquerade": "firsttraditionthemasquerade",
    "tututhedoublyevilonebanemummy": "tututhedoublyevilone",
    "wendelldelburtonhunter": "wendelldelburton",
}

logger = logging.getLogger()

parser = argparse.ArgumentParser(
    prog="krcg-static", description="VTES static files generator"
)
parser.add_argument("folder", help="Target folder", type=pathlib.Path)
parser.add_argument(
    "--minimal", action="store_true", help="Re-generate just the static web files"
)
parser.add_argument(
    "--data",
    action="store_true",
    help="Re-generate just the data files (cards, TWDA) — for frequent re-runs",
)


def standard_json(path, cards, archive) -> None:
    """Generate the v5 reference JSON: cards, expansions and the TWDA.

    The layout mirrors what `krcg.load_online` expects under `/data/v5/`.
    """
    print("generating v5 JSON files...")
    target = path / "data" / "v5"
    target.mkdir(parents=True, exist_ok=True)
    with open(target / "vtes.json", "w", encoding="utf-8") as fp:
        json.dump(
            [msgspec.to_builtins(c) for c in cards.cards()], fp, ensure_ascii=False
        )
    # cards.sets maps several keys (id, code, name) to each Set: dedupe by identity
    expansions = {id(s): s for s in cards.sets.values()}
    with open(target / "expansions.json", "w", encoding="utf-8") as fp:
        json.dump(
            [
                msgspec.to_builtins(s)
                for s in sorted(expansions.values(), key=lambda s: s.id)
            ],
            fp,
            ensure_ascii=False,
        )
    with open(target / "twda.json", "w", encoding="utf-8") as fp:
        json.dump(msgspec.to_builtins(archive), fp, ensure_ascii=False)


def all_cards_images(path: str) -> None:
    print("generating ZIP file for all cards images...")
    source = pathlib.Path("static/card")
    with zipfile.ZipFile(path / "card" / "_all_cards.zip", "w") as zipf:
        for fil in os.listdir(source):
            fil = source / fil
            if (
                fil.suffix == ".webp"
                and os.path.isfile(fil)
                and not os.path.islink(fil)
            ):
                zipf.write(fil, fil.relative_to("static"))


class LackeyIndexParser(html.parser.HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cards = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        url = dict(attrs)["href"]
        if url[-3:] != "jpg":
            return
        self.cards.append(url)


async def fetch_file(url, path, session):
    """Fetch image files, preserve "last-mofidifed" time."""
    time = None
    async with session.get(url) as response:
        if "Last-Modified" in response.headers:
            time = email.utils.mktime_tz(
                email.utils.parsedate_tz(response.headers["Last-Modified"])
            )
        content = await response.read()
    async with aiofile.async_open(path, "wb") as afp:
        await afp.write(content)
    if time:
        os.utime(path, (time, time))


async def fetch_lackey_card_images(path):
    parser = LackeyIndexParser()
    async with aiohttp.ClientSession() as session:
        async with session.get(CARD_IMAGES_URL) as response:
            index = await response.text()
            parser.feed(index)
        await asyncio.gather(
            fetch_file(
                CARD_LIBRARY_BACK_URL, path / "card" / "cardbacklibrary.jpg", session
            ),
            *(
                fetch_file(CARD_IMAGES_URL + card, path / "card" / card, session)
                for card in parser.cards
            ),
        )


class VtesPlIndexParser(html.parser.HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cards = []

    def handle_starttag(self, tag, attrs):
        if tag != "img":
            return
        url = dict(attrs).get("onmouseover")
        if not url:
            return
        url = re.search(r"'<IMG class=overlib src=([^>]*)", url).group(1)
        if url[-3:] != "jpg":
            return
        self.cards.append(url)


def url_to_filename(url):
    name, ext = url.rsplit("/", 1)[1].rsplit(".", 1)
    name = CARD_RENAME.get(name, name)
    return name + "." + ext


async def fetch_vtespl_set_images(session, path, url):
    path.mkdir(parents=True, exist_ok=True)
    parser = VtesPlIndexParser()
    async with session.get(url) as response:
        index = await response.text()
        parser.feed(index)
    # don't gather here to avoid opening too many files
    for card in parser.cards:
        await fetch_file(card, path / url_to_filename(card), session)


async def fetch_vtespl_cards_scans(path):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *(
                fetch_vtespl_set_images(session, path / "card" / "set" / expansion, url)
                for expansion, url in VTES_PL_SETS_URLS.items()
            )
        )


def vtespl_cards_scans(path):
    print("copying vtes.pl card images...")
    asyncio.run(fetch_vtespl_cards_scans(path))


def static(path):
    print("setting up website files...")
    shutil.copytree(
        "static",
        path,
        symlinks=True,
        ignore=lambda _dir, names: [n for n in names if n[-3:] == ".py"],
        dirs_exist_ok=True,
    )


def load_twda(cards):
    """Build a current TWDA from its source, else the packaged krcg snapshot.

    A daily/hourly data refresh wants the live TWDA; `fetch_from_source` is only
    in recent krcg, and needs the network, so any failure falls back gracefully.
    """
    try:
        return twda.fetch_from_source(cards)
    except Exception as e:
        logger.warning("TWDA source fetch unavailable, using snapshot: %s", e)
        return twda.load_local()


def card_image_manifest(source="static/card"):
    """Image paths (relative to `/card/`) that resolve to a file on disk.

    Passed to `loader.load_local` so krcg emits image URLs only for variants we
    actually host: the card itself, its `<lang>/` translations and its
    `set/<set>/` prints. Symlinks (legacy back-form aliases) that resolve count.
    """
    source = pathlib.Path(source)
    manifest = set()
    for root, _dirs, files in os.walk(source):
        rel_root = pathlib.Path(root).relative_to(source)
        for name in files:
            if os.path.isfile(pathlib.Path(root) / name):  # follows symlinks
                manifest.add((rel_root / name).as_posix())
    return manifest


def load_cards():
    """Load cards, pruning image URLs to the variants we host when supported.

    krcg only links images listed in the manifest it is given; older krcg
    without that parameter links every set/language variant optimistically.
    """
    if "available" in inspect.signature(loader.load_local).parameters:
        return loader.load_local(available=card_image_manifest())
    return loader.load_local()


def generate_data(path, cards, archive):
    """Generate the v5 reference JSON.

    All v4 data (vtes/twda/twd.htm/amaranth_ids) is a frozen static snapshot
    shipped as-is from `static/data/v4/`; it is never regenerated by the build.
    """
    standard_json(path, cards, archive)


def main():
    """Entrypoint for the krcg-gen tool."""
    args = parser.parse_args(sys.argv[1:])
    if args.minimal:
        print("setting up website files...")
        shutil.copytree(
            "static",
            args.folder,
            symlinks=True,
            ignore=lambda folder, names: (
                names
                if folder == "static/card"
                else [n for n in names if n[-3:] == ".py"]
            ),
            dirs_exist_ok=True,
        )
        return
    if args.data:
        print("setting up data files...")
        shutil.copytree(
            "static/data", args.folder / "data", symlinks=True, dirs_exist_ok=True
        )
        print("loading card and TWDA data...")
        cards = load_cards()
        generate_data(args.folder, cards, load_twda(cards))
        return
    shutil.rmtree(args.folder, ignore_errors=True)
    static(args.folder)
    all_cards_images(args.folder)
    print("loading card and TWDA data...")
    cards = loader.load_local()
    generate_data(args.folder, cards, load_twda(cards))
