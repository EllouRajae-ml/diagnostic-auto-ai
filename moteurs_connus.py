# Connaissances techniques generales documentees par code moteur Renault/Dacia
# Bases sur des pannes recurrentes largement connues dans la profession, pas des specs exactes par vehicule

MOTEURS_CONNUS = {
    "K9K": {
        "nom": "1.5 dCi (diesel, plusieurs puissances 65 à 115ch)",
        "usage": "Tres largement utilise sur Clio, Megane, Duster, Sandero, Logan, Captur",
        "points_connus": [
            "Injecteurs Delphi/Continental sujets à l'encrassement, surtout sur trajets courts répétés — la sonde de qualité de carburant est un point de contrôle fréquent",
            "Poulie découpleuse d'alternateur (poulie roue libre) sujette à l'usure, cause de bruit de grincement au ralenti",
            "Vanne EGR encline à l'encrassement sur usage urbain fréquent, cause fréquente de perte de puissance et voyant moteur",
            "Le remplacement de la courroie de distribution inclut généralement la pompe à eau (entraînée par la même courroie sur ce moteur) — à vérifier ensemble par précaution",
            "Volant moteur bi-masse (sur certaines versions) source de bruit métallique caractéristique en cas d'usure"
        ]
    },
    "H4D": {
        "nom": "1.0 TCe (essence turbo 3 cylindres, 90-100ch)",
        "usage": "Clio V, Captur récents",
        "points_connus": [
            "Chaîne de distribution (pas courroie) sur ce moteur — l'entretien diffère des moteurs à courroie classiques",
            "Filtre à particules essence (GPF) présent, sensible à un usage exclusivement urbain sans régénération complète",
            "Consommation d'huile parfois plus élevée que la moyenne, à surveiller entre vidanges sur les premiers modèles"
        ]
    },
    "F9Q": {
        "nom": "1.9 dCi (diesel, ancienne génération, 80-130ch)",
        "usage": "Mégane II, Scénic II, anciens modèles",
        "points_connus": [
            "Régulateur de pression Delphi connu pour des pannes causant perte de puissance ou démarrage difficile",
            "Débitmètre d'air sujet à l'encrassement, cause fréquente de fumée et perte de puissance",
            "Circuit de retour d'injecteurs (durites translucides) à vérifier en cas de fuite de gasoil ou perte de rendement"
        ]
    },
    "TCE": {
        "nom": "TCe (essence turbo, plusieurs cylindrées 90 à 150ch)",
        "usage": "Gamme large Clio, Captur, Megane, Kadjar",
        "points_connus": [
            "Turbo à géométrie fixe sur la plupart des versions, sensible à la qualité et à la fréquence de vidange d'huile",
            "Chaîne de distribution sur la majorité des versions récentes — attention à l'huile préconisée, une huile non conforme accélère l'usure de la chaîne",
            "Bougies d'allumage à changer selon intervalle strict, l'encrassement accéléré est fréquent en cas d'utilisation urbaine"
        ]
    },
    "M9R": {
        "nom": "2.0 dCi (diesel, 130-175ch)",
        "usage": "Laguna, Espace, Talisman, Koleos",
        "points_connus": [
            "Système d'injection haute pression Bosch, sensible à la qualité du carburant",
            "Vanne EGR refroidie par eau sur certaines versions, points de contrôle supplémentaires en cas de fuite de liquide de refroidissement"
        ]
    },
}


def identifier_moteur(texte_type_moteur):
    """
    Cherche si le texte saisi par le technicien correspond a un code moteur connu.
    Retourne les infos du moteur si trouve, sinon None.
    """
    if not texte_type_moteur:
        return None
    texte_maj = texte_type_moteur.upper().strip()
    for code, infos in MOTEURS_CONNUS.items():
        if code in texte_maj:
            return code, infos
    return None