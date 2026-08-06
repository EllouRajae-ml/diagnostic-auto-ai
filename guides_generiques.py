# Categories de diagnostic generique bases sur des mots-cles dans la description du code

CATEGORIES = [
    {
        "mots_cles": ["sonde lambda", "oxygene"],
        "nom": "Sonde Lambda / Sonde d'oxygène",
        "etapes": [
            {"titre": "Sécurité", "instruction": "Moteur froid pour la dépose, moteur chaud pour la lecture des valeurs. Contact coupé pour toute intervention sur le connecteur."},
            {"titre": "Lecture des données en temps réel", "instruction": "Connectez une valise de diagnostic sur la prise OBD, sélectionnez le menu 'paramètres moteur en temps réel', puis affichez la tension de la sonde. Valeur normale oscillante entre 0.1V et 0.9V à régime stabilisé."},
            {"titre": "Contrôle du câblage", "instruction": "Débranchez le connecteur de la sonde, contact coupé. Inspectez les broches pour dépôt de corrosion (vert/blanc) ou déformation. Testez chaque fil un par un en mode continuité (ohmmètre) entre le connecteur et le calculateur : valeur proche de 0 ohm attendue, une valeur infinie indique une coupure de fil."},
            {"titre": "Contrôle de la résistance de chauffage", "instruction": "Si le code concerne le chauffage de sonde, mesurez au multimètre (mode ohmmètre) la résistance entre les deux broches d'alimentation du chauffage, sonde débranchée. Comparez à la valeur constructeur (généralement entre 2 et 14 ohms selon modèle)."},
            {"titre": "Test de réactivité", "instruction": "Moteur chaud au ralenti, observez sur la valise la vitesse de bascule du signal de tension. Un signal qui reste figé entre 0.4V et 0.5V indique une sonde vieillie qui ne réagit plus."},
            {"titre": "Remplacement si nécessaire", "instruction": "Dévissez la sonde avec une clé à sonde lambda dédiée (souvent 22mm), appliquez un peu de graisse anti-grippante sur le filetage de la sonde neuve avant montage, serrez au couple préconisé."},
            {"titre": "Effacement et contrôle", "instruction": "Effacez le code via la valise, faites un essai routier de 10-15 minutes incluant accélérations et ralenti, puis relisez les codes pour confirmer l'absence de réapparition."}
        ]
    },
    {
        "mots_cles": ["injecteur"],
        "nom": "Circuit injecteur",
        "etapes": [
            {"titre": "Sécurité carburant", "instruction": "Contact coupé, attendez la chute de pression du circuit (quelques minutes) avant de débrancher toute durite ou connecteur d'injecteur."},
            {"titre": "Lecture des codes", "instruction": "Via la valise de diagnostic, identifiez le numéro exact du cylindre concerné (les cylindres sont numérotés depuis la distribution en général, cylindre 1 côté volant moteur ou distribution selon marque)."},
            {"titre": "Contrôle du câblage", "instruction": "Débranchez le connecteur de l'injecteur, inspectez les broches pour corrosion. Testez la continuité fil par fil jusqu'au calculateur avec un ohmmètre."},
            {"titre": "Mesure de résistance", "instruction": "Multimètre en mode ohmmètre, mesurez entre les deux broches de l'injecteur débranché. Injecteur essence classique : 12-16 ohms généralement. Injecteur diesel common-rail : souvent hors tolérance ohmmètre standard, nécessite un testeur dédié."},
            {"titre": "Test de commande", "instruction": "Reconnectez l'injecteur, utilisez une lampe test à diode (jamais une lampe à incandescence classique) branchée sur le connecteur pour vérifier la présence d'un signal de commande au démarreur."},
            {"titre": "Test de débit/étanchéité", "instruction": "Si électriquement correct, déposez l'injecteur et faites-le tester sur banc dédié (débit statique et dynamique, étanchéité au goutte-à-goutte)."},
            {"titre": "Remplacement si nécessaire", "instruction": "Remplacez avec joints toriques neufs systématiquement, sur diesel : respectez impérativement le calage/codage de l'injecteur neuf sur le calculateur (procédure valise obligatoire)."},
            {"titre": "Contrôle final", "instruction": "Effacez le code, faites un essai avec valise connectée pour observer les corrections d'injecteurs (long/short term fuel trim) en temps réel."}
        ]
    },
    {
        "mots_cles": ["capteur de vitesse", "capteur de regime", "capteur de vilebrequin", "capteur d'arbre a cames", "capteur de position"],
        "nom": "Capteur de position/vitesse",
        "etapes": [
            {"titre": "Sécurité", "instruction": "Contact coupé pour toute intervention sur le câblage du capteur."},
            {"titre": "Localisation du capteur", "instruction": "Repérez le capteur selon la description exacte du code (vilebrequin en bas de bloc moteur, arbre à cames en haut de culasse, capteur de roue près du moyeu)."},
            {"titre": "Contrôle visuel", "instruction": "Déposez le capteur si accessible facilement, inspectez son extrémité pour dépôt de limaille métallique (fréquent sur capteurs inductifs) et l'état de la cible dentée en face."},
            {"titre": "Contrôle du câblage", "instruction": "Testez la continuité du câblage entre le capteur et le calculateur en mode ohmmètre, connecteur débranché des deux côtés si accessible."},
            {"titre": "Mesure électrique", "instruction": "Capteur inductif (2 fils) : mesurez sa résistance interne au ohmmètre, généralement entre 200 et 1200 ohms selon modèle. Capteur à effet Hall (3 fils) : vérifiez la tension d'alimentation 5V ou 12V selon type, contact mis, moteur arrêté."},
            {"titre": "Vérification de l'entrefer", "instruction": "Pour un capteur inductif, utilisez une cale d'épaisseur non magnétique pour vérifier l'écart entre le capteur et la cible (généralement 0.5 à 1.5mm selon modèle)."},
            {"titre": "Remplacement si nécessaire", "instruction": "Remplacez le capteur si les mesures électriques sont hors tolérance ou si un dépôt métallique important est constaté malgré nettoyage."},
            {"titre": "Contrôle final", "instruction": "Effacez le code, démarrez le moteur et observez sur la valise la stabilité du signal de régime moteur (pas de saut ou perte de signal)."}
        ]
    },
    {
        "mots_cles": ["bobine d'allumage", "bobine d allumage", "rates d'allumage", "rates d allumage"],
        "nom": "Allumage / Ratés de combustion",
        "etapes": [
            {"titre": "Sécurité", "instruction": "Moteur froid et coupé avant toute intervention sur le système d'allumage haute tension."},
            {"titre": "Identification du cylindre", "instruction": "Le chiffre dans le code correspond au cylindre concerné (ex : P0301 = cylindre 1, P0304 = cylindre 4)."},
            {"titre": "Contrôle de la bougie", "instruction": "Déposez la bougie du cylindre concerné avec une clé à bougie. Inspectez l'électrode : dépôt noir sec = mélange trop riche, dépôt blanc = trop pauvre ou surchauffe. Vérifiez l'écartement au réglet d'épaisseur (valeur constructeur généralement 0.7-1.1mm)."},
            {"titre": "Contrôle de la bobine", "instruction": "Permutez la bobine suspectée avec celle d'un autre cylindre. Si le raté d'allumage suit la bobine (change de cylindre), la bobine est en cause."},
            {"titre": "Contrôle de l'injecteur associé", "instruction": "Si bougie et bobine sont bonnes, écoutez au stéthoscope mécanique le clic régulier de l'injecteur du même cylindre au ralenti."},
            {"titre": "Contrôle de compression", "instruction": "En dernier recours, utilisez un compressiomètre sur le cylindre concerné, bougies déposées, papillon ouvert. Comparez au cylindre voisin, un écart de plus de 15% indique un problème mécanique interne (soupape, segment)."},
            {"titre": "Remplacement de la pièce en cause", "instruction": "Remplacez le composant identifié comme défaillant après la permutation/test."},
            {"titre": "Contrôle final", "instruction": "Effacez le code, surveillez le régime au ralenti (stabilité) et l'absence de à-coups à l'accélération sur essai routier."}
        ]
    },
    {
        "mots_cles": ["communication", "reseau", "bus de communication", "can"],
        "nom": "Communication réseau (bus CAN)",
        "etapes": [
            {"titre": "Sécurité", "instruction": "Contact coupé, batterie chargée à plus de 12.4V pour ne pas fausser le diagnostic (une batterie faible peut provoquer de fausses pertes de communication)."},
            {"titre": "Lecture globale des défauts", "instruction": "Lisez les codes de tous les calculateurs du véhicule via le menu 'diagnostic multiplexé' ou 'tous systèmes' de la valise, pas seulement le calculateur qui affiche l'alerte."},
            {"titre": "Identification du module concerné", "instruction": "Repérez précisément quel calculateur ne répond plus selon le code (moteur, ABS, airbag, habitacle...)."},
            {"titre": "Contrôle de l'alimentation du module", "instruction": "Vérifiez le fusible dédié dans la boîte à fusibles moteur ou habitacle (schéma sur le couvercle de la boîte), et la présence de +après contact et de masse au connecteur du calculateur."},
            {"titre": "Contrôle du bus CAN", "instruction": "Contact coupé, débranchez la batterie, mesurez au ohmmètre entre les broches CAN-High et CAN-Low de la prise OBD : valeur attendue proche de 60 ohms (deux résistances de 120 ohms en parallèle sur le réseau)."},
            {"titre": "Contrôle des connecteurs", "instruction": "Inspectez le connecteur du calculateur concerné pour broches déformées, corrosion, ou connecteur mal enclenché."},
            {"titre": "Remplacement si nécessaire", "instruction": "Si alimentation et bus sont corrects mais le module ne répond toujours pas, le calculateur peut nécessiter un remplacement suivi d'une reprogrammation/codage."},
            {"titre": "Contrôle final", "instruction": "Rebranchez tout, effacez les codes, vérifiez via la valise que tous les modules répondent au menu 'diagnostic multiplexé'."}
        ]
    },
    {
        "mots_cles": ["airbag", "pretensionneur", "ceinture"],
        "nom": "Système de sécurité (Airbag / Prétensionneurs)",
        "etapes": [
            {"titre": "⚠️ SÉCURITÉ CRITIQUE", "instruction": "Coupez le contact, débranchez la borne négative de la batterie, isolez-la, et attendez au minimum 10 à 15 minutes (délai de décharge des condensateurs de secours) avant toute intervention."},
            {"titre": "Lecture des codes spécifiques", "instruction": "Utilisez une valise compatible diagnostic airbag (menu dédié, différent du diagnostic moteur) pour identifier précisément le composant en cause."},
            {"titre": "Contrôle visuel des connecteurs", "instruction": "Repérez les connecteurs de couleur jaune (norme sécurité airbag), vérifiez leur bon enclenchement sans les débrancher inutilement."},
            {"titre": "Contrôle de résistance des circuits squib", "instruction": "Utilisez exclusivement un ohmmètre à sécurité intrinsèque dédié airbag (jamais un multimètre standard, le courant de mesure standard peut déclencher le système)."},
            {"titre": "Intervention spécialisée", "instruction": "Toute dépose/repose d'un module airbag ou prétensionneur doit être réalisée par un technicien formé à cette habilitation spécifique, selon la procédure constructeur stricte."},
            {"titre": "Contrôle final", "instruction": "Après intervention et rebranchement de la batterie, effacez le code via la valise et vérifiez l'extinction du témoin airbag au tableau de bord après quelques secondes."}
        ]
    },
    {
        "mots_cles": ["circuit ouvert", "circuit trop bas", "circuit trop haut", "panne du circuit", "short", "court-circuit"],
        "nom": "Circuit électrique générique",
        "etapes": [
            {"titre": "Sécurité", "instruction": "Contact coupé avant toute intervention sur le câblage."},
            {"titre": "Localisation du composant", "instruction": "Identifiez le composant exact concerné d'après la description du code."},
            {"titre": "Contrôle du fusible", "instruction": "Repérez le fusible associé dans la boîte à fusibles (référence indiquée sur le schéma collé au dos du couvercle) et vérifiez visuellement le filament ou testez au multimètre en mode continuité."},
            {"titre": "Contrôle visuel du câblage", "instruction": "Suivez le faisceau du composant, cherchez des zones frottées, rongées, ou fondues, particulièrement aux points de passage (charnières de porte, passages de cloison)."},
            {"titre": "Test de continuité", "instruction": "Débranchez les deux extrémités du circuit suspecté, mesurez au ohmmètre : valeur proche de 0 ohm attendue, valeur infinie = coupure à localiser."},
            {"titre": "Test de tension/masse", "instruction": "Contact mis, multimètre en mode voltmètre, vérifiez la présence de +12V au connecteur du composant et une bonne masse (moins de 0.5V de chute entre masse composant et masse batterie)."},
            {"titre": "Remplacement du composant", "instruction": "Si câblage et alimentation sont corrects, le composant (capteur, actuateur, relais) est probablement en cause et doit être remplacé."},
            {"titre": "Contrôle final", "instruction": "Effacez le code, sollicitez le système concerné et vérifiez l'absence de réapparition du défaut."}
        ]
    },
    {
        "mots_cles": ["egr", "recyclage des gaz"],
        "nom": "Système EGR (recyclage gaz d'échappement)",
        "etapes": [
            {"titre": "Sécurité", "instruction": "Moteur froid pour éviter tout risque de brûlure lors de l'intervention sur le collecteur d'admission/échappement."},
            {"titre": "Lecture des valeurs EGR", "instruction": "Via la valise, affichez la position réelle et la position demandée de la vanne EGR en temps réel — un écart important entre les deux confirme un blocage mécanique."},
            {"titre": "Contrôle visuel de la vanne", "instruction": "Déposez la vanne EGR et inspectez le clapet pour dépôt de calamine noire compacte pouvant bloquer son mouvement (très fréquent sur diesel roulant beaucoup en ville)."},
            {"titre": "Test de commande", "instruction": "Commandez l'ouverture/fermeture de la vanne via la valise (test actionneur) et observez sa réponse physique à la main, vanne accessible."},
            {"titre": "Nettoyage ou remplacement", "instruction": "Nettoyez au produit dégommant spécifique si l'encrassement est modéré, remplacez la vanne si le moteur électrique interne est défaillant."},
            {"titre": "Contrôle du capteur de position", "instruction": "Si équipé d'un capteur de position séparé, vérifiez sa tension de sortie (généralement 0.5-4.5V) sur toute la course de la vanne."},
            {"titre": "Contrôle final", "instruction": "Effacez le code, effectuez un essai routier avec relevé en temps réel de la position EGR sous différentes charges moteur."}
        ]
    },
    {
        "mots_cles": ["embrayage", "pedale d'embrayage", "pedale embrayage"],
        "nom": "Système d'embrayage",
        "etapes": [
            {"titre": "Sécurité", "instruction": "Véhicule à l'arrêt, frein de parking serré. Pour toute dépose mécanique, véhicule sur pont élévateur, batterie débranchée."},
            {"titre": "Diagnostic du symptôme", "instruction": "Identifiez le type de problème : patinage (embrayage qui glisse en charge), broutement (à-coups au démarrage), point de patinage flou, ou pédale dure/molle."},
            {"titre": "Contrôle du niveau de commande hydraulique", "instruction": "Si commande hydraulique, vérifiez le niveau de liquide dans le réservoir dédié (souvent commun avec les freins ou séparé selon modèle). Un niveau bas indique une fuite possible au cylindre émetteur ou récepteur."},
            {"titre": "Test du point de patinage", "instruction": "Moteur tournant, en côte légère, relâchez progressivement la pédale : le point où le véhicule commence à avancer doit être net et reproductible. Un point flou ou qui recule dans la course indique une usure avancée du disque."},
            {"titre": "Contrôle de la garde de pédale", "instruction": "Sur commande mécanique par câble, vérifiez la garde (jeu libre) en haut de course de la pédale selon la valeur préconisée constructeur, réglable via l'écrou du câble."},
            {"titre": "Écoute des bruits", "instruction": "Pédale enfoncée à l'arrêt : un sifflement ou grincement indique généralement une butée d'embrayage usée. Pédale relâchée : un bruit qui disparaît au débrayage oriente vers un problème de volant moteur ou de disque."},
            {"titre": "Diagnostic de cause profonde", "instruction": "Un patinage confirmé nécessite généralement le remplacement du kit complet (disque, mécanisme, butée) plutôt qu'une pièce seule, pour éviter une nouvelle panne rapprochée."},
            {"titre": "Contrôle post-intervention", "instruction": "Après réparation ou réglage, effectuez plusieurs cycles d'embrayage à l'arrêt puis un essai routier avec accélérations progressives pour confirmer l'absence de patinage et un point de patinage net."}
        ]
    },
    {
        "mots_cles": ["boite de vitesses", "boite automatique", "transmission", "convertisseur de couple", "electrovanne de changement"],
        "nom": "Transmission / Boîte de vitesses",
        "etapes": [
            {"titre": "Sécurité", "instruction": "Véhicule à l'arrêt, frein de parking serré, sur pont si intervention mécanique nécessaire."},
            {"titre": "Identification du type de boîte", "instruction": "Déterminez le type exact : manuelle, automatique à convertisseur, robotisée (double embrayage) ou CVT — le diagnostic et les valeurs de référence diffèrent fortement selon le type."},
            {"titre": "Contrôle du niveau et de l'état d'huile", "instruction": "Vérifiez le niveau à la jauge ou au bouchon de niveau selon le type de boîte, généralement moteur chaud et à l'horizontale sur boîte automatique. Une huile brune/noire avec odeur de brûlé indique une dégradation avancée nécessitant une vidange avant tout autre diagnostic."},
            {"titre": "Lecture des codes détaillés", "instruction": "Identifiez précisément l'électrovanne, capteur ou circuit concerné via le menu 'transmission' dédié de la valise de diagnostic, distinct du menu moteur."},
            {"titre": "Observation du comportement", "instruction": "Sur boîte automatique, notez si le problème survient à un rapport précis (électrovanne suspecte) ou sur tous les rapports (problème hydraulique général ou électronique du calculateur)."},
            {"titre": "Contrôle électrique du composant", "instruction": "Débranchez le composant identifié, testez sa résistance au ohmmètre et comparez à la valeur constructeur (généralement entre 5 et 30 ohms pour une électrovanne de pression)."},
            {"titre": "Contrôle mécanique", "instruction": "Si applicable et accessible, vérifiez l'absence de grippage mécanique sur l'électrovanne ou le tiroir hydraulique associé, souvent causé par des dépôts d'huile dégradée."},
            {"titre": "Vidange si nécessaire", "instruction": "Une huile dégradée nécessite une vidange complète avec remplacement du filtre si équipé, avant de conclure à une panne purement électronique — beaucoup de codes défaut boîte automatique disparaissent après une simple vidange."},
            {"titre": "Remplacement du composant", "instruction": "Remplacez le composant défectueux identifié selon le résultat des tests électriques et mécaniques."},
            {"titre": "Contrôle final", "instruction": "Effacez le code, effectuez un essai routier sollicitant tous les rapports de vitesse (montée et descente de régime) pour confirmer l'absence de à-coups ou de patinage."}
        ]
    },
    {
        "mots_cles": ["climatisation", "compresseur", "evaporateur", "refrigerant"],
        "nom": "Système de climatisation",
        "etapes": [
            {"titre": "Sécurité", "instruction": "N'ouvrez jamais le circuit sans station de récupération de gaz réfrigérant certifiée — le rejet direct de gaz est interdit et dangereux."},
            {"titre": "Lecture des pressions", "instruction": "Connectez des manomètres HP/BP sur les prises dédiées, moteur tournant, clim en marche. Comparez aux valeurs de référence constructeur (varie selon température extérieure)."},
            {"titre": "Contrôle du niveau de gaz", "instruction": "Des pressions anormalement basses des deux côtés indiquent généralement un manque de charge de gaz."},
            {"titre": "Recherche de fuite", "instruction": "Utilisez un détecteur électronique de fuite ou un colorant UV injecté dans le circuit, à rechercher au niveau des raccords et joints avec une lampe UV."},
            {"titre": "Contrôle électrique du composant", "instruction": "Testez l'alimentation du compresseur (embrayage électromagnétique) au multimètre, contact mis, commande clim activée."},
            {"titre": "Remplacement/réparation", "instruction": "Réparez le point de fuite identifié (joint, raccord) ou remplacez le composant défectueux."},
            {"titre": "Recharge du circuit", "instruction": "Tirez au vide le circuit pendant au moins 20-30 minutes pour éliminer l'humidité, puis rechargez avec la quantité exacte de gaz préconisée par l'étiquette constructeur sous le capot."},
            {"titre": "Contrôle final", "instruction": "Vérifiez les pressions de fonctionnement et mesurez la température de soufflage à la grille centrale (objectif généralement 5-10°C)."}
        ]
    },
]

