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

-   Copy the card images in the `static/cards` folder, under their respective folder:
    + Right there for the most recent "main" images
    + In the relevant subfolder in `static/cards/set`
    + In the right ISO 639-1 language subfolder for translated cards (ie. `i18n_cards/fr`)

-   Go to Github in the `Actions` tab and run the `Deployment` action.

**Note only authorized admins on the krcg-static repository can run this action**
If you're a contributor, signal yourself to the repository administrators so they
can review and authorize your deployment.

## Fontforge & Imagemagick foo

Use [Homebrew](https://brew.sh) on OSX to install a few graphical tools:

```
brew install imagemagick inkscape potrace
```

[Fontforge](https://fontforge.org) can be used to build and extract fonts.
Use `File > Execute Script` to execute the following `FF` script:

```txt
SelectWorthOutputting(); foreach Export("svg"); endloop;
```

Convert SVG to PNG with a transparent background:

```shell
for f in svg/**/*(.); do g=${f#svg/}; g=png/${g%.svg}.png; convert -background none $f $g; done
```

Convert transparent PNG to white bordered PNG:

```shell
for f in png/icon/*(.); \
do g=png_wb/${f#png/}; \
convert $f \( \
    +clone -alpha extract -morphology edgeout octagon:15 -bordercolor black \
    -border 100 -morphology close Octagon:50 -shave 100 \
    -level 50% -transparent black \) \
-compose DstOver -composite $g \
; done
```

Convert transparent square PNG to white bordered PNG:

```shell
for f in png/icon/*(.); \
do g=png_wb/${f#png/}; \
convert -background none -size 896x896 xc:white \
    \( $f -trim +repage -resize 768x768 \) \
    -geometry +64+64 -composite $g \
; done
```

Note as seen on real cards, inferior disciplines are roughly 15% bigger squares than superior disciplines.
This is because when one rotates the square by 45° the width is √2 = 41% larger,
so compensation is required for visual consistency.
If the base square (inferior) is `896x896`, the superior square is `896/1.15` = `780x780`.
And if the inner inferior icon is `768` in width (for a `64` white border),
then the superior icon width needs to be `768/1.15 * √2` = `944x944`.

Convert transparent losange (sup) PNG to white bordered PNG:

```shell
for f in png/icon/*(.); \
do g=png_wb/${f#png/}; \
convert -background none -size 780x780 xc:white -rotate 45 \
    \( $f -trim +repage -resize 944x944 \) \
    -geometry +82+82 -composite $g \
; done
```

Add transparent border (`128px`):

```shell
for f in png_wb/icon/*(.); do \
convert -background none $f -bordercolor none -border 128x128 $f \
; done
```

Generate a multisize `.ico` file:

```shell
convert -background none vtes.svg \
\( -clone 0 -resize 16x16 \) \
\( -clone 0 -resize 32x32 \) \
\( -clone 0 -resize 64x64 \) \
\( -clone 0 -resize 128x128 \) \
\( -clone 0 -resize 256x256 \) \
-delete 0 -alpha on -compress Zip vtes.ico     
```

Convert VEKN card images to our format:

```shell
for f in incoming/*(.); do \
name=${f#incoming/}; \
name=${name%.*}; \
name=${name% - *}; \
name=${name% \[*}; \
name=`echo $name | iconv -f utf-8 -t ascii//translit | tr '[:upper:]' '[:lower:]' | tr -d '[:punct:]' | tr -d '[:space:]'`; \
name=result/${name}.jpg; \
convert $f -bordercolor black -border 0x1 $name; \
done
```

Depending on how they generate the files, those can come up with large block borders (400x544), in this case, do this:

```shell
for f in incoming/*(.); do \
name=${f#incoming/}; \
name=${name%.*}; \
name=${name% - *}; \
group=${name##*\[}; \
group=${group%%\]*}; \
if [[ ${group} == ${name} ]]; then \
    group= ; \
fi; \
name=${name% \[*}; \
name=`echo $name | iconv -f utf-8 -t ascii//translit | tr '[:upper:]' '[:lower:]' | tr -d '[:punct:]' | tr -d '[:space:]'`; \
if [[ ! -z $group ]]; then \
    name=${name}g${group}; \
fi; \
name=result/${name}.jpg; \
convert $f -shave 18 -resize x500 $name; \
done
```

Then, to create the symbolic links for the crypt cards, you can:

```shell
cd result
for f in ./*(.); do \
name=${f#./}; \
short=${name%g[123456789].jpg}; \
if [[ ${short} != ${name} ]]; then \
    ln -fs ${name} ${short}.jpg; \
fi; \
done
```

Then copy everything and preserve the links to the static directory:

```shell
cp -av ./* ~/dev/krcg-static/static/card/
```

Make sure your symbolic links are **relative to the `.` folder**  ot they won't work online.
