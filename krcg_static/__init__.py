"""Static files generator for third parties.

Produces static files for use in third parties softwares.
"""
import aiofile
import aiohttp
import argparse
import asyncio
import csv
import email.utils
import html.parser
import io
import json
import logging
import os
import pathlib
import re
import requests
import shutil
import sys
import urllib.request
import zipfile

from krcg import twda
from krcg import utils
from krcg import vtes


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
}
CARD_RENAME = {
    "akhenatenthesunpharaohmummy": "akhenatenthesunpharaoh",
    "amamthedevourerbanemummy": "amamthedevourerbane",
    "ambrosiustheferrymanwraith": "ambrosiustheferryman",
    "brigittegebauerwraith": "brigittegebauer",
    "carltonvanwykhunter": "carltonvanwyk",
    "dauntainblackmagicianchangeling": "dauntainblackmagician",
    "draevensoftfootchangeling": "draevensoftfoot",
    "felixfixhessianwraith": "felixfixhessian",
    "jakewashingtonhunter": "jakewashington",
    "kherebutubanemummy": "kherebutu",
    "khobartowers": "khobartowersalkhubar",
    "masquerwraith": "masquer",
    "mehemetoftheahlibatinmage": "mehemetoftheahlibatin",
    "mylanhorseedgoblin": "mylanhorseed",
    "neighborhoodwatchcommanderhunter": "neighborhoodwatchcommander",
    "nephandusmage": "nephandus",
    "pentexsubversion": "pentextmsubversion",
    "puppeteerwraith": "puppeteer",
    "qetutheevildoerbanemummy": "qetutheevildoer",
    "regomotus": "regomotum",
    "shadowcourtsatyrchangeling": "shadowcourtsatyr",
    "thadiuszhomage": "thadiuszho",
    "theadmonitions": "admonitionsthe",
    "theailingspirit": "ailingspiritthe",
    "theanarchfreepress": "anarchfreepressthe",
    "theancestorstalisman": "ancestorstalismanthe",
    "theankaracitadelturkey": "ankaracitadelturkeythe",
    "theankou": "ankouthe",
    "thearcadian": "arcadianthe",
    "theartoflove": "artoflovethe",
    "theartofmemory": "artofmemorythe",
    "theartofpain": "artofpainthe",
    "thebaron": "baronthe",
    "thebarrens": "barrensthe",
    "thebecoming": "becomingthe",
    "thebitterandsweetstory": "bitterandsweetstorythe",
    "theblackbeast": "blackbeastthe",
    "theblackthrone": "blackthronethe",
    "thebookofgoingforthbynight": "bookofgoingforthbynightthe",
    "thebruisers": "bruisersthe",
    "thecall": "callthe",
    "thecapuchin": "capuchinthe",
    "thechurchofvindicatedfaith": "churchofvindicatedfaiththe",
    "thecolonel": "colonelthe",
    "thecoven": "coventhe",
    "thecrimsonsentinel": "crimsonsentinelthe",
    "thecrocodiletemple": "crocodiletemplethe",
    "thecrusadersword": "crusaderswordthe",
    "thedamned": "damnedthe",
    "thedeadliestsin": "deadliestsinthe",
    "thedeathofmyconscience": "deathofmyconsciencethe",
    "thediamondthunderbolt": "diamondthunderboltthe",
    "thedowager": "dowagerthe",
    "thedracon": "draconthe",
    "theeldestarekholo": "eldestarekholothe",
    "theeldestcommandundeath": "eldestcommandundeaththe",
    "theembrace": "embracethe",
    "theerciyesfragments": "erciyesfragmentsthe",
    "theeternalmask": "eternalmaskthe",
    "theeternalsofsirius": "eternalsofsiriusthe",
    "thefinalnights": "finalnightsthe",
    "thefourthcycle": "fourthcyclethe",
    "theframing": "framingthe",
    "theghoulsofplazamorera": "ghoulsofplazamorerathe",
    "thegrandesttrick": "grandesttrickthe",
    "theguruhiaretheland": "guruhiarethelandthe",
    "thehaunting": "hauntingthe",
    "thehorde": "hordethe",
    "thehungrycoyote": "hungrycoyotethe",
    "thehuntclub": "huntclubthe",
    "thejones": "jonesthe",
    "thekhabarcommunity": "khabarcommunitythe",
    "thekhabarhonor": "khabarhonorthe",
    "thekikiyaon": "kikiyaonthe",
    "thekissofra": "kissofrathe",
    "theknights": "knightsthe",
    "thelabyrinth": "labyrinththe",
    "theline": "linethe",
    "thelouvreparis": "louvreparisthe",
    "themalkaviansevenmiseries": "malkaviansevenmiseriesthe",
    "themarrakeshcodex": "marrakeshcodexthe",
    "themausoleumvenice": "mausoleumvenicethe",
    "themeddlingofsemsith": "meddlingofsemsiththe",
    "themedic": "medicthe",
    "themissingvoice": "missingvoicethe",
    "themole": "molethe",
    "thenameforgotten": "nameforgottenthe",
    "thenewinquisition": "newinquisitionthe",
    "theoath": "oaththe",
    "theparthenon": "parthenonthe",
    "thepathofblood": "pathofbloodthe",
    "thepathofbone": "pathofbonethe",
    "thepathofharmony": "pathofharmonythe",
    "thepathoflilith": "pathofliliththe",
    "thepathofmetamorphosis": "pathofmetamorphosisthe",
    "thepathofnight": "pathofnightthe",
    "thepathofparadox": "pathofparadoxthe",
    "thepathofretribution": "pathofretributionthe",
    "thepathofservice": "pathofservicethe",
    "thepathoftears": "pathoftearsthe",
    "thepathoftheferalheart": "pathoftheferalheartthe",
    "thepathofthescorchedheart": "pathofthescorchedheartthe",
    "thepathoftyphon": "pathoftyphonthe",
    "thepeaceofkhetamon": "peaceofkhetamonthe",
    "theportrait": "portraitthe",
    "therack": "rackthe",
    "therealmoftheblacksun": "realmoftheblacksunthe",
    "theredquestion": "redquestionthe",
    "thereturntoinnocence": "returntoinnocencethe",
    "therising": "risingthe",
    "therose": "rosethe",
    "therosefoundation": "rosefoundationthe",
    "therumormilltabloidnewspaper": "rumormilltabloidnewspaperthe",
    "thesargonfragment": "sargonfragmentthe",
    "thesecretlibraryofalexandria": "secretlibraryofalexandriathe",
    "thesecretmustbekept": "secretmustbekeptthe",
    "thesiamese": "siamesethe",
    "thesignetofkingsaul": "signetofkingsaulthe",
    "theslashers": "slashersthe",
    "theslaughterhouse": "slaughterhousethe",
    "thesleepingmind": "sleepingmindthe",
    "theslowwithering": "slowwitheringthe",
    "thespawningpool": "spawningpoolthe",
    "thestatusperfectus": "statusperfectusthe",
    "thestrangeramongus": "strangeramongusthe",
    "thesummoning": "summoningthe",
    "thetextbookdamnation": "textbookdamnationthe",
    "thetreatment": "treatmentthe",
    "thetrickofthedanya": "trickofthedanyathe",
    "theuncoiling": "uncoilingthe",
    "theunmasking": "unmaskingthe",
    "theunnamed": "unnamedthe",
    "thewarrens": "warrensthe",
    "thewildebeest": "wildebeestthe",
    "theworldsacanvas": "worldsacanvasthe",
    "tututhedoublyevilonebanemummy": "tututhedoublyevilone",
    "wendelldelburtonhunter": "wendelldelburton",
}

