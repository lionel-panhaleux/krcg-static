import os.path
import textwrap

from krcg import twda
from krcg import vtes


def test_card():
    assert vtes.VTES["Aid from Bats"].to_json() == {
        "_i18n": {
            "es": {
                "card_text": (
                    "[ani] Ataque: 1 de daño a distancia, con 1 maniobra opcional.\n"
                    "[ANI] Como antes, con 1 acoso opcional."
                ),
                "flavor_text": (
                    "Colgando boca abajo como hileras de trapos viejos y repugnantes\n"
                    "Y sonriendo mientras duermen. ¡Murciélagos!\n"
                    'D.H. Lawrence, "Murciélago"'
                ),
                "name": "Ayuda de murciélagos",
                "sets": {"First Blood": "Primera Sangre"},
                "url": "https://static.krcg.org/card/es/aidfrombats.jpg",
            },
            "fr": {
                "card_text": (
                    "[ani] Frapper à toute portée : 1 point de dégâts, "
                    "avec 1 manœuvre optionnelle.\n"
                    "[ANI] Comme ci-dessus, avec 1 poursuite optionnelle."
                ),
                "flavor_text": (
                    "Pendues tête en bas comme des rangées de guenilles repoussantes\n"
                    "Et souriant de toutes leurs dents dans leur sommeil. "
                    "Des chauves-souris !\n"
                    'D.H. Lawrence, "La Chauve-souris"'
                ),
                "name": "Aide des chauves-souris",
                "sets": {"First Blood": "Premier Sang"},
                "url": "https://static.krcg.org/card/fr/aidfrombats.jpg",
            },
        },
        "_name": "Aid from Bats",
        "_set": "Jyhad:C, VTES:C, CE:C/PN3, Anarchs:PG2, Third:C, KoT:C, FB:PN6",
        "artists": ["Melissa Benson", "Eric Lofgren"],
        "card_text": (
            "[ani] Strike: 1R damage, with 1 optional maneuver.\n"
            "[ANI] As above, with 1 optional press."
        ),
        "disciplines": ["ani"],
        "flavor_text": (
            "Hanging upside down like rows of disgusting old rags\n"
            "And grinning in their sleep. Bats!\n"
            'D.H. Lawrence, "Bat"'
        ),
        "id": 100029,
        "legality": "1994-08-16",
        "name": "Aid from Bats",
        "printed_name": "Aid from Bats",
        "rulings": [
            {
                "cards": [
                    {
                        "id": 100916,
                        "name": "Hidden Lurker",
                        "text": "{Hidden Lurker}",
                        "usual_name": "Hidden Lurker",
                        "vekn_name": "Hidden Lurker",
                    },
                ],
                "group": "Strikes with optional maneuver",
                "references": [
                    {
                        "label": "LSJ 20021028",
                        "text": "[LSJ 20021028]",
                        "url": "https://groups.google.com/g/rec.games.trading-cards.jyhad/c/g0GGiVIxyis/m/35WA-O9XrroJ",
                    },
                ],
                "text": "The optional maneuver cannot be used if the strike cannot be used "
                "(eg. {Hidden Lurker}). [LSJ 20021028]",
            },
            {
                "group": "Optional press",
                "references": [
                    {
                        "label": "TOM 19960521",
                        "text": "[TOM 19960521]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/poYD3n0TKGo/m/xvU5HW7lBxMJ"
                        ),
                    },
                ],
                "symbols": [
                    {
                        "symbol": "I",
                        "text": "[ANI]",
                    },
                ],
                "text": (
                    "[ANI]The optional press can only be used during the current "
                    "round. [TOM 19960521]"
                ),
            },
        ],
        "sets": {
            "Anarchs": [
                {"copies": 2, "precon": "Gangrel", "release_date": "2003-05-19"}
            ],
            "Camarilla Edition": [
                {"rarity": "Common", "release_date": "2002-08-19"},
                {"copies": 3, "precon": "Nosferatu", "release_date": "2002-08-19"},
            ],
            "First Blood": [
                {"copies": 6, "precon": "Nosferatu", "release_date": "2019-10-01"}
            ],
            "Jyhad": [{"rarity": "Common", "release_date": "1994-08-16"}],
            "Keepers of Tradition": [
                {"rarity": "Common", "release_date": "2008-11-19"}
            ],
            "Third Edition": [{"rarity": "Common", "release_date": "2006-09-04"}],
            "Vampire: The Eternal Struggle": [
                {"rarity": "Common", "release_date": "1995-09-15"}
            ],
        },
        "scans": {
            "Anarchs": ("https://static.krcg.org/card/set/anarchs/aidfrombats.jpg"),
            "Camarilla Edition": (
                "https://static.krcg.org/card/set/camarilla-edition/aidfrombats.jpg"
            ),
            "First Blood": (
                "https://static.krcg.org/card/set/first-blood/aidfrombats.jpg"
            ),
            "Jyhad": ("https://static.krcg.org/card/set/jyhad/aidfrombats.jpg"),
            "Keepers of Tradition": (
                "https://static.krcg.org/card/set/keepers-of-tradition/aidfrombats.jpg"
            ),
            "Third Edition": (
                "https://static.krcg.org/card/set/third-edition/aidfrombats.jpg"
            ),
            "Vampire: The Eternal Struggle": (
                "https://static.krcg.org/card/set/"
                "vampire-the-eternal-struggle/aidfrombats.jpg"
            ),
        },
        "ordered_sets": [
            "Jyhad",
            "Vampire: The Eternal Struggle",
            "Camarilla Edition",
            "Anarchs",
            "Third Edition",
            "Keepers of Tradition",
            "First Blood",
        ],
        "types": ["Combat"],
        "url": "https://static.krcg.org/card/aidfrombats.jpg",
    }

    assert vtes.VTES["Theo Bell"].to_json() == {
        "_name": "Theo Bell",
        "_set": "FN:U, CE:PB",
        "artists": ["John Van Fleet"],
        "capacity": 7,
        "card_text": (
            "Camarilla: Theo may enter combat with any ready minion "
            "controlled by another Methuselah as a Ⓓ action. If you control "
            "a ready prince or justicar, blood hunts cannot be called on Theo."
        ),
        "clans": ["Brujah"],
        "disciplines": ["cel", "dom", "pre", "POT"],
        "group": "2",
        "has_advanced": True,
        "has_evolution": True,
        "id": 201362,
        "legality": "2001-06-11",
        "name": "Theo Bell (G2)",
        "name_variants": ["Theo Bell"],
        "ordered_sets": ["Final Nights", "Camarilla Edition"],
        "printed_name": "Theo Bell",
        "scans": {
            "Camarilla Edition": (
                "https://static.krcg.org/card/set/camarilla-edition/theobellg2.jpg"
            ),
            "Final Nights": (
                "https://static.krcg.org/card/set/final-nights/theobellg2.jpg"
            ),
        },
        "sets": {
            "Camarilla Edition": [
                {"copies": 1, "precon": "Brujah", "release_date": "2002-08-19"}
            ],
            "Final Nights": [{"rarity": "Uncommon", "release_date": "2001-06-11"}],
        },
        "types": ["Vampire"],
        "url": "https://static.krcg.org/card/theobellg2.jpg",
        "variants": {"G2 ADV": 201363, "G6": 201613},
    }


