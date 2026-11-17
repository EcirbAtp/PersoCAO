#!/usr/bin/env bash
# Génère les vues des exigences à partir des fichiers StrictDoc de reqs/ :
#   build/html/            site HTML navigable (documents, traçabilité)
#   build/PersoCAO_exigences.xlsx   tableur de synthèse
# Prérequis : pip install -r requirements-docs.txt
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf build
strictdoc export . --formats html --output-dir build
python3 tools/synthese.py reqs build/PersoCAO_exigences.xlsx
