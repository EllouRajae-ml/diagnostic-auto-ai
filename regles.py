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
        # Verifie si TOUS les mots-cles sont dans la phrase
        if all(mot in phrase_minuscule for mot in mots_cles):
            return panne
    
    return None