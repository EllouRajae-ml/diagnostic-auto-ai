#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagnostic_dtc.py
------------------
Générateur de solutions de diagnostic OBD-II à partir d'une base CSV
(code, description). AUCUN appel à une IA : tout est codé en dur
(règles + bibliothèque de procédures) afin que chaque code produise
une solution réellement différente des autres.

Utilisation :
    python diagnostic_dtc.py                  -> mode interactif
    python diagnostic_dtc.py P0301             -> un seul code
    python diagnostic_dtc.py P0301 P0130 U0100 -> plusieurs codes

Le fichier CSV attendu (par défaut "codes_dtc.csv" dans le même dossier)
doit avoir l'entête : code,description
"""

import csv
import os
import re
import sys

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codes_dtc.csv")


# ---------------------------------------------------------------------------
# 1) CHARGEMENT DE LA BASE DE CODES
# ---------------------------------------------------------------------------

def charger_codes(csv_path: str) -> dict:
    """Charge le CSV code -> description dans un dictionnaire."""
    codes = {}
    if not os.path.exists(csv_path):
        print(f"[ATTENTION] Fichier introuvable : {csv_path}")
        print("Place ton fichier CSV (colonnes 'code,description') à côté de ce script,")
        print("ou passe le chemin avec --csv chemin/vers/fichier.csv")
        return codes

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row["code"].strip().upper()
            desc = row["description"].strip()
            codes[code] = desc
    return codes


# ---------------------------------------------------------------------------
# 2) DÉTECTION DE LA CATÉGORIE (famille du code)
# ---------------------------------------------------------------------------

def detecter_categorie(code: str) -> str:
    """
    Retourne une catégorie lisible à partir du préfixe et de la plage
    numérique du code DTC (norme SAE J2012 / ISO 15031-6).
    """
    code = code.upper()
    prefixe = code[0]
    try:
        numero = int(code[1:])
    except (ValueError, IndexError):
        numero = -1

    if prefixe == "P":
        if 0 <= numero <= 999:
            if 0 <= numero <= 99:
                return "Carburant / Air (dosage, débitmètre, pression)"
            if 100 <= numero <= 199:
                return "Mesure air/carburant (capteurs admission, MAP, IAT)"
            if 200 <= numero <= 299:
                return "Injecteurs de carburant"
            if 300 <= numero <= 399:
                return "Ratés d'allumage / Allumage"
            if 400 <= numero <= 499:
                return "Dépollution (EGR, catalyseur, purge canister)"
            if 500 <= numero <= 599:
                return "Ralenti / Régulateur de vitesse / Démarrage"
            if 600 <= numero <= 699:
                return "Calculateur moteur (module de commande)"
            if 700 <= numero <= 999:
                return "Transmission automatique / Boîte de vitesses"
        return "Moteur / Groupe motopropulseur (générique)"

    if prefixe == "C":
        return "Châssis (ABS, freinage, direction, suspension)"

    if prefixe == "U":
        return "Réseau de communication (bus CAN / modules)"

    if prefixe == "B":
        return "Carrosserie / Habitacle (confort, sécurité, électricité)"

    return "Catégorie inconnue"


# ---------------------------------------------------------------------------
# 3) DÉTECTION DU TYPE DE DÉFAUT (à partir de mots-clés dans la description)
# ---------------------------------------------------------------------------

REGLES_TYPE_DEFAUT = [
    # (motif regex sur la description en minuscules, type_defaut)
    (r"communication perdue|bus de communication|autobus", "communication"),
    (r"circuit ouvert|circuit .* ouvert", "circuit_ouvert"),
    (r"court-circuit.*(batterie|vbatt)|short to battery|circuit trop haut|signal haut|valeur d.entrée trop haute",
     "circuit_haut"),
    (r"court-circuit.*(terre|masse|ground)|short to ground|circuit trop bas|signal bas|valeur d.entrée trop basse",
     "circuit_bas"),
    (r"réponse lente", "reponse_lente"),
    (r"pas d.activité détectée|aucun signal|no signal", "signal_absent"),
    (r"résistance du chauffage|commande de chauffage", "chauffage"),
    (r"plage de mesure|performance|rendement|corrélation", "performance"),
    (r"erreur de somme|checksum|erreur interne|défaut de fonctionnement d.ecu|données inadmissibles",
     "calculateur_interne"),
    (r"fuite", "fuite"),
    (r"surchauffe|température .* trop haute|température .* trop basse", "temperature"),
]


def detecter_type_defaut(description: str) -> str:
    desc = description.lower()
    for motif, type_defaut in REGLES_TYPE_DEFAUT:
        if re.search(motif, desc):
            return type_defaut
    return "generique"


# ---------------------------------------------------------------------------
# 4) DÉTECTION DU COMPOSANT (nom lisible à réinjecter dans le texte)
# ---------------------------------------------------------------------------

COMPOSANTS_CONNUS = [
    "sonde lambda", "capteur de vilebrequin", "capteur d'arbre à cames",
    "capteur de vitesse", "injecteur", "bobine d'allumage", "électrovanne",
    "débitmètre d'air", "capteur de pression", "sonde de température",
    "catalyseur", "turbocompresseur", "egr", "pompe à carburant",
    "calculateur", "module de commande", "capteur de position",
    "contacteur", "moteur de", "relais", "capteur d'angle de direction",
    "capteur de vitesse de roue", "airbag", "colonne de direction",
    "miroir", "siège", "fenêtre", "serrure", "essuie-glace",
]


def detecter_composant(description: str) -> str:
    desc = description.lower()
    for comp in COMPOSANTS_CONNUS:
        if comp in desc:
            return comp
    # à défaut, on prend les premiers mots significatifs de la description
    mots = re.split(r"[,\-–]", description)
    return mots[0].strip().lower() if mots else "composant non identifié"


# ---------------------------------------------------------------------------
# 5) BIBLIOTHÈQUE DE PROCÉDURES (codée en dur, une par type de défaut)
# ---------------------------------------------------------------------------

PROCEDURES = {
    "communication": [
        "Vérifier la présence de tension batterie et de masse sur le module concerné.",
        "Contrôler la continuité et l'isolement des lignes de bus (CAN H / CAN L) : pas de coupure, pas de court-circuit entre elles.",
        "Vérifier les connecteurs du module signalé pour oxydation, broches déformées ou déconnectées.",
        "Contrôler la résistance de terminaison du bus (généralement environ 60 ohms mesurés aux deux extrémités en parallèle, à vérifier selon schéma constructeur).",
        "Si plusieurs modules sont en défaut de communication simultanément, suspecter une coupure d'alimentation commune ou un module qui pollue le bus (le déconnecter un par un pour isoler).",
    ],
    "circuit_ouvert": [
        "Contrôler la continuité complète du câblage entre le calculateur et le composant (rupture de fil, connecteur débranché, cosse arrachée).",
        "Vérifier la propreté et le bon verrouillage des connecteurs aux deux extrémités du circuit.",
        "Mesurer la résistance du composant lui-même (bobinage, résistance interne) et la comparer à la valeur constructeur.",
        "Si le circuit est bon mais le défaut persiste, contrôler le fusible et le relais associés à ce circuit.",
    ],
    "circuit_haut": [
        "Rechercher un court-circuit du fil de signal vers le +12V (frottement de câblage, isolant endommagé).",
        "Vérifier que le composant n'est pas alimenté en direct par erreur (mauvais branchement après une intervention récente).",
        "Contrôler la tension de référence envoyée par le calculateur (souvent 5V) : si elle est déjà anormalement haute en amont, le calculateur peut être en cause.",
        "Débrancher le composant et mesurer la tension résiduelle sur le fil signal : si elle reste haute, le court-circuit est côté câblage, pas côté composant.",
    ],
    "circuit_bas": [
        "Rechercher un court-circuit du fil de signal vers la masse (isolant endommagé, pincement de câblage).",
        "Vérifier la valeur de résistance du composant : une résistance anormalement basse indique un composant interne en court-circuit.",
        "Contrôler la propreté des masses du véhicule proches du circuit concerné.",
        "Débrancher le composant : si la tension reste basse fil débranché, le défaut est côté câblage vers le calculateur.",
    ],
    "reponse_lente": [
        "Nettoyer ou remplacer le composant si son temps de réponse ne respecte plus les spécifications (cas fréquent sur sondes lambda encrassées).",
        "Vérifier qu'il n'y a pas de fuite d'air parasite en amont (cause fréquente de réponse faussée sur les sondes de mélange).",
        "Contrôler l'état du connecteur (résistance de contact ajoute un retard électrique).",
        "Vérifier que le composant a atteint sa température de fonctionnement avant le diagnostic (certains capteurs nécessitent une mise en chauffe).",
    ],
    "signal_absent": [
        "Vérifier l'alimentation et la masse du capteur/composant à l'aide d'un multimètre, moteur en fonctionnement si applicable.",
        "Contrôler la continuité du fil de signal jusqu'au calculateur.",
        "Inspecter le composant pour dommage mécanique (denture cassée, entrefer trop grand sur capteurs inductifs).",
        "Si le signal reste absent malgré un câblage et une alimentation corrects, remplacer le capteur.",
    ],
    "chauffage": [
        "Mesurer la résistance de l'élément chauffant du composant et la comparer à la valeur constructeur.",
        "Vérifier l'alimentation du relais ou du circuit de commande de chauffage.",
        "Contrôler que le fusible dédié au circuit de chauffage n'est pas grillé.",
        "Si la résistance de l'élément chauffant est hors tolérance, remplacer le composant (l'élément chauffant n'est généralement pas réparable seul).",
    ],
    "performance": [
        "Comparer la valeur mesurée en temps réel (valise de diagnostic) à la plage attendue dans différentes conditions de fonctionnement (ralenti, charge, régime).",
        "Vérifier qu'aucun autre code lié ne pointe vers une cause commune (ex : fuite d'air, capteur en amont défectueux faussant tout le système).",
        "Contrôler l'état physique du composant (encrassement, corrosion, jeu mécanique).",
        "Réaliser un nouvel apprentissage / une réinitialisation adaptative si le composant ou le calculateur vient d'être remplacé.",
    ],
    "calculateur_interne": [
        "Effectuer une remise à jour ou une reprogrammation du calculateur si une version logicielle corrective existe chez le constructeur.",
        "Vérifier la stabilité de l'alimentation électrique du calculateur (chute de tension batterie, masse calculateur oxydée).",
        "Si le défaut persiste après effacement et un cycle de conduite complet, envisager le remplacement du calculateur.",
        "Avant tout remplacement de calculateur, sauvegarder / noter la configuration (VIN, options) pour la reprogrammation du nouveau boîtier.",
    ],
    "fuite": [
        "Réaliser un test de fumée (fumigène) sur le circuit concerné pour localiser précisément le point de fuite.",
        "Contrôler l'état des durites, colliers de serrage et joints du système concerné.",
        "Vérifier que le bouchon ou le clapet associé (ex : bouchon de réservoir pour le circuit de purge canister) ferme correctement.",
        "Réparer ou remplacer l'élément fuyard identifié, puis effacer la mémoire et revalider par un nouveau cycle de diagnostic.",
    ],
    "temperature": [
        "Vérifier le niveau et l'état du liquide de refroidissement ou du fluide concerné.",
        "Contrôler le bon fonctionnement du ou des motoventilateurs de refroidissement.",
        "Vérifier l'absence d'obstruction (radiateur encrassé, grille d'air bouchée).",
        "Contrôler le thermostat et la sonde de température elle-même si la valeur affichée semble incohérente.",
    ],
    "generique": [
        "Identifier précisément le composant, le capteur, l'injecteur, la bobine, le relais ou la soupape concernés par le code.",
        "Rechercher toute contamination, fuite, obstruction ou signal incohérent sur ce composant et son câblage.",
        "Vérifier les points de service associés (niveau d'huile, pression, refroidissement, état du filtre ou du turbo si pertinent).",
        "Corriger le défaut constaté, effacer le code, réaliser un cycle de fonctionnement complet, puis relire la mémoire de défauts.",
    ],
}


# ---------------------------------------------------------------------------
# 6) GÉNÉRATION DE LA SOLUTION FINALE POUR UN CODE DONNÉ
# ---------------------------------------------------------------------------

def generer_solution(code: str, description: str) -> str:
    categorie = detecter_categorie(code)
    type_defaut = detecter_type_defaut(description)
    composant = detecter_composant(description)
    etapes = PROCEDURES.get(type_defaut, PROCEDURES["generique"])

    lignes = []
    lignes.append(f"Code : {code}")
    lignes.append(f"Description : {description}")
    lignes.append(f"Catégorie : {categorie}")
    lignes.append(f"Composant identifié : {composant}")
    lignes.append(f"Type de défaut détecté : {type_defaut.replace('_', ' ')}")
    lignes.append("")
    lignes.append("Procédure de diagnostic recommandée :")
    for i, etape in enumerate(etapes, start=1):
        lignes.append(f"  {i}. {etape}")
    lignes.append("")
    lignes.append(
        "Après intervention : effacer le code, effectuer un cycle de conduite complet "
        "(ralenti puis charge), et relire la mémoire de défauts pour confirmer que le code "
        "ne réapparaît pas avant toute réparation définitive."
    )
    lignes.append(
        "⚠ Procédure indicative — se référer à la revue technique constructeur pour les "
        "valeurs précises (couples de serrage, tensions, résistances) propres au véhicule."
    )
    return "\n".join(lignes)


# ---------------------------------------------------------------------------
# 7) POINT D'ENTRÉE
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    csv_path = CSV_PATH

    if "--csv" in args:
        idx = args.index("--csv")
        csv_path = args[idx + 1]
        del args[idx : idx + 2]

    codes_db = charger_codes(csv_path)
    if not codes_db:
        return

    if args:
        codes_a_traiter = [a.upper() for a in args]
    else:
        code_saisi = input("Entrez un code DTC (ex: P0301) : ").strip().upper()
        codes_a_traiter = [code_saisi]

    for code in codes_a_traiter:
        print("=" * 70)
        if code not in codes_db:
            print(f"Code {code} introuvable dans la base.")
            continue
        description = codes_db[code]
        print(generer_solution(code, description))
    print("=" * 70)


if __name__ == "__main__":
    main()