GUIDE_PAR_DEFAUT = {
    "nom": "Diagnostic électrique/mécanique standard",
    "etapes": [
        {"titre": "Sécurité", "instruction": "Contact coupé avant toute intervention sur le câblage électrique."},
        {"titre": "Lecture complète des codes", "instruction": "Relevez l'ensemble des codes présents (pas seulement celui-ci) via le menu 'tous systèmes' de la valise de diagnostic."},
        {"titre": "Recherche documentaire", "instruction": "Consultez la documentation technique constructeur (manuel de réparation MR) spécifique au modèle et à l'année exacts pour la procédure et le schéma électrique précis."},
        {"titre": "Contrôle visuel", "instruction": "Inspectez le composant identifié et son câblage pour tout dommage visible (corrosion, coupure, connecteur desserré)."},
        {"titre": "Contrôle électrique de base", "instruction": "Vérifiez dans l'ordre : fusible (continuité au ohmmètre), alimentation (+12V au voltmètre contact mis), masse (chute de tension < 0.5V), continuité du câblage."},
        {"titre": "Test du composant", "instruction": "Testez le composant selon les valeurs de référence constructeur (résistance en ohms, tension en volts, ou signal à l'oscilloscope selon le type)."},
        {"titre": "Remplacement si nécessaire", "instruction": "Remplacez le composant si les tests électriques confirment sa défaillance, avec pièce de référence équivalente."},
        {"titre": "Contrôle final", "instruction": "Effacez le code défaut via la valise et vérifiez son absence de réapparition après un essai routier représentatif."}
    ]
}


