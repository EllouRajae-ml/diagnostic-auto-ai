# Dictionnaire de règles : mots-clés obligatoires -> panne
# Si TOUS les mots-clés d'une regle sont presents dans la phrase, on la retient

REGLES = [
    (["fume", "blanc"], "joint de culasse defectueux"),
    (["fume", "blanche"], "joint de culasse defectueux"),
    (["grincement", "frein"], "plaquettes de frein usees"),
    (["grince", "frein"], "plaquettes de frein usees"),
    (["volant", "tourne"], "rotule de direction usee"),
    (["volant", "braque"], "rotule de direction usee"),
    (["clim", "chaud"], "compresseur de climatisation en panne"),
    (["climatisation", "chaud"], "compresseur de climatisation en panne"),
    (["batterie", "demarre pas"], "batterie a plat"),
    (["phares", "eteints"], "batterie a plat"),
    (["fume", "noir"], "melange air carburant trop riche"),
    (["odeur", "oeuf"], "catalyseur defectueux"),
    (["odeur", "soufre"], "catalyseur defectueux"),
    (["huile", "consomme"], "segments de piston uses"),
    (["huile", "baisse"], "segments de piston uses"),
]

def chercher_regle(phrase):
    """
    Cherche si une regle correspond a la phrase.
    Retourne le nom de la panne si trouve, sinon None.
    """
    phrase_minuscule = phrase.lower()

    for mots_cles, panne in REGLES:
        if all(mot in phrase_minuscule for mot in mots_cles):
            return panne

    return None


def analyser_mesures(tension_batterie=None, temperature_moteur=None, niveau_huile=None, kilometrage=None):
    """
    Analyse les mesures techniques et retourne des alertes complementaires.
    Retourne une liste de messages d'alerte bases sur des seuils reels.
    """
    alertes = []

    if tension_batterie is not None:
        if tension_batterie < 12.0:
            alertes.append("🔴 Tension batterie critique (< 12.0V) — batterie fortement dechargee ou defectueuse")
        elif tension_batterie < 12.4:
            alertes.append("🟠 Tension batterie faible (< 12.4V) — a recharger ou tester")

    if temperature_moteur is not None:
        if temperature_moteur > 110:
            alertes.append("🔴 Surchauffe moteur critique (> 110°C) — arret immediat recommande")
        elif temperature_moteur > 105:
            alertes.append("🟠 Temperature moteur elevee (> 105°C) — verifier refroidissement")

    if niveau_huile is not None:
        if niveau_huile < 15:
            alertes.append("🔴 Niveau d'huile critique (< 15%) — risque de casse moteur")
        elif niveau_huile < 30:
            alertes.append("🟠 Niveau d'huile bas (< 30%) — appoint necessaire")

    if kilometrage is not None:
        if kilometrage > 150000:
            alertes.append("ℹ️ Kilometrage eleve (>150 000 km) — verifier courroie de distribution et embrayage")
        elif kilometrage > 100000:
            alertes.append("ℹ️ Kilometrage important (>100 000 km) — surveiller pieces d'usure")

    return alertes