logger = logging.getLogger()

parser = argparse.ArgumentParser(
    prog="krcg-static", description="VTES static files generator"
)
parser.add_argument("folder", help="Target folder", type=pathlib.Path)


def geonames(path: str) -> None:
    """Fetch countries and first order cities from geonames.org, save as JSON"""
    print("generating geographical data...")
    local_filename, _headers = urllib.request.urlretrieve(
        "https://download.geonames.org/export/dump/countryInfo.txt"
    )
    buffer = io.StringIO()
    with open(local_filename) as f:
        for line in f.readlines():
            if line[:1] == "#":
                continue
            buffer.write(line)
    buffer.seek(0)
    countries = list(
        csv.DictReader(
            buffer,
            delimiter="\t",
            fieldnames=[
                "iso",
                "iso3",
                "iso_numeric",
                "fips",
                "country",
                "capital",
                "area",
                "population",
                "continent",
                "tld",
                "currency_code",
                "currency_name",
                "phone",
                "postal_code_format",
                "postal_code_regex",
                "languages",
                "geoname_id",
                "neighbours",
                "equivalent_fips_code",
            ],
        )
    )
    for country in countries:
        try:
            country["languages"] = country["languages"].split(",")
            country["neighbours"] = country["neighbours"].split(",")
            country["geoname_id"] = (
                int(country["geoname_id"]) if country.get("geoname_id") else None
            )
            country["area"] = float(country["area"]) if country.get("area") else None
            country["population"] = int(country["population"])
            logger.info(country)
        except (KeyError, ValueError):
            logger.exception(f"Failed to parse country: {country}")
    with open(path / "data" / "countries.json", "w", encoding="utf-8") as fp:
        json.dump(utils.json_pack(countries), fp, ensure_ascii=False)
    local_filename, _headers = urllib.request.urlretrieve(
        "https://download.geonames.org/export/dump/cities15000.zip"
    )
    z = zipfile.ZipFile(local_filename)
    cities = list(
        csv.DictReader(
            io.TextIOWrapper(z.open("cities15000.txt")),
            delimiter="\t",
            fieldnames=[
                "geoname_id",  # integer id of record in geonames database
                "name",  # name of geographical point (utf8) varchar(200)
                "ascii_name",  # name of geographical point in plain ascii characters
                "alternate_names",  # alternate ascii names automatically transliterated
                "latitude",  # latitude in decimal degrees (wgs84)
                "longitude",  # longitude in decimal degrees (wgs84)
                "feature_class",  # see http://www.geonames.org/export/codes.html
                "feature_code",  # see http://www.geonames.org/export/codes.html
                "country_code",  # ISO-3166 2-letter country code, 2 characters
                "cc2",  # alternate country codes, ISO-3166 2-letter country code
                "admin1_code",  # fipscode (subject to change to iso code)
                "admin2_code",  # code for the second administrative division
                "admin3_code",  # code for third level administrative division
                "admin4_code",  # code for fourth level administrative division
                "population",  # integer
                "elevation",  # in meters, integer
                "dem",  # digital elevation model, srtm3 or gtopo30, integer
                "timezone",  # iana timezone id
                "modification_date",  # date of last modification in ISO format
            ],
        )
    )
    for city in cities:
        city["geoname_id"] = int(city["geoname_id"])
        city["latitude"] = float(city["latitude"])
        city["longitude"] = float(city["longitude"])
        city["cc2"] = city["cc2"].split(",")
        city["population"] = int(city["population"])
        city["elevation"] = int(city["elevation"] or 0)
        city["dem"] = int(city["dem"] or 0)
        city["alternate_names"] = city["alternate_names"].split(",")
    with open(path / "data" / "cities.json", "w", encoding="utf-8") as fp:
        json.dump(utils.json_pack(cities), fp, ensure_ascii=False)


def amaranth_ids(path: str) -> None:
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
        place = deck.place or "Undisclosed location"
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
    await asyncio.gather(
        *(
            fetch_file(card, path / url_to_filename(card), session)
            for card in parser.cards
        )
    )


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
    shutil.rmtree(path, ignore_errors=True)
    shutil.copytree(
        "static",
        path,
        symlinks=True,
        ignore=lambda _dir, names: [n for n in names if n[-3:] == ".py"],
    )


def main():
    """Entrypoint for the krcg-gen tool."""
    args = parser.parse_args(sys.argv[1:])
    static(args.folder)
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
