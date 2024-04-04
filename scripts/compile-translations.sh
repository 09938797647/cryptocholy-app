#!/bin/bash

LANGUAGES=("en" "ru" "be" "uk" "fa" "uz" "pl")

echo "Compiling translations for all languages..."

for lang in "${LANGUAGES[@]}"; do
    mkdir -p translations/$lang/LC_MESSAGES
    msgfmt -o "translations/$lang/LC_MESSAGES/messages.mo" "translations/$lang/messages.po"
done

echo "Translations compiled successfully."
