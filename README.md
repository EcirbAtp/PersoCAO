# PersoCAO

Logiciel personnel de CAO 3D de mécanique générale, avec des modules métier installables (aéronautique, automobile, marine, spatial). Développé en C++20, Qt 6 et Open CASCADE, pour Windows et Linux.

Le projet suit un cycle en V : aucune implémentation avant la fin du V descendant (besoin, spécifications, faisabilité, conception).

## Organisation du dépôt

| Dossier | Contenu |
| --- | --- |
| `docs/01_besoin/` | Expression du besoin |
| `docs/images/` | Schémas utilisés par les documents |
| `reqs/` | Exigences au format [StrictDoc](https://github.com/strictdoc-project/strictdoc), une source par niveau du V |
| `tools/` | Scripts de génération des vues (site HTML, tableur de synthèse) |

## Avancement du V descendant

| Étape | Document | Exigences | État |
| --- | --- | --- | --- |
| 1. Expression du besoin | `docs/01_besoin/expression_du_besoin.md` | `reqs/01_besoin.sdoc` (CU, BES-F, BES-T) | Brouillon v0.3 |
| 2. Spécification fonctionnelle | à venir | EXF, EXT | À faire |
| 3. Spécification IHM et rendu | à venir | EXI | À faire |
| 4. Faisabilité et conception générale | à venir | CON | À faire |

## Gestion des exigences

- Chaque exigence a un identifiant stable (`CU-xx`, `BES-F-xx`, `BES-T-xx`, puis `EXF-xxx`, `EXT-xxx`, `EXI-xxx`, `CON-xxx`, `TST-xxx`) et un lien vers son ou ses parents.
- Les fichiers `.sdoc` de `reqs/` font foi. Les tableaux des documents Markdown en sont un reflet ; en cas d'écart, le `.sdoc` l'emporte.
- Une exigence n'est jamais supprimée : elle passe au statut `Rejeté` ou `Reporté`.
- Les documents sont relus et commentés en dehors du dépôt, puis chaque version validée est enregistrée ici par une pull request.

## Générer les vues

```sh
pip install strictdoc openpyxl
./tools/generer_vues.sh
```

Le script produit dans `build/` (non versionné) :

- `build/html/index.html` : les exigences navigables, avec les liens de traçabilité ;
- `build/PersoCAO_exigences.xlsx` : le tableur de synthèse (compte par nature, priorité et statut ; éléments sans fils signalés).
