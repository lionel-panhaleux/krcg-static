"""A convenience function to fix tournament archive files
"""
import os
import re


def format_tournament(path):
    for p in os.listdir(path):
        f = open(os.path.join(path, p))
        content = f.read()
        head = content.split("\n", 2)
        print(head[0])
        score = re.match(
            r"[\w\d\s:]*?(?P<number>\d+)\.\s*(?P<gw>\d+)GW\s*"
            r"(?P<vp>\d+)(,|.)?(?P<half>\d)?\s*V?P?",
            head[0],
        )
        print(score.groups())
        outdir, taildir = os.path.dirname(path).rsplit("/", 1)
        outdir = os.path.join(outdir, taildir + "_Out")
        os.makedirs(outdir, exist_ok=True)
        name = f"{taildir}_{score['number']}"
        score_string = score["gw"] + "GW" + score["vp"]
        if score["half"]:
            score_string += ".5"
        of = open(os.path.join(outdir, name + ".txt"), "w")
        of.write(f"Deck Name: {name}\n")
        of.write(head[1] + "\n")
        of.write(f"Description: {score_string}\n")
        of.write(head[2])
        of.close()