def obtenir_notes_carburant(description_code, carburant=None, adblue=False, fap=False):
    """
    Retourne des notes complementaires specifiques au type de carburant,
    a ajouter au guide generique selon le profil du vehicule.
    """
    if not carburant:
        return []

    notes = []
    desc = description_code.lower()

    if carburant == "Diesel":
        if adblue and ("egr" in desc or "nox" in desc or "scr" in desc or "reducteur" in desc):
            notes.append("🔵 **Spécifique AdBlue/SCR** : ce défaut peut être lié au système de réduction des NOx. Vérifiez le niveau et la qualité de l'AdBlue, l'état de la sonde NOx, et l'absence de cristallisation dans les injecteurs AdBlue avant de conclure à une panne EGR classique.")
        if "injecteur" in desc:
            notes.append("🔵 **Spécifique Diesel** : les injecteurs fonctionnent à très haute pression (rampe commune, jusqu'à 2000 bars). Ne jamais tester l'étanchéité moteur tournant sans équipement de protection adapté — risque de perforation cutanée par jet haute pression.")
        if fap and ("particul" in desc or "echappement" in desc or "catalyseur" in desc):
            notes.append("🔵 **Spécifique FAP Diesel** : vérifiez le niveau d'encrassement du filtre à particules via la valise avant remplacement de pièce — une régénération forcée peut suffire à résoudre le défaut.")

    elif carburant == "Essence":
        if fap and ("particul" in desc or "gpf" in desc):
            notes.append("🟢 **Spécifique FAP essence (GPF)** : équipement plus récent, souvent couplé à l'injection directe. Vérifiez la pression rail haute pression spécifique injection directe avant de conclure à une panne du filtre lui-même.")
        if "injecteur" in desc:
            notes.append("🟢 **Spécifique Essence** : si le véhicule est à injection directe (GDI/TCe/TSI...), la pression rail est nettement plus élevée (jusqu'à 350 bars) qu'en injection indirecte classique — utilisez le manomètre adapté à cette pression.")

    if carburant in ["Hybride", "Électrique"]:
        if "batterie" in desc or "tension" in desc or "haute tension" in desc:
            notes.append(f"🟠 **Spécifique {carburant}** : ne jamais intervenir sur le circuit haute tension sans habilitation électrique véhicule (B2VL/B2XL) et équipement de protection individuelle (gants isolants classe 0, VAT). Procédure de consignation obligatoire avant toute mesure.")

    return notes


def obtenir_guide_generique(description_code, carburant=None, adblue=False, fap=False):
    """
    Determine la categorie du code d'apres sa description,
    retourne le guide generique correspondant enrichi des notes carburant.
    """
    description_minuscule = description_code.lower()
    guide_trouve = GUIDE_PAR_DEFAUT
    for categorie in CATEGORIES:
        for mot_cle in categorie["mots_cles"]:
            if mot_cle in description_minuscule:
                guide_trouve = categorie
                break

    notes = obtenir_notes_carburant(description_code, carburant, adblue, fap)
    guide_final = dict(guide_trouve)
    guide_final["notes_carburant"] = notes
    return guide_final