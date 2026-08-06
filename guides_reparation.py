"""
Base de guides de reparation step-by-step, indexee par code panne
(le code qui s'affiche dans le logiciel de diagnostic, ex: P0300).

Structure de GUIDES :
{
    "P0300": {
        "titre": "...",
        "gravite": "faible / moyenne / elevee",
        "etapes": ["etape 1", "etape 2", ...]
    },
    ...
}

Pour les codes qui ne sont PAS dans GUIDES (la grande majorité),
_guide_generique() ne renvoie plus un texte fixe : elle analyse la
description du code (dans CODES_DEFAUT) pour déterminer le type de
défaut (circuit ouvert, court-circuit, performance, communication...)
et le composant concerné, puis choisit des étapes adaptées. Résultat :
les guides varient réellement d'un code à l'autre.
"""

import re

from codes_defaut import CODES_DEFAUT

GUIDES = {
    "P0300": {
        "titre": "Rates d'allumage multiples / aleatoires",
        "gravite": "elevee",
        "etapes": [
            "Brancher la valise diagnostic et relever les cylindres concernes (freeze frame).",
            "Controler visuellement les bougies d'allumage : usure, encrassement, ecartement.",
            "Verifier l'etat des bobines / faisceau d'allumage (fissures, traces d'arc).",
            "Controler les injecteurs concernes (etancheite, resistance electrique).",
            "Verifier la pression carburant a la rampe d'injection.",
            "Controler les fuites d'admission (durites, joint de collecteur) au moyen d'un spray detecteur.",
            "Effacer les codes, effectuer un essai routier, puis relire la memoire de defauts.",
        ],
    },
    "P0171": {
        "titre": "Melange trop pauvre (Banque 1)",
        "gravite": "moyenne",
        "etapes": [
            "Verifier les fuites d'admission en amont du debitmetre (durites, joints, pipe admission).",
            "Nettoyer et controler le debitmetre (MAF) / capteur de pression collecteur (MAP).",
            "Controler la pression et le debit de la pompe a carburant.",
            "Verifier l'etat des injecteurs (encrassement, debit).",
            "Controler la sonde lambda amont (reponse, temps de reaction).",
            "Verifier l'absence de fuite au niveau du joint de culasse / systeme EGR.",
            "Effacer les codes et verifier la correction de melange en temps reel (valeur STFT/LTFT).",
        ],
    },
    "P0420": {
        "titre": "Rendement catalyseur insuffisant (Banque 1)",
        "gravite": "moyenne",
        "etapes": [
            "Controler l'absence de fuite d'echappement en amont du catalyseur.",
            "Verifier l'etat et la reponse de la sonde lambda amont et aval.",
            "Controler les rates d'allumage (une cause frequente de catalyseur endommage).",
            "Inspecter visuellement/thermiquement le catalyseur (nid d'abeille bouche ou fondu).",
            "Verifier la temperature d'echappement en amont/aval du catalyseur (ecart attendu).",
            "Si le catalyseur est hors service : remplacement necessaire (piece + MO).",
        ],
    },
    "P0128": {
        "titre": "Thermostat - temperature moteur trop basse",
        "gravite": "faible",
        "etapes": [
            "Verifier le niveau et l'etat du liquide de refroidissement.",
            "Controler le fonctionnement du thermostat (ouverture a la bonne temperature).",
            "Verifier le capteur de temperature moteur (resistance, cablage).",
            "Controler que le circuit court (chauffage habitacle) fonctionne normalement.",
            "Remplacer le thermostat si blocage en position ouverte constate.",
        ],
    },
    "P0442": {
        "titre": "Fuite systeme EVAP (petite fuite)",
        "gravite": "faible",
        "etapes": [
            "Verifier le serrage et l'etat du bouchon de reservoir carburant.",
            "Controler visuellement les durites du circuit EVAP (fissures, debranchement).",
            "Verifier l'etanchite du canister (charbon actif) et de son electrovanne.",
            "Effectuer un test de fumee (fumigene) pour localiser la fuite si disponible.",
            "Effacer les codes et effectuer un cycle de conduite complet pour confirmation.",
        ],
    },
    "P0562": {
        "titre": "Tension systeme trop basse",
        "gravite": "moyenne",
        "etapes": [
            "Mesurer la tension batterie au repos (attendu ~12.6V) et moteur tournant (~13.5-14.5V).",
            "Controler l'etat des cosses et la propreter des bornes batterie.",
            "Verifier la courroie et le fonctionnement de l'alternateur (charge sous charge electrique).",
            "Controler l'etat general de la batterie (test de charge / capacite).",
            "Verifier les fusibles et le cablage d'alimentation principal.",
        ],
    },
    "P0011": {
        "titre": "Calage arbre a cames (avance) - Banque 1",
        "gravite": "elevee",
        "etapes": [
            "Verifier le niveau et la qualite de l'huile moteur (viscosite, encrassement).",
            "Controler la pression d'huile moteur.",
            "Verifier le fonctionnement de l'electrovanne de calage variable (VVT).",
            "Controler l'etat de la chaine/courroie de distribution et son tendeur.",
            "Verifier le calage effectif via l'outil diagnostic (valeur reelle vs consigne).",
        ],
    },
    "P0016": {
        "titre": "Correlation position vilebrequin / arbre a cames",
        "gravite": "elevee",
        "etapes": [
            "Verifier visuellement le calage de la distribution (reperes chaine/courroie).",
            "Controler l'etat du tendeur et des patins de distribution.",
            "Verifier les capteurs PMH (vilebrequin) et arbre a cames (entrefer, cablage).",
            "Controler l'absence de jeu anormal sur la chaine de distribution.",
            "Ne pas faire tourner le moteur si un saut de calage est suspecte (risque moteur).",
        ],
    },
}


