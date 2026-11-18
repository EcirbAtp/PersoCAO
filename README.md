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
| `strictdoc_config.py` | Configuration StrictDoc (documents inclus, écrans, traçabilité vers le code) |

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
pip install -r requirements-docs.txt
./tools/generer_vues.sh
```

Le script produit dans `build/` (non versionné) :

- `build/html/index.html` : les exigences navigables, avec les liens de traçabilité, la matrice de traçabilité (`traceability_matrix.html`), les statistiques (`project_statistics.html`) et la couverture du code (`source_coverage.html`) ;
- `build/PersoCAO_exigences.xlsx` : le tableur de synthèse (compte par nature, priorité et statut ; éléments sans fils signalés).

La même génération tourne sur GitHub à chaque pull request qui touche aux exigences (workflow `Exigences`) : elle échoue si un `.sdoc` est invalide ou si un lien vise un UID inexistant, et les vues sont téléchargeables dans l'onglet *Actions*, artefact `exigences`.

## Éditer les exigences

- À la main : modifier les fichiers `reqs/*.sdoc`.
- Avec l'interface web de StrictDoc : `strictdoc server .` à la racine du dépôt, puis ouvrir http://localhost:5111. Les modifications sont écrites directement dans les `.sdoc`.

## Tracer les exigences vers le code et les tests

La traçabilité vers le code est activée dans `strictdoc_config.py` pour les dossiers `src/`, `modules/` et `tests/` (créés à l'implémentation). Un commentaire dans un fichier source ou de test le relie à une exigence :

```cpp
/**
 * @relation(BES-F-03, scope=function)
 */
void test_annuler_retablir() { /* ... */ }
```

Après génération, chaque exigence affiche les fichiers qui la réalisent ou la vérifient, et `source_coverage.html` montre la part du code couverte.