def test_twda():
    deck = twda.TWDA["2020bf3hf"]
    test_twda = twda._TWDA()
    test_twda[deck.id] = deck
    assert test_twda.to_json() == [
        {
            "comments": textwrap.dedent(
                """
Here is a quick report by the Winner of the event Niko Vanhatalo.

Just your average Ventrue grinder/stickmen with my own personal preferences

Finals were pretty brutal because every deck was a bleeder in some way or the
other and there was no clear winner even when it was down to 2 players.
Players from 1 to 5 were Petri with Anarch stealth bleeder, Jyrkkä with
Lasombra/Kiasyd stealth bleeder, Pauli with Ventrue grinder, me with my own
Ventrue grinder and Lasse with Legion and Legionnaire bleeder.  My biggest
concern was my predator who played pretty much the same deck with like 90% of
the crypt being the same cards, but we were able to avoid unnecesary contesting
thanks to table talk. He still contested my Lodin later in the game but was
ousted pretty fast after that before any real damage to me was done.
"""
            )[1:],
            "crypt": {
                "cards": [
                    {"count": 3, "id": 200848, "name": "Lodin (Olaf Holte)"},
                    {"count": 2, "id": 200533, "name": "Graham Gottesman"},
                    {"count": 2, "id": 201438, "name": "Victor Donaldson"},
                    {"count": 1, "id": 201026, "name": "Mustafa, The Heir"},
                    {"count": 1, "id": 200280, "name": "Claus Wegener"},
                    {"count": 1, "id": 200421, "name": "Emily Carson"},
                    {"count": 1, "id": 200691, "name": "Jephta Hester"},
                    {"count": 1, "id": 201403, "name": "Ulrike Rothbart"},
                ],
                "count": 12,
            },
            "date": "2020-09-05",
            "event": "Black Forest Base 3",
            "event_link": "http://www.vekn.net/event-calendar/event/9667",
            "id": "2020bf3hf",
            "library": {
                "cards": [
                    {
                        "cards": [
                            {"count": 1, "id": 100058, "name": "Anarch Troublemaker"},
                            {"count": 1, "id": 100545, "name": "Direct Intervention"},
                            {"count": 1, "id": 100588, "name": "Dreams of the Sphinx"},
                            {"count": 1, "id": 100824, "name": "Giant's Blood"},
                            {
                                "comments": "Neat card, but never played. "
                                "Should propably switch for "
                                "another Dreams or Wash",
                                "count": 1,
                                "id": 100842,
                                "name": "Golconda: Inner Peace",
                            },
                            {"count": 1, "id": 101225, "name": "Misdirection"},
                            {"count": 1, "id": 101350, "name": "Papillon"},
                            {"count": 2, "id": 101384, "name": "Pentex™ Subversion"},
                            {"count": 2, "id": 101388, "name": "Perfectionist"},
                            {"count": 2, "id": 102113, "name": "Vessel"},
                            {"count": 2, "id": 102121, "name": "Villein"},
                            {"count": 1, "id": 102151, "name": "Wash"},
                        ],
                        "count": 16,
                        "type": "Master",
                    },
                    {
                        "cards": [
                            {"count": 1, "id": 100573, "name": "Dominate Kine"},
                            {"count": 2, "id": 100652, "name": "Entrancement"},
                            {"count": 11, "id": 100845, "name": "Govern the Unaligned"},
                        ],
                        "count": 14,
                        "type": "Action",
                    },
                    {
                        "cards": [
                            {"count": 2, "id": 100903, "name": "Heart of Nizchetus"}
                        ],
                        "count": 2,
                        "type": "Equipment",
                    },
                    {
                        "cards": [{"count": 4, "id": 101353, "name": "Parity Shift"}],
                        "count": 4,
                        "type": "Political Action",
                    },
                    {
                        "cards": [
                            {"count": 2, "id": 100236, "name": "Bonding"},
                            {"count": 3, "id": 100401, "name": "Conditioning"},
                            {"count": 3, "id": 100492, "name": "Daring the Dawn"},
                            {"count": 4, "id": 100788, "name": "Freak Drive"},
                            {"count": 5, "id": 101712, "name": "Seduction"},
                            {"count": 2, "id": 101978, "name": "Threats"},
                        ],
                        "count": 19,
                        "type": "Action Modifier",
                    },
                    {
                        "cards": [
                            {"count": 8, "id": 100518, "name": "Deflection"},
                            {"count": 3, "id": 101321, "name": "On the Qui Vive"},
                            {
                                "count": 4,
                                "id": 101706,
                                "name": "Second Tradition: Domain",
                            },
                            {
                                "comments": (
                                    "This should be another On the Qui Vive but I was "
                                    "too lazy to find 1 from my collection"
                                ),
                                "count": 1,
                                "id": 102137,
                                "name": "Wake with Evening's Freshness",
                            },
                        ],
                        "count": 16,
                        "type": "Reaction",
                    },
                    {
                        "cards": [
                            {"count": 5, "id": 100918, "name": "Hidden Strength"},
                            {"count": 6, "id": 100973, "name": "Indomitability"},
                            {
                                "count": 2,
                                "id": 101649,
                                "name": "Rolling with the Punches",
                            },
                            {
                                "count": 4,
                                "id": 102169,
                                "name": "Weighted Walking Stick",
                            },
                        ],
                        "count": 17,
                        "type": "Combat",
                    },
                ],
                "count": 88,
            },
            "name": "My stick is better than bacon",
            "place": "Hyvinkää, Finland",
            "player": "Niko Vanhatalo",
            "players_count": 14,
            "score": "1GW5+3",
            "tournament_format": "2R+F",
        },
    ]