# ---------------------------------------------------------------------------
# DÉTECTION DU TYPE DE DÉFAUT À PARTIR DE LA DESCRIPTION DU CODE
# ---------------------------------------------------------------------------

REGLES_TYPE_DEFAUT = [
    (r"communication perdue|bus de communication|autobus", "communication"),
    (r"ratés? d.allumage", "rates_allumage"),
    (r"débit (insuffisant|excessif|incorrect)|problème de débit", "debit"),
    (r"apprise|apprentissage", "performance"),
    (r"préchauffage", "chauffage"),
    (r"calage.*(avancé|retardé|excessivement)", "calage"),
    (r"signaux? .*invers|invers.*signal", "signaux_inverses"),
    (r"mélange trop (riche|pauvre)|ajustement du carburant", "melange_carburant"),
    (r"défaut d.équilibrage|quantité de (fuel|carburant) inject", "equilibrage_injection"),
    (r"régime excessif|vitesse excessive|sur-?régime", "survitesse"),
    (r"sélection de la vitesse|patinage|vitesses? engagée|durée de changement de vitesse|"
     r"montée des vitesses|problème de changement de vitesse",
     "passage_vitesse"),
    (r"circuit ouvert|panne d[eu] circuit|circuit.*\bouvert\b|circuit open|\bouvert\b",
     "circuit_ouvert"),
    (r"court-circuit.*(batterie|vbatt|l.alimentation)|short to battery|short.*batter|"
     r"circuit trop haut|circuit .* trop fort|signal haut|valeur d.entrée trop haute",
     "circuit_haut"),
    (r"court-circuit.*(terre|masse|ground)|short to ground|short.*(terre|masse)|"
     r"circuit trop bas|circuit .* trop faible|signal bas|valeur d.entrée trop basse",
     "circuit_bas"),
    (r"court-?circuit", "circuit_ouvert"),
    (r"circuit intermittent", "circuit_intermittent"),
    (r"réponse lente", "reponse_lente"),
    (r"pas d.activité détectée|aucun signal|no signal", "signal_absent"),
    (r"résistance du chauffage|commande de chauffage", "chauffage"),
    (r"plage de mesure|performance|rendement|corrélation|blocage|limite dépassée", "performance"),
    (r"erreur de somme|checksum|erreur interne|données inadmissibles|erreur d[eu] |"
     r"erreur (RAM|ROM|KAM|de processeur|de programmation)|désaccord|non programmé",
     "calculateur_interne"),
    (r"fuite", "fuite"),
    (r"surchauffe|température .* trop haute|température .* trop basse|insuffisante", "temperature"),
    (r"échec.*circuit|circuit.*échec|failure|défaut de fonctionnement", "circuit_ouvert"),
    (r"trop faible|trop basse", "circuit_bas"),
    (r"trop fort[ee]?|trop haute", "circuit_haut"),
    (r"\bélectrique\b|\belectric\b", "circuit_ouvert"),
    (r"basse tension|flux .* (faible|bas)|perte de charge", "circuit_bas"),
    (r"haute tension|surcharge|flux .* (élevé|haut)", "circuit_haut"),
    (r"inférieur au seuil|en dessous du seuil|plus (lent|rapide) que prévu|rationalité|\bincorrect\b",
     "performance"),
    (r"instable", "circuit_intermittent"),
    (r"bloqu", "performance"),
    (r"\bpanne\b", "circuit_ouvert"),
    (r"\bfaible\b|\bbasse\b", "circuit_bas"),
    (r"\bélevé[e]?\b|\bhaute\b|\bexcessive?\b", "circuit_haut"),
]


