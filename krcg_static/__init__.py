"""Static files generator for third parties.

Produces static files for use in third parties softwares.
"""
import aiofile
import aiohttp
import argparse
import asyncio
import email.utils
import html.parser
import json
import logging
import os
import pathlib
import re
import requests
import shutil
import sys

from krcg import twda
from krcg import vtes


CARD_IMAGES_URL = "https://lackeyccg.com/vtes/high/cards/"

logger = logging.getLogger()

parser = argparse.ArgumentParser(
    prog="krcg-static", description="VTES static files generator"
)
parser.add_argument("folder", help="Target folder", type=pathlib.Path)


def amaranth_ids(path: str):
    print("generating Amaranth IDs file...")
    with open(path / "data" / "amaranth_ids.json", "w", encoding="utf-8") as fp:
        r = requests.get("https://amaranth.vtes.co.nz/api/cards", timeout=30)
        r.raise_for_status()
        json.dump(
            {
                int(card["id"]): vtes.VTES[card["name"]].id
                for card in r.json()["result"]
                if card["name"] in vtes.VTES  # ignore storyline / counter cards
            },
            fp,
            ensure_ascii=False,
        )


def standard_json(path: str) -> None:
    print("generating JSON files...")
    path.mkdir(parents=True, exist_ok=True)
    with open(path / "data" / "vtes.json", "w", encoding="utf-8") as fp:
        json.dump(vtes.VTES.to_json(), fp, ensure_ascii=False)
    with open(path / "data" / "twda.json", "w", encoding="utf-8") as fp:
        json.dump(twda.TWDA.to_json(), fp, ensure_ascii=False)


def standard_html(path: str) -> None:
    """A normalized HTML version of the TWDA"""
    print("generating HTML TWD file...")
    # TODO: automatize header generation, so as not to edit it every year
    content = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>TWDA</title></head>

<body>
<center>
<h1>Tournament Winning Deck Archive</h1>
<h2>Formerly hosted on the Lasombra</h2>

