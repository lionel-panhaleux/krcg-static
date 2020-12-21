# KRCG Static

[![Validation](https://github.com/lionel-panhaleux/krcg-static/workflows/Validation/badge.svg)](https://github.com/lionel-panhaleux/krcg-static/actions)
[![Python version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

KRCG static V:tES files generation, using
the VEKN [official card texts](http://www.vekn.net/card-lists),
the [Tournament Winning Deck Archive (TWDA)](http://www.vekn.fr/decks/twd.htm) and
[KRCG](https://github.com/lionel-panhaleux/krcg) rulings list.

This software is used to generate the static website [static.krcg.org](https://static.krcg.org).

Portions of the materials are the copyrights and trademarks of Paradox Interactive AB,
and are used with permission. All rights reserved.
For more information please visit [white-wolf.com](http://www.white-wolf.com).

![Dark Pack](dark-pack.png)

## Contribute

**Contributions are welcome !**

This is an offspring of the [KRCG](https://github.com/lionel-panhaleux/krcg)
python package, so please refer to that repository for issues, discussions
and contributions guidelines.

## Update the KRCG static website

-   Copy the translated card images in the `i18n_cards` folder, under their respective
    ISO 639-1 language code folder (ie. `i18n_cards/fr`)

-   Launch the `make static` command

The command build the static site into the `build` folder with the `krcg-static build`
command, then uses `rsync` over `ssh` to push it to the `static.krcg.org` server.
Note you need ssh access to the `krcg.org` server to deploy.
