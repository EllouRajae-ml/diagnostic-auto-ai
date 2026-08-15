# Dictionnaire de règles : mots-clés obligatoires -> panne
# Si TOUS les mots-clés d'une regle sont presents dans la phrase, on la retient
# L'ordre compte : la premiere regle qui matche est retenue en premier,
# donc les regles les plus specifiques sont placees avant les plus generales.
#
# Version elargie : plusieurs formulations/synonymes par panne pour
# maximiser les chances de match local et eviter l'appel IA externe.

REGLES = [
    # =========================================================
    # BATTERIE / DEMARRAGE
    # =========================================================
    (["batterie", "demarre pas"], "batterie a plat"),
    (["batterie", "ne demarre pas"], "batterie a plat"),
    (["phares", "eteints"], "batterie a plat"),
    (["demarre pas", "rien"], "batterie a plat"),
    (["ne demarre pas", "rien"], "batterie a plat"),
    (["voiture", "morte"], "batterie a plat"),
    (["aucun bruit", "demarrage"], "batterie a plat"),
    (["tableau de bord", "eteint"], "batterie a plat"),
    (["rien ne s allume"], "batterie a plat"),

    (["batterie", "faible"], "batterie faible ou usee"),
    (["batterie", "vieille"], "batterie faible ou usee"),
    (["batterie", "ancienne"], "batterie faible ou usee"),
    (["demarre difficilement", "matin"], "batterie faible ou usee"),
    (["demarre mal", "froid"], "batterie faible ou usee"),
    (["batterie", "tient pas la charge"], "batterie faible ou usee"),

    (["cosses", "corrodees"], "bornes de batterie corrodees"),
    (["cosses", "oxydees"], "bornes de batterie corrodees"),
    (["bornes", "oxydees"], "bornes de batterie corrodees"),
    (["bornes", "blanches"], "bornes de batterie corrodees"),
    (["bornes", "vertes"], "bornes de batterie corrodees"),

    (["batterie", "vide", "matin"], "fuite de courant electrique"),
    (["decharge", "nuit"], "fuite de courant electrique"),
    (["batterie", "se decharge", "seule"], "fuite de courant electrique"),
    (["batterie", "se vide toute seule"], "fuite de courant electrique"),
    (["consommation", "parasite"], "fuite de courant electrique"),

    (["alternateur", "charge"], "alternateur defectueux"),
    (["voyant", "batterie", "allume"], "alternateur defectueux"),
    (["voyant batterie"], "alternateur defectueux"),
    (["batterie", "se recharge pas"], "alternateur defectueux"),

    (["court", "circuit"], "court circuit electrique"),
    (["fusible", "grille", "souvent"], "court circuit electrique"),
    (["odeur", "brule", "electrique"], "court circuit electrique"),
    (["fumee", "tableau de bord"], "court circuit electrique"),

    (["clignotant", "marche pas"], "ampoule de clignotant grillee"),
    (["clignotant", "fonctionne pas"], "ampoule de clignotant grillee"),
    (["clignotant", "grille"], "ampoule de clignotant grillee"),
    (["clignotant", "clignote vite"], "ampoule de clignotant grillee"),
    (["clignotant", "rapide"], "ampoule de clignotant grillee"),

    (["feu de position", "marche pas"], "ampoule feu de position grillee"),
    (["feu de position", "eteint"], "ampoule feu de position grillee"),
    (["veilleuse", "grillee"], "ampoule feu de position grillee"),
    (["veilleuse", "marche pas"], "ampoule feu de position grillee"),

    (["klaxon", "marche pas"], "fusible klaxon grille"),
    (["klaxon", "muet"], "fusible klaxon grille"),
    (["klaxon", "fonctionne pas"], "fusible klaxon grille"),
    (["klaxon", "silencieux"], "fusible klaxon grille"),

    (["demarreur", "clic"], "relais de demarreur defectueux"),
    (["demarreur", "clic clic"], "relais de demarreur defectueux"),
    (["cle", "tourne", "rien"], "relais de demarreur defectueux"),
    (["contact", "aucun bruit"], "relais de demarreur defectueux"),

    (["demarreur", "tourne pas"], "pignon du demarreur use"),
    (["demarreur", "grince"], "pignon du demarreur use"),
    (["demarreur", "bruit metallique"], "pignon du demarreur use"),
    (["demarreur", "crisse"], "pignon du demarreur use"),

    # =========================================================
    # ALLUMAGE / COMBUSTION / MOTEUR
    # =========================================================
    (["bougie", "usee"], "bougies usees"),
    (["bougie", "encrassee"], "bougies usees"),
    (["moteur", "demarre difficilement", "essence"], "bougies usees"),
    (["allumage", "difficile"], "bougies usees"),

    (["rate", "allumage"], "bobine d allumage defectueuse"),
    (["rates", "moteur"], "bobine d allumage defectueuse"),
    (["moteur", "saccade"], "bobine d allumage defectueuse"),
    (["moteur", "tremble"], "bobine d allumage defectueuse"),
    (["moteur", "broute"], "bobine d allumage defectueuse"),
    (["a coups", "acceleration"], "bobine d allumage defectueuse"),
    (["voyant moteur clignote"], "bobine d allumage defectueuse"),

    (["fume", "blanc"], "joint de culasse defectueux"),
    (["fume", "blanche"], "joint de culasse defectueux"),
    (["fumee", "blanche", "echappement"], "joint de culasse defectueux"),
    (["huile", "melangee", "eau"], "joint de culasse defectueux"),
    (["liquide de refroidissement", "huile"], "joint de culasse defectueux"),

    (["fume", "bleu"], "segments de piston uses"),
    (["fume", "bleue"], "segments de piston uses"),
    (["fumee", "bleue", "echappement"], "segments de piston uses"),
    (["huile", "consomme"], "segments de piston uses"),
    (["huile", "baisse"], "segments de piston uses"),
    (["consommation", "huile", "excessive"], "segments de piston uses"),
    (["huile", "disparait"], "segments de piston uses"),

    (["fume", "noir"], "melange air carburant trop riche"),
    (["fume", "noire"], "melange air carburant trop riche"),
    (["fumee", "noire", "echappement"], "melange air carburant trop riche"),
    (["consomme", "trop", "carburant"], "melange air carburant trop riche"),
    (["surconsommation", "essence"], "melange air carburant trop riche"),

    (["injecteur", "encrasse"], "injecteurs encrasses"),
    (["moteur", "broute", "ralenti"], "injecteurs encrasses"),
    (["ralenti", "instable", "moteur"], "injecteurs encrasses"),
    (["moteur", "tousse"], "injecteurs encrasses"),

    (["carburant", "filtre"], "filtre a carburant colmate"),
    (["filtre carburant", "colmate"], "filtre a carburant colmate"),
    (["perte", "puissance", "cote"], "filtre a carburant colmate"),
    (["moteur", "s etouffe"], "filtre a carburant colmate"),

    (["turbo", "sifflement"], "turbo defectueux"),
    (["turbo", "siffle"], "turbo defectueux"),
    (["manque", "puissance"], "turbo defectueux"),
    (["fumee", "bleue", "acceleration"], "turbo defectueux"),
    (["sifflement", "acceleration"], "turbo defectueux"),

    (["sonde", "lambda"], "sonde lambda defectueuse"),
    (["voyant moteur", "consommation"], "sonde lambda defectueuse"),
    (["consommation", "augmente", "soudainement"], "sonde lambda defectueuse"),

    (["filtre a air", "encrasse"], "filtre a air encrasse"),
    (["filtre air", "sale"], "filtre a air encrasse"),
    (["moteur", "manque de souffle"], "filtre a air encrasse"),
    (["acceleration", "molle"], "filtre a air encrasse"),

    # =========================================================
    # FREINAGE
    # =========================================================
    (["grincement", "frein"], "plaquettes de frein usees"),
    (["grince", "frein"], "plaquettes de frein usees"),
    (["freinage", "grince"], "plaquettes de frein usees"),
    (["bruit metallique", "freinage"], "plaquettes de frein usees"),
    (["frein", "couine"], "plaquettes de frein usees"),
    (["plaquettes", "usees"], "plaquettes de frein usees"),

    (["pedale", "spongieuse"], "air dans le circuit de freinage"),
    (["pedale de frein", "molle"], "air dans le circuit de freinage"),
    (["frein", "s enfonce trop"], "air dans le circuit de freinage"),
    (["pedale frein", "enfonce fond"], "air dans le circuit de freinage"),

    (["frein", "vibre"], "disques de frein voiles"),
    (["volant", "vibre", "freinage"], "disques de frein voiles"),
    (["disque", "voile"], "disques de frein voiles"),
    (["freinage", "vibration"], "disques de frein voiles"),
    (["pedale", "vibre", "freinage"], "disques de frein voiles"),

    (["frein", "tire", "cote"], "etrier de frein grippe"),
    (["voiture", "tire", "freinage"], "etrier de frein grippe"),
    (["etrier", "grippe"], "etrier de frein grippe"),
    (["roue", "chauffe"], "etrier de frein grippe"),

    (["liquide de frein", "bas"], "niveau liquide de frein bas"),
    (["voyant", "liquide de frein"], "niveau liquide de frein bas"),
    (["niveau frein", "bas"], "niveau liquide de frein bas"),

    (["frein a main", "course"], "cable de frein a main detendu"),
    (["frein a main", "detendu"], "cable de frein a main detendu"),
    (["frein a main", "monte trop haut"], "cable de frein a main detendu"),
    (["frein a main", "tient pas"], "cable de frein a main detendu"),

    # =========================================================
    # DIRECTION / SUSPENSION / PNEUS
    # =========================================================
    (["volant", "tourne"], "rotule de direction usee"),
    (["volant", "braque"], "rotule de direction usee"),
    (["bruit", "virage"], "rotule de direction usee"),
    (["claquement", "direction"], "rotule de direction usee"),
    (["jeu", "volant"], "rotule de direction usee"),

    (["direction assistee", "dure"], "pompe de direction assistee defectueuse"),
    (["volant", "lourd"], "pompe de direction assistee defectueuse"),
    (["direction", "difficile", "tourner"], "pompe de direction assistee defectueuse"),
    (["volant", "dur a tourner"], "pompe de direction assistee defectueuse"),

    (["vibration", "vitesse"], "pneus desequilibres"),
    (["volant", "vibre", "route"], "pneus desequilibres"),
    (["vibre", "autoroute"], "pneus desequilibres"),
    (["tremblement", "haute vitesse"], "pneus desequilibres"),

    (["voiture", "tire", "route"], "parallelisme desregle"),
    (["voiture", "tire", "droite"], "parallelisme desregle"),
    (["voiture", "tire", "gauche"], "parallelisme desregle"),
    (["pneus", "usure", "irreguliere"], "parallelisme desregle"),
    (["usure", "anormale", "pneu"], "parallelisme desregle"),

    (["pneu", "degonfle", "lentement"], "fuite lente pneu"),
    (["pneu", "perd", "pression"], "fuite lente pneu"),
    (["pression", "pneu", "baisse"], "fuite lente pneu"),

    (["amortisseur", "rebond"], "amortisseurs uses"),
    (["voiture", "rebondit"], "amortisseurs uses"),
    (["suspension", "molle"], "amortisseurs uses"),
    (["voiture", "tangue"], "amortisseurs uses"),
    (["amortisseur", "fuite"], "amortisseurs uses"),

    (["suspension", "affaisse"], "ressorts de suspension fatigues"),
    (["voiture", "basse", "avant"], "ressorts de suspension fatigues"),
    (["hauteur", "caisse", "differente"], "ressorts de suspension fatigues"),
    (["ressort", "casse"], "ressorts de suspension fatigues"),

    (["bruit", "bosse"], "biellette de barre stabilisatrice cassee"),
    (["cliquetis", "route"], "biellette de barre stabilisatrice cassee"),
    (["bruit", "nid de poule"], "biellette de barre stabilisatrice cassee"),
    (["biellette", "cassee"], "biellette de barre stabilisatrice cassee"),

    (["geometrie", "roues"], "geometrie des roues desreglee"),
    (["geometrie", "desreglee"], "geometrie des roues desreglee"),

    # =========================================================
    # REFROIDISSEMENT
    # =========================================================
    (["fuite", "refroidissement"], "fuite liquide de refroidissement"),
    (["fuite", "liquide", "moteur"], "fuite liquide de refroidissement"),
    (["fuite", "sous la voiture", "vert"], "fuite liquide de refroidissement"),
    (["flaque", "liquide", "vert"], "fuite liquide de refroidissement"),
    (["niveau", "liquide refroidissement", "baisse"], "fuite liquide de refroidissement"),

    (["pompe a eau", "fuite"], "pompe a eau defectueuse"),
    (["pompe a eau", "bruit"], "pompe a eau defectueuse"),
    (["bruit", "sous le capot", "aigu"], "pompe a eau defectueuse"),

    (["temperature", "capteur"], "capteur de temperature defaillant"),
    (["jauge temperature", "erratique"], "capteur de temperature defaillant"),
    (["temperature", "affiche n importe quoi"], "capteur de temperature defaillant"),

    (["surchauffe"], "thermostat bloque"),
    (["moteur", "chauffe trop"], "thermostat bloque"),
    (["temperature", "monte vite"], "thermostat bloque"),
    (["aiguille temperature", "rouge"], "thermostat bloque"),

    (["temperature", "monte jamais"], "thermostat bloque en position ouverte"),
    (["chauffage", "chauffe pas"], "thermostat bloque en position ouverte"),
    (["moteur", "chauffe jamais"], "thermostat bloque en position ouverte"),

    (["radiateur", "perce"], "radiateur perce"),
    (["radiateur", "fuite"], "radiateur perce"),
    (["radiateur", "fissure"], "radiateur perce"),

    # =========================================================
    # MOTEUR / HUILE / DISTRIBUTION
    # =========================================================
    (["niveau", "huile", "bas"], "niveau d huile bas"),
    (["jauge huile", "bas"], "niveau d huile bas"),
    (["voyant", "niveau huile"], "niveau d huile bas"),

    (["pression", "huile"], "pompe a huile defectueuse"),
    (["voyant", "huile", "allume"], "pompe a huile defectueuse"),
    (["voyant huile rouge"], "pompe a huile defectueuse"),

    (["courroie de distribution", "use"], "courroie de distribution usee"),
    (["courroie", "craquelee"], "courroie de distribution usee"),
    (["bruit", "distribution"], "courroie de distribution usee"),

    (["courroie de distribution", "cassee"], "courroie de distribution cassee"),
    (["moteur", "cale", "brutalement"], "courroie de distribution cassee"),
    (["moteur", "s arrete", "soudainement", "bruit"], "courroie de distribution cassee"),
    (["bruit", "fort", "moteur", "arret"], "courroie de distribution cassee"),

    (["capteur", "vilebrequin"], "capteur de vilebrequin defectueux"),
    (["moteur", "demarre pas", "intermittent"], "capteur de vilebrequin defectueux"),
    (["calage", "perdu"], "capteur de vilebrequin defectueux"),

    (["capteur", "regime"], "capteur de regime moteur defaillant"),
    (["compte tours", "erratique"], "capteur de regime moteur defaillant"),
    (["regime moteur", "instable", "capteur"], "capteur de regime moteur defaillant"),

    (["voyant", "moteur", "allume"], "calculateur moteur defaillant"),
    (["voyant moteur"], "calculateur moteur defaillant"),
    (["voyant orange", "moteur"], "calculateur moteur defaillant"),

    (["mode degrade"], "calculateur moteur en mode degrade"),
    (["perte", "puissance", "brutale"], "calculateur moteur en mode degrade"),
    (["voiture", "bride"], "calculateur moteur en mode degrade"),
    (["acceleration", "limitee"], "calculateur moteur en mode degrade"),

    # =========================================================
    # ECHAPPEMENT
    # =========================================================
    (["odeur", "oeuf"], "catalyseur defectueux"),
    (["odeur", "soufre"], "catalyseur defectueux"),
    (["odeur", "oeuf pourri"], "catalyseur defectueux"),

    (["bruit", "echappement"], "silencieux perce"),
    (["echappement", "perce"], "silencieux perce"),
    (["voiture", "bruyante", "pot"], "silencieux perce"),
    (["pot d echappement", "bruit"], "silencieux perce"),
    (["bruit", "grondement", "moteur"], "silencieux perce"),

    # =========================================================
    # EMBRAYAGE / BOITE
    # =========================================================
    (["embrayage", "patine"], "embrayage use"),
    (["embrayage", "glisse"], "embrayage use"),
    (["regime", "monte", "vitesse n avance pas"], "embrayage use"),
    (["odeur", "brule", "embrayage"], "embrayage use"),

    (["embrayage", "sifflement"], "butee d embrayage defectueuse"),
    (["pedale embrayage", "sifflement"], "butee d embrayage defectueuse"),
    (["bruit", "pedale embrayage"], "butee d embrayage defectueuse"),

    (["embrayage", "cable"], "cable ou circuit d embrayage casse"),
    (["pedale embrayage", "molle"], "cable ou circuit d embrayage casse"),
    (["pedale embrayage", "bloquee"], "cable ou circuit d embrayage casse"),
    (["pedale embrayage", "au plancher"], "cable ou circuit d embrayage casse"),

    (["boite automatique", "huile"], "huile de boite automatique usee"),
    (["boite automatique", "a coups"], "huile de boite automatique usee"),
    (["boite auto", "secousses"], "huile de boite automatique usee"),
    (["passage de vitesse", "brutal"], "huile de boite automatique usee"),

    # =========================================================
    # CLIMATISATION
    # =========================================================
    (["clim", "chaud"], "compresseur de climatisation en panne"),
    (["climatisation", "chaud"], "compresseur de climatisation en panne"),
    (["clim", "marche pas"], "compresseur de climatisation en panne"),
    (["climatisation", "fonctionne pas"], "compresseur de climatisation en panne"),
    (["clim", "souffle chaud"], "compresseur de climatisation en panne"),

    (["clim", "faible"], "gaz climatisation manquant"),
    (["clim", "froid pas assez"], "gaz climatisation manquant"),
    (["climatisation", "pas assez froide"], "gaz climatisation manquant"),
    (["clim", "tiede"], "gaz climatisation manquant"),

    (["filtre habitacle", "encrasse"], "filtre habitacle encrasse"),
    (["odeur", "ventilation"], "filtre habitacle encrasse"),
    (["odeur", "moisi", "voiture"], "filtre habitacle encrasse"),
    (["aeration", "faible"], "filtre habitacle encrasse"),

    (["ralenti", "instable", "clim"], "regime moteur instable avec climatisation"),
    (["moteur", "cale", "clim"], "regime moteur instable avec climatisation"),

    # =========================================================
    # ELECTRONIQUE CONFORT / SECURITE
    # =========================================================
    (["essuie glace", "marche pas"], "moteur essuie glace en panne"),
    (["essuie glace", "fonctionne pas"], "moteur essuie glace en panne"),
    (["essuie glace", "bloque"], "moteur essuie glace en panne"),

    (["leve vitre", "marche pas"], "moteur leve vitre defectueux"),
    (["vitre", "bloquee"], "moteur leve vitre defectueux"),
    (["vitre", "monte pas"], "moteur leve vitre defectueux"),
    (["vitre", "descend pas"], "moteur leve vitre defectueux"),

    (["airbag", "voyant"], "capteur airbag defectueux"),
    (["voyant airbag"], "capteur airbag defectueux"),

    (["ceinture", "bloquee"], "mecanisme retracteur bloque"),
    (["ceinture", "se retracte pas"], "mecanisme retracteur bloque"),
    (["ceinture", "coincee"], "mecanisme retracteur bloque"),

    (["abs", "voyant"], "capteur abs defectueux"),
    (["voyant abs"], "capteur abs defectueux"),

    (["vitesse", "capteur"], "capteur de vitesse defectueux"),
    (["compteur", "vitesse", "fonctionne pas"], "capteur de vitesse defectueux"),
    (["compteur", "affiche rien"], "capteur de vitesse defectueux"),

    (["verrouillage centralise", "marche pas"], "verrouillage centralise en panne"),
    (["telecommande", "marche pas"], "verrouillage centralise en panne"),
    (["portes", "verrouillent pas"], "verrouillage centralise en panne"),
    (["cle", "ouvre pas", "voiture"], "verrouillage centralise en panne"),

    (["portiere", "verrouille pas"], "module de verrouillage centralise defectueux"),
    (["une porte", "verrouille pas"], "module de verrouillage centralise defectueux"),

    (["retroviseur", "electrique", "marche pas"], "moteur retroviseur electrique en panne"),
    (["retroviseur", "bouge pas"], "moteur retroviseur electrique en panne"),
    (["retroviseur", "reglage", "marche pas"], "moteur retroviseur electrique en panne"),

    (["capteur", "recul"], "capteur de recul defectueux"),
    (["radar", "recul"], "capteur de recul defectueux"),
    (["aide au stationnement", "marche pas"], "capteur de recul defectueux"),
    (["bip", "recul", "marche pas"], "capteur de recul defectueux"),

    (["lave glace", "marche pas"], "pompe lave glace en panne"),
    (["lave glace", "fonctionne pas"], "pompe lave glace en panne"),
    (["jet", "eau", "marche pas"], "pompe lave glace en panne"),

    (["siege", "reglage", "marche pas"], "moteur de reglage de siege en panne"),
    (["siege electrique", "bouge pas"], "moteur de reglage de siege en panne"),
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