<p>
This is a chronological archive of decks that have won tournaments that were<br>
sanctioned by the Vampire: Elder Kindred Network and had 10 or more players.<br>
National and Continental Championship are included as well, irrelatively to their attendance.<br>
To be included in this list, a tournament report had to be made on the official V:EKN Player's Forum:<br>
<a href="http://www.vekn.net/index.php/forum/9-event-reports-and-twd">http://www.vekn.net/index.php/forum/9-event-reports-and-twd</a><br>
This archive will not include the Storyline Tournament Winning Decks.<br>
Unless otherwise noted, each deck was the winning player's creation.<br>
<br>
The original <a href="http://www.thelasombra.com/hall_of_fame.htm">Hall of Fame</a> and the <a href="http://www.veknfrance.com/decks/twd.htm">Tournament Winning Deck Archive</a> were closed as of October 26, 2013.<br>
Many thanks to Jeff Thompson for maintaining them for all these years.
</p>
<table width="500" align="center" border="2" cellpadding="0">
<tbody><tr align="center">
<td colspan="10">You can jump to the end of a year that interests you:</td>
</tr>
<tr align="center">
<td colspan="3"></td>
<td><a href="#Year2020">2020</a></td>
<td><a href="#Year2019">2019</a></td>
<td><a href="#Year2018">2018</a></td>
<td><a href="#Year2017">2017</a></td>
<td colspan="3"></td>
</tr><tr align="center">
<td><a href="#Year2016">2016</a></td>
<td><a href="#Year2015">2015</a></td>
<td><a href="#Year2014">2014</a></td>
<td><a href="#Year2013">2013</a></td>
<td><a href="#Year2012">2012</a></td>
<td><a href="#Year2011">2011</a></td>
<td><a href="#Year2010">2010</a></td>
<td><a href="#Year2009">2009</a></td>
<td><a href="#Year2008">2008</a></td>
<td><a href="#Year2007">2007</a></td>
</tr><tr align="center">
<td><a href="#Year2006">2006</a></td>
<td><a href="#Year2005">2005</a></td>
<td><a href="#Year2004">2004</a></td>
<td><a href="#Year2003">2003</a></td>
<td><a href="#Year2002">2002</a></td>
<td><a href="#Year2001">2001</a></td>
<td><a href="#Year2000">2000</a></td>
<td><a href="#Year1999">1999</a></td>
<td><a href="#Year1998">1998</a></td>
<td><a href="#Year1997">1997</a></td>
</tr>
</tbody></table>
<p>Some abbreviations are used throughout the archive:
<table>
<tr><td>NC</td><td>National Championship</td><td>NAC</td><td>North American (Continental) Championship</td></tr>
<tr><td>NCQ</td><td>National Championship Qualifier</td><td>SAC</td><td>South American (Continental) Championship</td></tr>
<tr><td>ECQ</td><td>European Championship Qualifier</td><td>EC</td><td>European (Continental) Championship</td></tr>
<tr><td>CCQ</td><td>Continental Championship Qualifier</td><td>ACC</td><td>Asian Continental Championship</td></tr>
</table>"""  # noqa: E501
    decks = sorted(twda.TWDA.values(), key=lambda a: a.date, reverse=True)
    current_year = None
    # header: list of decks, year after year
    for deck in decks:
        if current_year != deck.date.year:
            current_year = deck.date.year
            content += f'\n<h3><a id="Year{current_year}">{current_year}</a></h3>\n\n'
        player = deck.player
        assert player, f"no player indicated for deck #{deck.id}"
        if player[-1] == "s":
            player += "'"
        else:
            player += "'s"
        event = deck.event
        event = re.sub(r"\s*--\s+.*", "", event)
        place = deck.place
        place = re.sub(r"\s*,", ",", place)
        place = re.sub(r",,", ",", place)
        place = [x.strip() for x in place.split(",")[-2:]]
        event = event.strip().strip(":")
        if event[-len(place[0]) :] == place[0]:
            place = place[1:]
            event = event.strip().strip(":") + ","
        else:
            event = event.strip().strip(":") + ":"
        place = ", ".join(place)
        content += (
            f"<a href=#{deck.id}>{player} {event} {place} "
            f"{deck.date.strftime('%B %Y')}</a><br>\n"
        )
    content += "</center>\n"
    # body: list of decklists
    for deck in decks:
        content += f"<a id={deck.id} href=#>Top</a>\n<hr><pre>\n"
        content += deck.to_txt()
        content += "\n</pre>\n"
    with open(path / "data" / "twd.htm", "w", encoding="utf-8") as fp:
        fp.write(content)


class IndexParser(html.parser.HTMLParser):
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


async def fetch_file(path, session, card):
    """Fetch image files, preserve "last-mofidifed" time."""
    async with session.get(CARD_IMAGES_URL + card) as response:
        time = email.utils.mktime_tz(
            email.utils.parsedate_tz(response.headers["Last-Modified"])
        )
        content = await response.read()
    dst = path / "card" / card
    async with aiofile.async_open(dst, "wb") as afp:
        await afp.write(content)
    os.utime(dst, (time, time))


async def fetch_lackey_card_images(path):
    parser = IndexParser()
    async with aiohttp.ClientSession() as session:
        async with session.get(CARD_IMAGES_URL) as response:
            index = await response.text()
            parser.feed(index)
        await asyncio.gather(
            *(fetch_file(path, session, card) for card in parser.cards)
        )


def card_images(path):
    print("copying card images...")
    i18n = pathlib.Path("i18n_cards")
    for lang in os.listdir(i18n):
        (path / "card" / lang).mkdir(parents=True, exist_ok=True)
        for card in os.listdir(i18n / lang):
            dst, ext = card.rsplit(".", 1)
            dst = dst.split("_")
            if len(dst) > 1:
                dst = dst[1]
            else:
                dst = dst[0]
            dst = re.sub(r"[^\w\d]", "", dst).lower() + "." + ext
            shutil.copyfile(i18n / lang / card, path / "card" / lang / dst)
    asyncio.run(fetch_lackey_card_images(path))


def static(path):
    print("setting up website files...")
    shutil.rmtree(path, ignore_errors=True)
    shutil.copytree("static", path)


def main():
    """Entrypoint for the krcg-gen tool."""
    args = parser.parse_args(sys.argv[1:])
    static(args.folder)
    card_images(args.folder)
    try:
        print("loading from VEKN...")
        vtes.VTES.load_from_vekn()
        twda.TWDA.load_from_vekn()
    except requests.exceptions.ConnectionError as e:
        logger.exception("failed to connect to %s", e.request.url)
        exit(1)
    (args.folder / "data").mkdir(parents=True, exist_ok=True)
    standard_json(args.folder)
    standard_html(args.folder)
    amaranth_ids(args.folder)
