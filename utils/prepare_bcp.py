"""A convenience function to rename BCP images
"""

import os
import re

from krcg.parser import _CLAN


def prepare_bcp(path):
    for dirpath, _dirnames, filenames in os.walk(path):
        for name in filenames:
            clan_prefix = re.match(r"({})_".format(_CLAN), name.lower())
            if clan_prefix:
                os.rename(
                    os.path.join(dirpath, name),
                    os.path.join(dirpath, name[clan_prefix.end(0) :]),
                )
