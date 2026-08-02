# Pannes frequemment observees par modele (a affiner avec de vraies donnees d'atelier)
PANNES_FREQUENTES_PAR_MODELE = {
    "Dacia Sandero": [
        "injecteurs encrasses", "bougies usees", "plaquettes de frein usees",
        "filtre a air encrasse", "batterie faible ou usee"
    ],
    "Dacia Duster": [
        "amortisseurs uses", "rotule de direction usee", "courroie de distribution usee",
        "capteur abs defectueux", "turbo defectueux"
    ],
    "Dacia Logan": [
        "alternateur defectueux", "embrayage use", "plaquettes de frein usees",
        "joint de culasse defectueux"
    ],
    "Dacia Spring": [
        "moteur retroviseur electrique en panne", "moteur leve vitre defectueux",
        "fuite de courant electrique"
    ],
    "Renault Clio": [
        "bobine d allumage defectueuse", "injecteurs encrasses", "amortisseurs uses",
        "capteur de vilebrequin defectueux"
    ],
    "Renault Megane": [
        "turbo defectueux", "embrayage use", "capteur abs defectueux",
        "pompe a eau defectueuse"
    ],
    "Renault Captur": [
        "batterie faible ou usee", "capteur de recul defectueux",
        "compresseur de climatisation en panne"
    ],
    "Renault Kadjar": [
        "courroie de distribution usee", "turbo defectueux", "amortisseurs uses"
    ],
}

def est_panne_frequente(panne, modele):
    """Verifie si une panne est connue comme frequente sur ce modele."""
    if modele not in PANNES_FREQUENTES_PAR_MODELE:
        return False
    return panne in PANNES_FREQUENTES_PAR_MODELE[modele]