def _detecter_type_defaut(description: str) -> str:
    desc = (description or "").lower()
    for motif, type_defaut in REGLES_TYPE_DEFAUT:
        if re.search(motif, desc, re.IGNORECASE):
            return type_defaut
    return "generique"


COMPOSANTS_CONNUS = [
    "sonde lambda", "capteur de vilebrequin", "capteur d'arbre à cames",
    "capteur de vitesse", "injecteur", "bobine d'allumage", "électrovanne",
    "débitmètre d'air", "capteur de pression", "sonde de température",
    "catalyseur", "turbocompresseur", "egr", "pompe à carburant",
    "calculateur", "module de commande", "capteur de position",
    "contacteur", "relais", "capteur d'angle de direction",
    "capteur de vitesse de roue", "airbag", "colonne de direction",
]


def _detecter_composant(description: str) -> str:
    desc = (description or "").lower()
    for comp in COMPOSANTS_CONNUS:
        if comp in desc:
            return comp
    mots = re.split(r"[,\-–]", description or "")
    return mots[0].strip().lower() if mots and mots[0].strip() else "composant à identifier"


# ---------------------------------------------------------------------------
# ÉTAPES SPÉCIFIQUES PAR TYPE DE DÉFAUT (remplace le texte fixe des étapes 3-7)
# ---------------------------------------------------------------------------