def test_images():
    # list of storyline/token cards that are present, but not for legal play.
    filenames = {
        "agonisingfury.jpg",
        "alanmeroni.jpg",
        "allhighthe_storyline.jpg",
        "alterself.jpg",
        "amuletoftheancients.jpg",
        "anarchcounter.jpg",
        "andrewstuart_storyline.jpg",
        "andrewstuartadv_storyline.jpg",
        "angelorossi.jpg",
        "ankhsensutekadv_storyline.jpg",
        "aurelianarchambeau.jpg",
        "babayagatheironhag_storyline.jpg",
        "balefulbumsrush.jpg",
        "bindingoath.jpg",
        "blackhandcounter.jpg",
        "brunhildeadv_storyline.jpg",
        "budacastle.jpg",
        "bulscu_storyline.jpg",
        "bunyip.jpg",
        "caern.jpg",
        "callofthenephandi.jpg",
        "capuchinthe_storyline.jpg",
        "cardbackcrypt.jpg",
        "cardbackcultist.jpg",
        "cardbackcultistcrypt.jpg",
        "cardbacklibrary.jpg",
        "cardbacknergal.jpg",
        "cardbacknergalcrypt.jpg",
        "cardbacktoken.jpg",
        "carlagrimsson.jpg",
        "cecilialyons.jpg",
        "colocation.jpg",
        "corpsecray.jpg",
        "corruptdetective.jpg",
        "corruptioncounter.jpg",
        "countermagick.jpg",
        "craigjohnston.jpg",
        "cultists44magnum.jpg",
        "cultistsaireofelation.jpg",
        "cultistsarmsdealer.jpg",
        "cultistsassaultrifle.jpg",
        "cultistsatonement.jpg",
        "cultistsawe.jpg",
        "cultistsbloodfeast.jpg",
        "cultistsbomb.jpg",
        "cultistscombatshotgun.jpg",
        "cultistscreationrites.jpg",
        "cultistsenchantkindred.jpg",
        "cultistsenhancedsenses.jpg",
        "cultistsentrancement.jpg",
        "cultistsesgrima.jpg",
        "cultistsflamethrower.jpg",
        "cultistsguardianangel.jpg",
        "cultistsmindrape.jpg",
        "cultistsprecognition.jpg",
        "cultistsprotractedinvestment.jpg",
        "cultistsrevelations.jpg",
        "cultistssurvivalist.jpg",
        "cultiststributetothemaster.jpg",
        "demoniccondemnationbetrayed.jpg",
        "demoniccondemnationdoomed.jpg",
        "demoniccondemnationlanguid.jpg",
        "demoniccondemnationmute.jpg",
        "demonicconfusionoftheeye.jpg",
        "demonicfreakdrive.jpg",
        "demonicheraldoftopheth.jpg",
        "demonicminiontap.jpg",
        "demonicpulseofthecanaille.jpg",
        "demonictrap.jpg",
        "distorttime.jpg",
        "domainauckland.jpg",
        "domainbrisbane.jpg",
        "domaincanberra.jpg",
        "domainmelbourne.jpg",
        "domainsydney.jpg",
        "domaintownsville.jpg",
        "domainwellington.jpg",
        "draconthe_storyline.jpg",
        "dualityadv_storyline.jpg",
        "edge.png",
        "edge2.png",
        "edgecard.jpg",
        "edwardgrey.jpg",
        "egyptiandagger.jpg",
        "emmadodd.jpg",
        "estobaldumas.jpg",
        "exeterchantrylondon.jpg",
        "exlibrisnecro.jpg",
        "fangjumper.jpg",
        "floatingonethe.jpg",
        "formofdemoniccorruption.jpg",
        "frateranson.jpg",
        "garmrhoundofhel.jpg",
        "gerihungrywolf.jpg",
        "gjallahornhornofheimdall.jpg",
        "glasshousemountains.jpg",
        "golgolfangsfirst.jpg",
        "greatercatatonicfear.jpg",
        "greaterfacelessnight.jpg",
        "greaterfearofthevoidbelow.jpg",
        "greaterhavenuncovered.jpg",
        "greaterrotschreck.jpg",
        "greatertelepathiccounter.jpg",
        "greatertelepathicmisdirection.jpg",
        "greaterundeadpersistence.jpg",
        "greaterwakewitheveningsfreshness.jpg",
        "gungnirodin'sspear.jpg",
        "gungnirodinsspear.jpg",
        "guntheroddeye.jpg",
        "hatimoonchaser.jpg",
        "healself.jpg",
        "helmistressoftheunderworld.jpg",
        "huginnraven.jpg",
        "imbuedrules1.jpg",
        "imbuedrules2.jpg",
        "imbuedrules3.jpg",
        "imbuedrules4.jpg",
        "imbuedrules5.jpg",
        "infernalconflagration.jpg",
        "infernalcontagion.jpg",
        "infernalecstasy.jpg",
        "infernalperfectionist.jpg",
        "infernalpsychomachia.jpg",
        "infernalregeneration.jpg",
        "infernalruinsofcharizel.jpg",
        "inferno.jpg",
        "irvingsloan.jpg",
        "jensmith.jpg",
        "johannkurtzweil.jpg",
        "jormungandrmidgardserpent.jpg",
        "josiahlamb.jpg",
        "ke.jpg",
        "kinfolkcontact.jpg",
        "kingofthebeasts.jpg",
        "kraken.jpg",
        "kristofftheblack.jpg",
        "laevateinnswordoffreya.jpg",
        "liaisonmarker.jpg",
        "locateweakness.jpg",
        "lokitrickstergod.jpg",
        "lorddom.jpg",
        "lunasarmour.jpg",
        "lunasblessing.jpg",
        "manafromheaven.jpg",
        "marcusdeallegresse.jpg",
        "masterofcorrespondence.jpg",
        "masterofentropy.jpg",
        "masterofforces.jpg",
        "masteroflife.jpg",
        "masterofmatter.jpg",
        "masterofmind.jpg",
        "masterofprime.jpg",
        "masterofspirit.jpg",
        "masteroftime.jpg",
        "melissachong.jpg",
        "mithras_storyline.jpg",
        "mjolnirthorshammer.jpg",
        "montano_storyline.jpg",
        "motherstouch.jpg",
        "motivatedbygehenna.jpg",
        "motivatedbyjyhad.jpg",
        "motivatedbyknowledge.jpg",
        "motivatedbysecrecy.jpg",
        "muninnraven.jpg",
        "natachadimitrivaradocara_storyline.jpg",
        "nathanielgalpin.jpg",
        "nefertitiadv_storyline.jpg",
        "nergalcallsthegreatbeast.jpg",
        "nergalignoresthesearingflames.jpg",
        "nergalprinceofhell.jpg",
        "nergalsblooddoll.jpg",
        "nergalsconcordance.jpg",
        "nergalsfragmentofthebookofnod.jpg",
        "nergalsgiantsblood.jpg",
        "nidhoggthehungryworm.jpg",
        "operationantigencountdown.jpg",
        "parliamenthousecanberra.jpg",
        "percival_storyline.jpg",
        "philippedemarseillesadv_storyline.jpg",
        "phrygiancap.jpg",
        "pierredecalice.jpg",
        "probethoughts.jpg",
        "prophail.jpg",
        "quintessencecounter.jpg",
        "razorclaws.jpg",
        "rebeccamitsotakai.jpg",
        "recklessabandonment.jpg",
        "redsignthe.jpg",
        "regomotus.jpg",
        "reverendadamsmillenniumcultist.jpg",
        "rogerdaly.jpg",
        "rubyring.jpg",
        "rutoradv_storyline.jpg",
        "rutorsinfernalhand.jpg",
        "saintthe.jpg",
        "scarthroatleechkiller.jpg",
        "sealofmithras.jpg",
        "seating1.jpg",
        "seating2.jpg",
        "seating3.jpg",
        "seating4.jpg",
        "seating5.jpg",
        "senseconnection.jpg",
        "sensetheinfernalsin.jpg",
        "sensewyrm.jpg",
        "shadethe.jpg",
        "skinoftheinfernaladder.jpg",
        "skollsunchaser.jpg",
        "sleipnirgreatestofsteeds.jpg",
        "sonofmoonlight.jpg",
        "sophiachevallier.jpg",
        "steppingsideways.jpg",
        "stepsideways.jpg",
        "strawintogold.jpg",
        "stuarttechnobabblejaques.jpg",
        "sutrwarriorgiant.jpg",
        "svalinnshieldofthesun.jpg",
        "swallowedbythedemonicnight.jpg",
        "teotihuacan.jpg",
        "themistoclesadv_storyline.jpg",
        "thralltotheblood.jpg",
        "tonywedd.jpg",
        "tremere_storyline.jpg",
        "underworldenforcer.jpg",
        "valkyrie_storyline.jpg",
        "virustowyrm.jpg",
        "visageofcaine.jpg",
        "vladtepesdracula_storyline.jpg",
        "walkofinfernalflame.jpg",
        "windycitycoffeecart.jpg",
        "yellowsignthe.jpg",
    }
    # legacy names kept for convenience
    filenames.add("mindrape.jpg")
    filenames.add("vozhdofsofia.jpg")
    for card in vtes.VTES:
        filename = card.url.replace("https://static.krcg.org/card/", "")
        assert os.path.isfile("static/card/" + filename)
        filenames.add(filename)
        filename = card._compute_legacy_url().replace(
            "https://static.krcg.org/card/", ""
        )
        assert os.path.isfile("static/card/" + filename)
        filenames.add(filename)
    static_filenames = set()

    for filename in os.listdir("static/card"):
        if os.path.isfile("static/card/" + filename):
            static_filenames.add(filename)
    assert filenames == static_filenames
