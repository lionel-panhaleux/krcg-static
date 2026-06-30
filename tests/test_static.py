import os.path
import re

import msgspec

from krcg import models


def test_card(cards):
    """The v5 card serialization krcg-static writes to data/v5/vtes.json."""
    aid = cards["Aid from Bats"]
    j = msgspec.to_builtins(aid)
    assert j["id"] == 100029
    assert j["kind"] == models.Card.Kind.LIBRARY
    assert j["printed_name"] == "Aid from Bats"
    assert aid.url == "https://static.krcg.org/card/aidfrombats.jpg"
    # translations are carried over (data/v5 must ship i18n)
    assert {lang.value for lang in aid.i18n} == {"es", "fr"}
    assert aid.i18n[models.Lang.FR].name == "Aide des chauves-souris"

    theo = cards["Theo Bell"]
    j = msgspec.to_builtins(theo)
    assert j["id"] == 201362
    assert j["kind"] == models.Card.Kind.CRYPT
    assert j["printed_name"] == "Theo Bell"
    assert j["clan"] == "Brujah"
    assert j["capacity"] == 7
    assert j["disciplines"] == ["cel", "dom", "pre", "POT"]
    assert theo.url == "https://static.krcg.org/card/theobellg2.jpg"


def test_twda(TWDA):
    """The v5 deck model krcg-static writes to data/v5/twda.json."""
    deck = TWDA["2020bf3hf"]
    assert deck.name == "My stick is better than bacon"
    assert deck.player == "Niko Vanhatalo"
    assert deck.event.name == "Black Forest Base 3"
    assert deck.event.place == "Hyvinkää, Finland"
    assert deck.event.date.isoformat() == "2020-09-05"
    assert deck.event.players_count == 14
    assert str(deck.score) == "1GW5+3!"
    crypt = sum(c.count for c in deck.cards if c.kind == models.Card.Kind.CRYPT)
    library = sum(c.count for c in deck.cards if c.kind == models.Card.Kind.LIBRARY)
    assert crypt == 12
    assert library == 88


def test_images(cards):
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

    def card_file(filename):
        """Assert an image exists for a card, return its real-file target name."""
        path = "static/card/" + filename
        assert os.path.isfile(path), f"missing {filename}"
        filenames.add(filename)
        # group-less names are symlinks onto the real grouped file: keep both
        if os.path.islink(path) and "/" not in os.readlink(path):
            filenames.add(os.readlink(path))

    for card in cards.cards():
        filename = card.url.replace("https://static.krcg.org/card/", "")
        card_file(filename)
        # crypt cards keep a group-less symlink for convenience ("...g3.jpg" ->
        # "....jpg", "...g3adv.jpg" -> "...adv.jpg")
        legacy = re.sub(r"g\d(adv)?\.jpg$", r"\1.jpg", filename)
        if legacy != filename:
            card_file(legacy)
    # add .webp counterparts for all .jpg files (except storyline/token symlinks)
    filenames |= {
        f[:-4] + ".webp"
        for f in filenames
        if f.endswith(".jpg")
        and not (
            os.path.islink("static/card/" + f)
            and "/" in os.readlink("static/card/" + f)
        )
    }
    # the real card file is the name as printed ("theankoug5.jpg"); legacy
    # back-form names ("ankoutheg5.jpg") and group-less aliases are symlinks
    # kept for retrocompatibility: accept any local symlink (.jpg or .webp)
    # that resolves onto an already-expected card file.
    for filename in os.listdir("static/card"):
        path = "static/card/" + filename
        if os.path.islink(path) and "/" not in os.readlink(path):
            target = os.path.basename(os.path.realpath(path))
            if target in filenames:
                filenames.add(filename)

    static_filenames = set()
    for filename in os.listdir("static/card"):
        if os.path.isfile("static/card/" + filename):
            static_filenames.add(filename)
    assert filenames - static_filenames == set(), "missing files"
    assert static_filenames - filenames == set(), "spurious files"
