export LOCAL_CARDS := "1"
static_server := env_var_or_default("STATIC_SERVER", "lpanhaleux@krcg.org:projects/static.krcg.org/dist")

quality:
    uv run ruff format --check .
    uv run ruff check

test: quality
    uv run pytest -vv

static:
    uv run krcg-static build
    rsync -rlptq --delete-after -e ssh build/ {{static_server}}

minimal:
    uv run krcg-static build --minimal
    rsync -rlptq --delete-after -e ssh build/ {{static_server}}

update:
    uv sync --upgrade

clean:
    rm -rf build
    rm -rf .pytest_cache
    rm -rf result

# Process incoming card images into result/, then copy to static/card/
cards dir="incoming": (_process-cards "false" dir)

# Process incoming BCP card images (with large border removal)
cards-bcp dir="incoming": (_process-cards "true" dir)

_process-cards bcp dir:
    #!/usr/bin/env zsh
    set -euo pipefail
    if [[ ! -d "{{dir}}" ]]; then
        echo "Error: {{dir}}/ directory not found. Place card images in {{dir}}/"
        exit 1
    fi
    mkdir -p result
    # Process and rename incoming images
    for f in "{{dir}}"/*(.); do
        name=${f#"{{dir}}"/}
        name=${name%.*}
        name=${name% - *}
        group=${name##*\[}
        group=${group%%\]*}
        if [[ ${group} == ${name} ]]; then
            group=
        fi
        name=${name% \[*}
        name=$(echo $name | iconv -sc -f utf-8 -t ascii//translit | tr '[:upper:]' '[:lower:]' | tr -d '[:punct:]' | tr -d '[:space:]')
        group=$(echo $group | iconv -f utf-8 -t ascii//translit | tr -d '[:punct:]' | tr -d '[:space:]')
        if [[ -n $group ]]; then
            name=${name}g${group}
        fi
        out=result/${name}.jpg
        if [[ "{{bcp}}" == "true" ]]; then
            magick $f -shave 18 -resize x500 -background black -gravity center -extent 358x500 $out
        else
            magick $f -resize x500 -background black -gravity center -extent 358x500 $out
        fi
        echo "  $f -> $out"
    done
    # Generate webp versions
    for f in result/*.jpg(.); do
        magick $f ${f%.jpg}.webp
    done
    echo "Generated webp versions"
    # Create symlinks for crypt cards (with group number)
    cd result
    for f in ./*.jpg(.); do
        name=${f#./}
        short=${name%g[123456789].jpg}
        if [[ ${short} != ${name} ]]; then
            ln -fs ${name} ${short}.jpg
            ln -fs ${name%.jpg}.webp ${short}.webp
            echo "  ${short}.jpg -> ${name}"
        fi
    done
    cd ..
    # Copy to static/card/ preserving symlinks
    cp -av result/* static/card/
    echo "Done! Cards copied to static/card/"
