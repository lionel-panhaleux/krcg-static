# krcg-static

KRCG static V:tES files generation

## Update KRCG static

-   Copy the translated card images in the `i18n_cards` folder, under their respective
    ISO 639-1 language code folder (ie. `i18n_cards/fr`)

-   Launch the `make static` command

That's it.

The command build the static site into the `build` folder,
then uses `rsync` over `ssh` to push it to the `static.krcg.org` server.
Note you need ssh access to the `krcg.org` server to deploy.