ETAPES_PAR_TYPE_DEFAUT = {
    "communication": [
        "Contrôlez l'alimentation +12V et la masse du module signalé (connecteur débranché, multimètre).",
        "Vérifiez la continuité et l'isolement des lignes de bus CAN-H / CAN-L (pas de coupure, pas de court-circuit entre elles).",
        "Contrôlez la résistance de terminaison du bus (environ 60 ohms mesurés aux deux extrémités en parallèle, selon schéma constructeur).",
        "Si plusieurs modules sont en défaut simultanément, déconnectez-les un par un pour isoler celui qui pollue le réseau.",
    ],
    "circuit_ouvert": [
        "Contrôlez la continuité complète du câblage entre le calculateur et le composant (fil coupé, connecteur débranché).",
        "Vérifiez la propreté et le verrouillage des connecteurs aux deux extrémités du circuit.",
        "Mesurez la résistance du composant lui-même et comparez-la à la valeur constructeur.",
        "Contrôlez le fusible et le relais associés à ce circuit si le câblage est bon.",
    ],
    "circuit_haut": [
        "Recherchez un court-circuit du fil de signal vers le +12V (isolant endommagé, frottement de câblage).",
        "Vérifiez que le composant n'est pas alimenté en direct par erreur après une intervention récente.",
        "Contrôlez la tension de référence envoyée par le calculateur (souvent 5V) : si déjà anormale en amont, suspecter le calculateur.",
        "Débranchez le composant et mesurez la tension résiduelle sur le fil signal pour localiser le défaut (câblage ou composant).",
    ],
    "circuit_bas": [
        "Recherchez un court-circuit du fil de signal vers la masse (isolant endommagé, pincement de câblage).",
        "Mesurez la résistance du composant : une valeur anormalement basse indique un composant interne en court-circuit.",
        "Contrôlez la propreté des masses du véhicule proches du circuit concerné.",
        "Débranchez le composant : si la tension reste basse fil débranché, le défaut est côté câblage vers le calculateur.",
    ],
    "circuit_intermittent": [
        "Reproduisez le défaut en sollicitant le faisceau (vibrations, torsion douce) tout en surveillant la valeur en temps réel sur la valise.",
        "Inspectez les connecteurs pour oxydation ou mauvais verrouillage, cause la plus fréquente de défaut intermittent.",
        "Contrôlez les points de passage du câblage (charnières, passages de cloison) pour usure ou frottement.",
        "Si rien n'est trouvé au repos, réalisez un essai routier avec la valise connectée en enregistrement continu.",
    ],
    "reponse_lente": [
        "Nettoyez ou remplacez le composant si son temps de réponse ne respecte plus les spécifications (fréquent sur sondes encrassées).",
        "Vérifiez l'absence de fuite parasite en amont si le composant est une sonde de mélange.",
        "Contrôlez la propreté et le verrouillage du connecteur (une résistance de contact ajoute un retard électrique).",
        "Assurez-vous que le composant a atteint sa température de fonctionnement avant le diagnostic.",
    ],
    "signal_absent": [
        "Vérifiez l'alimentation et la masse du capteur au multimètre, moteur en fonctionnement si applicable.",
        "Contrôlez la continuité du fil de signal jusqu'au calculateur.",
        "Inspectez le composant pour dommage mécanique (denture cassée, entrefer trop grand sur capteurs inductifs).",
        "Si le signal reste absent malgré un câblage correct, remplacez le composant.",
    ],
    "chauffage": [
        "Mesurez la résistance de l'élément chauffant du composant et comparez-la à la valeur constructeur.",
        "Vérifiez l'alimentation du relais ou du circuit de commande de chauffage.",
        "Contrôlez le fusible dédié au circuit de chauffage.",
        "Si la résistance est hors tolérance, remplacez le composant.",
    ],
    "performance": [
        "Comparez la valeur mesurée en temps réel (valise) à la plage attendue dans différentes conditions (ralenti, charge, régime).",
        "Vérifiez qu'aucun autre code lié ne pointe vers une cause commune (fuite d'air, capteur en amont défectueux).",
        "Contrôlez l'état physique du composant (encrassement, corrosion, jeu mécanique).",
        "Réalisez un nouvel apprentissage / une réinitialisation adaptative si le composant vient d'être remplacé.",
    ],
    "calculateur_interne": [
        "Vérifiez la stabilité de l'alimentation électrique du calculateur (chute de tension batterie, masse oxydée).",
        "Recherchez une mise à jour logicielle constructeur corrective si disponible.",
        "Si le défaut persiste après effacement et un cycle de conduite complet, envisagez le remplacement du calculateur.",
        "Avant tout remplacement, notez la configuration (VIN, options) pour la reprogrammation du nouveau boîtier.",
    ],
    "fuite": [
        "Réalisez un test de fumée (fumigène) sur le circuit concerné pour localiser précisément le point de fuite.",
        "Contrôlez l'état des durites, colliers de serrage et joints du système concerné.",
        "Vérifiez que le bouchon ou le clapet associé ferme correctement.",
        "Réparez ou remplacez l'élément fuyard, puis effacez la mémoire et revalidez.",
    ],
    "temperature": [
        "Vérifiez le niveau et l'état du liquide de refroidissement ou du fluide concerné.",
        "Contrôlez le bon fonctionnement du ou des motoventilateurs de refroidissement.",
        "Vérifiez l'absence d'obstruction (radiateur encrassé, grille d'air bouchée).",
        "Contrôlez le thermostat et la sonde de température elle-même.",
    ],
    "rates_allumage": [
        "Identifiez le(s) cylindre(s) concerné(s) d'après le numéro dans le code (ex : P0301 = cylindre 1), ou relevez le freeze frame si non spécifié.",
        "Contrôlez la bougie du cylindre concerné : état de l'électrode, écartement, dépôt (noir = trop riche, blanc = trop pauvre).",
        "Permutez la bobine avec celle d'un autre cylindre : si le raté suit la bobine lors du changement, elle est en cause.",
        "Si bougie et bobine sont bonnes, contrôlez l'injecteur du même cylindre, puis en dernier recours réalisez un test de compression.",
    ],
    "debit": [
        "Comparez, via la valise, la position/le débit réel du composant (vanne, électrovanne) à la valeur demandée.",
        "Inspectez le composant pour encrassement ou blocage mécanique (dépôt de calamine fréquent sur EGR et injection d'air secondaire).",
        "Vérifiez l'absence de fuite ou d'obstruction sur les durites et canalisations associées.",
        "Nettoyez ou remplacez le composant selon le résultat, puis validez le débit réel après intervention.",
    ],
    "calage": [
        "Vérifiez le niveau et la qualité de l'huile moteur : une pression d'huile insuffisante est la cause la plus fréquente d'un mauvais calage variable (VVT).",
        "Contrôlez le fonctionnement de l'électrovanne de calage variable (dépose, test de commande à la valise si accessible).",
        "Inspectez l'état de la chaîne/courroie de distribution et de son tendeur (allongement, usure).",
        "Comparez le calage réel affiché par la valise à la valeur de consigne pour confirmer l'écart avant intervention.",
    ],
    "signaux_inverses": [
        "Vérifiez au connecteur du calculateur que les fils des deux capteurs/sondes concernés ne sont pas physiquement intervertis.",
        "Contrôlez la continuité de chaque fil individuellement jusqu'à sa broche d'origine sur le calculateur.",
        "Si les connecteurs sont bien branchés, suspectez une erreur de câblage lors d'une intervention antérieure sur ce circuit.",
        "Corrigez le branchement si besoin, effacez le code et vérifiez la cohérence des deux signaux en temps réel.",
    ],
    "melange_carburant": [
        "Recherchez une fuite d'admission (durites, joints, pipe d'admission) en amont du débitmètre ou du capteur de pression collecteur.",
        "Contrôlez la pression et le débit de la pompe à carburant.",
        "Vérifiez l'état et la réponse de la ou des sondes lambda concernées.",
        "Inspectez les injecteurs (encrassement, débit, étanchéité) et l'absence de fuite au niveau du joint de culasse ou de l'EGR.",
    ],
    "equilibrage_injection": [
        "Identifiez précisément le cylindre concerné d'après la description du code.",
        "Contrôlez la résistance électrique et l'étanchéité de l'injecteur de ce cylindre.",
        "Comparez, si possible sur banc, le débit de cet injecteur à celui des autres cylindres.",
        "Vérifiez la pression rampe/rail commune à tous les injecteurs avant de conclure à un injecteur isolé.",
    ],
    "survitesse": [
        "Vérifiez la cohérence entre le régime moteur affiché sur la valise et le régime réel.",
        "Contrôlez le capteur de vitesse/régime concerné (câblage, entrefer, fixation).",
        "Recherchez une cause mécanique (rétrogradage intempestif, patinage d'embrayage sur boîte automatique).",
        "Effacez le code après correction et surveillez la valeur en temps réel lors d'un essai routier.",
    ],
    "passage_vitesse": [
        "Contrôlez le niveau et l'état de l'huile de boîte automatique (une huile dégradée est la cause la plus fréquente de patinage ou de passages anormaux).",
        "Notez si le défaut survient à un rapport précis (électrovanne suspecte) ou sur tous les rapports (problème hydraulique général).",
        "Testez électriquement l'électrovanne ou le capteur de rapport engagé concerné (résistance, câblage).",
        "Effectuez une vidange complète si l'huile est dégradée avant de conclure à une panne purement électronique — beaucoup de défauts disparaissent après une simple vidange.",
    ],
    "generique": [
        "Contrôlez l'alimentation du composant concerné, la masse et les tensions de référence avec un multimètre.",
        "Inspectez le composant, le capteur, l'injecteur, la bobine, le relais ou la soupape lié au défaut : usure, contamination, fuite, obstruction.",
        "Vérifiez les points de service associés (niveau d'huile, pression carburant, refroidissement, état du filtre/turbo si pertinent).",
        "Corrigez le défaut constaté, effacez le code, réalisez un cycle de fonctionnement complet, puis relisez la mémoire de défauts.",
    ],
}


