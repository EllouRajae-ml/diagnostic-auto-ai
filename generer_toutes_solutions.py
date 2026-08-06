#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_toutes_solutions.py
----------------------------
Prend TA liste de codes déjà tapée dans ton programme (peu importe le
format : dict, liste de tuples, ou CSV) et génère, pour CHACUN sans
exception, une solution détaillée via diagnostic_dtc.generer_solution().

Aucun appel IA. Résultat = un dictionnaire {code: solution} complet,
que tu peux ensuite utiliser dans ton appli (afficher, sauvegarder en
JSON, servir via une API, etc.)
"""

import sys
from diagnostic_dtc import generer_solution, charger_codes


# ---------------------------------------------------------------------------
# ÉTAPE 1 : CHARGEMENT AUTOMATIQUE DE TON FICHIER codes_defaut.csv
# ---------------------------------------------------------------------------
# Par défaut on cherche "codes_defaut.csv" dans le dossier courant.
# Tu peux aussi préciser un autre nom :
#     python generer_toutes_solutions.py mon_autre_fichier.csv

nom_fichier_csv = sys.argv[1] if len(sys.argv) > 1 else "codes_defaut.csv"
mes_codes = charger_codes(nom_fichier_csv)


# ---------------------------------------------------------------------------
# ÉTAPE 2 : GÉNÉRATION — TOURNE SUR TOUS LES CODES, SANS EXCEPTION
# ---------------------------------------------------------------------------

def generer_toutes_les_solutions(codes_dict: dict) -> dict:
    """
    Retourne {code: solution_texte} pour CHAQUE entrée de codes_dict.
    Ne saute jamais un code : le fallback 'generique' dans
    diagnostic_dtc.py garantit une solution même pour les codes rares
    ou mal documentés.
    """
    solutions = {}
    total = len(codes_dict)
    for i, (code, description) in enumerate(codes_dict.items(), start=1):
        solutions[code] = generer_solution(code, description)
        if i % 200 == 0 or i == total:
            print(f"  ... {i}/{total} codes traités")
    return solutions


if __name__ == "__main__":
    if not mes_codes:
        print(f"⚠ Aucun code chargé depuis '{nom_fichier_csv}'.")
        print("Vérifie que le fichier existe dans ce dossier et a bien les colonnes 'code,description'.")
    else:
        print(f"Génération des solutions pour {len(mes_codes)} codes...")
        toutes_les_solutions = generer_toutes_les_solutions(mes_codes)

        # Sauvegarde en JSON pour réutilisation dans ton appli
        import json
        with open("solutions_completes.json", "w", encoding="utf-8") as f:
            json.dump(toutes_les_solutions, f, ensure_ascii=False, indent=2)

        print(f"Terminé. {len(toutes_les_solutions)} solutions générées "
              f"et sauvegardées dans solutions_completes.json")

        # Vérification qu'aucun code n'a été oublié
        codes_manquants = set(mes_codes.keys()) - set(toutes_les_solutions.keys())
        if codes_manquants:
            print(f"⚠ ATTENTION, codes sans solution : {codes_manquants}")
        else:
            print("✅ Confirmé : 100% des codes ont une solution, aucune exception.")