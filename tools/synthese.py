"""Construit le tableur de synthèse à partir des fichiers StrictDoc (.sdoc).

Usage : python3 tools/synthese.py <dossier des .sdoc> <fichier de sortie .xlsx>

Feuilles produites :
- Synthèse : nombre d'éléments par nature, priorité et statut, et nombre
  d'éléments sans élément fils (non encore couverts par le niveau inférieur).
- Exigences : toutes les lignes, avec filtres et colonne « Nb fils ».
"""

import sys
from collections import Counter
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

HEAD = PatternFill("solid", fgColor="1F3A5F")
HFONT = Font(bold=True, color="FFFFFF")
ALERT = PatternFill("solid", fgColor="FCE4D6")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
PRIORITES = ["Indispensable", "Important", "Souhaitable", ""]
STATUTS = ["Brouillon", "Validé", "Rejeté", "Reporté"]
# Les cas d'usage n'ont pas de priorité ni de fils attendus dans la synthèse.
SANS_FILS_ATTENDUS = {"Test"}


def lire(dossier: Path) -> list[dict]:
    """Lit les blocs [REQUIREMENT] des fichiers .sdoc (champs simples et >>> multilignes)."""
    lignes = []
    for fichier in sorted(dossier.glob("*.sdoc")):
        courant, cle_multi, tampon = None, None, []
        for brut in fichier.read_text(encoding="utf-8").splitlines():
            if cle_multi:
                if brut == "<<<":
                    courant[cle_multi] = "\n".join(tampon).strip()
                    cle_multi, tampon = None, []
                else:
                    tampon.append(brut)
                continue
            if brut == "[REQUIREMENT]":
                courant = {"document": fichier.stem, "parents": []}
                lignes.append(courant)
            elif brut.startswith("[") or not brut.strip():
                courant = None if brut.startswith("[") else courant
            elif courant is not None:
                if brut.startswith("  VALUE: "):
                    courant["parents"].append(brut.split(": ", 1)[1].strip())
                elif ": " in brut or brut.endswith(":"):
                    cle, _, valeur = brut.partition(":")
                    valeur = valeur.strip()
                    if valeur == ">>>":
                        cle_multi = cle.strip().lower()
                    elif not brut.startswith("-"):
                        courant[cle.strip().lower()] = valeur
    for l in lignes:
        l["parents"] = ", ".join(l["parents"])
    return lignes


def entete(ws, valeurs, largeurs):
    ws.append(valeurs)
    for cellule, largeur in zip(ws[ws.max_row], largeurs):
        cellule.fill, cellule.font, cellule.border = HEAD, HFONT, BORDER
        ws.column_dimensions[cellule.column_letter].width = largeur


def main(dossier: str, sortie: str) -> None:
    lignes = lire(Path(dossier))
    fils = Counter(p.strip() for l in lignes for p in l.get("parents", "").split(",") if p.strip())

    wb = Workbook()
    syn = wb.active
    syn.title = "Synthèse"
    entete(syn, ["Nature", "Priorité"] + STATUTS + ["Total", "Sans fils"], [16, 16, 12, 12, 12, 12, 10, 12])
    groupes = Counter((l["nature"], l.get("priorite", "")) for l in lignes)
    for nature, prio in sorted(groupes, key=lambda g: (g[0], PRIORITES.index(g[1]) if g[1] in PRIORITES else 9)):
        du_groupe = [l for l in lignes if l["nature"] == nature and l.get("priorite", "") == prio]
        sans_fils = sum(1 for l in du_groupe if not fils[l["uid"]]) if nature not in SANS_FILS_ATTENDUS else 0
        syn.append([nature, prio or "–"] + [sum(l["statut"] == s for l in du_groupe) for s in STATUTS]
                   + [len(du_groupe), sans_fils])
    syn.append(["Total", ""] + [sum(l["statut"] == s for l in lignes) for s in STATUTS] + [len(lignes), ""])
    for rang in syn.iter_rows(min_row=2):
        for c in rang:
            c.border = BORDER
    syn.freeze_panes = "A2"

    ex = wb.create_sheet("Exigences")
    colonnes = [("uid", "ID", 12), ("nature", "Nature", 13), ("title", "Titre", 30), ("statement", "Énoncé", 80),
                ("priorite", "Priorité", 14), ("cible", "Cible", 20), ("statut", "Statut", 11),
                ("parents", "Parent(s)", 18), (None, "Nb fils", 9), ("verification", "Vérification", 14),
                ("comment", "Commentaire", 40), ("document", "Document", 14)]
    entete(ex, [c[1] for c in colonnes], [c[2] for c in colonnes])
    for l in lignes:
        ex.append([fils[l["uid"]] if cle is None else l.get(cle, "") for cle, _, _ in colonnes])
        for c in ex[ex.max_row]:
            c.alignment, c.border = Alignment(wrap_text=True, vertical="top"), BORDER
        if not fils[l["uid"]] and l["nature"] not in SANS_FILS_ATTENDUS:
            ex.cell(ex.max_row, 9).fill = ALERT
    ex.freeze_panes = "B2"
    ex.auto_filter.ref = f"A1:L{ex.max_row}"
    wb.save(sortie)
    print(f"{len(lignes)} éléments écrits dans {sortie}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