def _tenter_guide_ia(code, description, modele=None, debug=False):
    """
    Tente de générer un guide via l'IA (OpenAI, à travers ia_fallback._appel_externe)
    pour un code dont la description n'a permis de détecter aucun type de défaut
    local (ex : descriptions mal traduites, cas très spécifiques).

    Retourne None si l'appel échoue (pas de clé API, erreur réseau, etc.) —
    l'appelant doit alors continuer avec le guide générique local classique
    comme filet de sécurité. Aucune exception n'est jamais levée ici.
    """
    try:
        from ia_fallback import _appel_externe
    except Exception:
        return None

    if description:
        phrase = f"Code défaut OBD {code} : {description}"
    else:
        phrase = f"Code défaut OBD {code} (aucune description répertoriée localement)"

    reponse = _appel_externe(phrase, modele=modele, debug=debug)
    if not reponse:
        return None

    etapes = [ligne.strip("-• ").strip() for ligne in reponse.split("\n") if ligne.strip()]
    if not etapes:
        etapes = [reponse]

    return {
        "titre": f"Diagnostic IA — {code} (non couvert par la base locale)",
        "gravite": "moyenne",
        "etapes": etapes,
    }


def _guide_generique(code, modele=None, debug=False):
    """
    Retourne un guide adapté au type de défaut ET au composant détectés
    dans la description réelle du code (via CODES_DEFAUT), et non plus
    un texte fixe identique pour tous les codes.
    """
    prefixe = code[:1] if code else "?"
    categorie = {
        "P": "Paramètre moteur / injection / combustion",
        "C": "Châssis / ABS / freinage",
        "B": "Body / accessoires / confort",
        "U": "Réseau / communication / bus",
    }.get(prefixe, "Système OBD")

    description = CODES_DEFAUT.get(code, "") if isinstance(CODES_DEFAUT, dict) else ""

    if "aucune panne" in description.lower():
        return {
            "titre": f"Aucune panne détectée — {code}",
            "gravite": "faible",
            "etapes": [
                "Ce code signifie qu'aucun défaut actif n'est mémorisé pour cette position.",
                "Rien à réparer : si ce code apparaît isolément, il s'agit généralement d'une valeur de remplissage sans signification technique.",
            ],
        }

    type_defaut = _detecter_type_defaut(description)

    if type_defaut == "generique":
        guide_ia = _tenter_guide_ia(code, description, modele=modele, debug=debug)
        if guide_ia:
            return guide_ia
        # Aucune clé API / échec réseau : on continue ci-dessous avec le
        # guide générique local classique, qui reste toujours disponible.

    composant = _detecter_composant(description)
    etapes_specifiques = ETAPES_PAR_TYPE_DEFAUT.get(type_defaut, ETAPES_PAR_TYPE_DEFAUT["generique"])

    etapes = [
        f"1. Relisez le code {code} sur la valise de diagnostic et notez le freeze frame : "
        f"régime moteur, température, km, charge, et durée d'apparition du défaut.",
        f"2. Identifiez la zone concernée sur le plan {categorie}. "
        f"Composant probable d'après la description du code : {composant}. "
        f"Type de défaut détecté : {type_defaut.replace('_', ' ')}.",
    ]
    for i, etape in enumerate(etapes_specifiques, start=3):
        etapes.append(f"{i}. {etape}")
    etapes.append(
        f"{len(etapes) + 1}. Corrigez le défaut constaté, effacez le code, réalisez un cycle de "
        f"fonctionnement complet, puis relisez la mémoire de défauts pour confirmer qu'il ne réapparaît pas."
    )

    gravite = "elevee" if type_defaut in ("communication", "calculateur_interne") else "moyenne"

    return {
        "titre": f"Diagnostic {type_defaut.replace('_', ' ')} — {code}"
        if type_defaut != "generique" else f"Diagnostic générique — {code}",
        "gravite": gravite,
        "etapes": etapes,
    }


def rechercher_guide(code, modele=None, debug=False):
    """Recherche un guide par code panne (insensible a la casse/espaces).

    modele et debug sont transmis à l'appel IA de secours (voir
    _tenter_guide_ia) pour les codes non couverts par les règles locales —
    ils sont ignorés pour les codes qui ont un guide local (ciblé ou nommé).
    """
    if not code:
        return None
    code_normalise = code.strip().upper().replace(" ", "")
    if code_normalise in GUIDES:
        return GUIDES[code_normalise]
    return _guide_generique(code_normalise, modele=modele, debug=debug)


def codes_disponibles():
    """Retourne la liste de tous les codes OBD connus, y compris ceux qui utilisent le guide générique."""
    return sorted(set(GUIDES.keys()) | set(CODES_DEFAUT.keys()))
