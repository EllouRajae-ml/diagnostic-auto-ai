# Pour chaque panne : quel composant verifier, et comment/quoi controler
EXPLICATIONS = {
    "alternateur defectueux": {
        "composant": "Alternateur",
        "verification": "Mesurer la tension aux bornes batterie moteur tourne (doit etre 13.7-14.7V). Verifier l'etat de la courroie d'alternateur et les charbons."
    },
    "batterie a plat": {
        "composant": "Batterie 12V",
        "verification": "Mesurer la tension au repos (doit etre 12.4-12.7V). Verifier les cosses et tester la charge avec un chargeur externe."
    },
    "batterie faible ou usee": {
        "composant": "Batterie 12V",
        "verification": "Tester la capacite de charge avec un testeur de batterie. Si l'age depasse 4-5 ans, envisager le remplacement."
    },
    "plaquettes de frein usees": {
        "composant": "Plaquettes de frein",
        "verification": "Controler visuellement l'epaisseur des plaquettes (remplacer sous 3mm). Verifier aussi l'etat des disques."
    },
    "air dans le circuit de freinage": {
        "composant": "Circuit hydraulique de freinage",
        "verification": "Purger le circuit de freinage a chaque roue. Verifier l'absence de fuite au niveau des durites et etriers."
    },
    "disques de frein voiles": {
        "composant": "Disques de frein",
        "verification": "Mesurer le voile du disque au comparateur (tolerance generalement <0.05mm). Remplacer si deforme."
    },
    "etrier de frein grippe": {
        "composant": "Etrier de frein",
        "verification": "Verifier le retour du piston d'etrier apres relachement de la pedale. Controler l'etat des glissieres et graisser ou remplacer."
    },
    "bougies usees": {
        "composant": "Bougies d'allumage",
        "verification": "Deposer et inspecter l'ecartement des electrodes et l'etat visuel (depot noir = trop riche, blanc = trop pauvre). Remplacer selon preconisation constructeur."
    },
    "bobine d allumage defectueuse": {
        "composant": "Bobine d'allumage",
        "verification": "Tester la resistance de la bobine au multimetre ou effectuer un test de permutation entre cylindres pour isoler la bobine en cause."
    },
    "court circuit electrique": {
        "composant": "Circuit electrique (a localiser)",
        "verification": "Controler les fusibles grilles, inspecter le faisceau electrique pour cables denudes ou rongés. Utiliser un multimetre en mode continuite."
    },
    "ampoule de clignotant grillee": {
        "composant": "Ampoule de clignotant",
        "verification": "Verifier visuellement le filament de l'ampoule. Remplacer par une ampoule de meme reference."
    },
    "moteur essuie glace en panne": {
        "composant": "Moteur d'essuie-glace",
        "verification": "Verifier le fusible dedie, tester l'alimentation electrique au moteur. Controler la timonerie mecanique."
    },
    "moteur leve vitre defectueux": {
        "composant": "Moteur leve-vitre",
        "verification": "Verifier le fusible, tester l'alimentation au connecteur du moteur. Controler le mecanisme (cable ou ciseaux) pour blocage mecanique."
    },
    "pneus desequilibres": {
        "composant": "Pneumatiques / roues",
        "verification": "Effectuer un equilibrage des 4 roues sur machine dediee. Verifier l'absence de masse d'equilibrage manquante."
    },
    "parallelisme desregle": {
        "composant": "Geometrie / parallelisme",
        "verification": "Controler le parallelisme sur banc de geometrie. Inspecter aussi rotules et biellettes de direction avant reglage."
    },
    "fuite lente pneu": {
        "composant": "Pneumatique",
        "verification": "Immerger la roue dans l'eau pour localiser la fuite, ou verifier la valve et le joint de jante. Controler la presence de corps etranger."
    },
    "fuite liquide de refroidissement": {
        "composant": "Circuit de refroidissement",
        "verification": "Inspecter visuellement durites, radiateur et pompe a eau. Effectuer un test de pression du circuit pour localiser la fuite."
    },
    "pompe a eau defectueuse": {
        "composant": "Pompe a eau",
        "verification": "Verifier le jeu de la pompe et une eventuelle fuite au niveau de l'axe. Controler la temperature moteur en roulant."
    },
    "capteur de temperature defaillant": {
        "composant": "Capteur de temperature moteur",
        "verification": "Lire la valeur via valise de diagnostic OBD et comparer a la temperature reelle mesuree. Remplacer si incoherence."
    },
    "joint de culasse defectueux": {
        "composant": "Joint de culasse",
        "verification": "Realiser un test de compression cylindre par cylindre et un controle du liquide de refroidissement (presence d'huile = joint HS)."
    },
    "capteur de regime moteur defaillant": {
        "composant": "Capteur de regime (vilebrequin/PMH)",
        "verification": "Lire les codes defaut via valise OBD. Tester la resistance du capteur au multimetre selon valeur constructeur."
    },
    "niveau d huile bas": {
        "composant": "Niveau d'huile moteur",
        "verification": "Controler la jauge a froid sur sol plat. Rechercher une fuite ou une consommation excessive si le niveau baisse frequemment."
    },
    "pompe a huile defectueuse": {
        "composant": "Pompe a huile",
        "verification": "Verifier la pression d'huile avec un manometre dedie au niveau du bloc moteur. Comparer a la valeur constructeur."
    },
    "segments de piston uses": {
        "composant": "Segments de piston / cylindres",
        "verification": "Realiser un test de compression et un controle de la fumee (bleue = consommation d'huile). Envisager une revision moteur."
    },
    "injecteurs encrasses": {
        "composant": "Injecteurs",
        "verification": "Effectuer un test de debit et d'etancheite des injecteurs sur banc. Un nettoyage additif ou ultrasons peut suffire."
    },
    "filtre a carburant colmate": {
        "composant": "Filtre a carburant",
        "verification": "Controler la pression de carburant en amont et en aval du filtre. Remplacer selon preconisation kilometrique."
    },
    "turbo defectueux": {
        "composant": "Turbocompresseur",
        "verification": "Verifier le jeu axial et radial de la turbine, controler les durites de suralimentation pour fuite, et la pression de suralimentation."
    },
    "melange air carburant trop riche": {
        "composant": "Systeme d'injection / sonde lambda",
        "verification": "Lire les valeurs de la sonde lambda en temps reel via valise OBD. Verifier aussi le debitmetre d'air et les injecteurs."
    },
    "rotule de direction usee": {
        "composant": "Rotule de direction (biellette)",
        "verification": "Controler le jeu de la rotule a la main (vehicule sur pont, roue en l'air). Remplacer si jeu detecte."
    },
    "pompe de direction assistee defectueuse": {
        "composant": "Pompe de direction assistee",
        "verification": "Verifier le niveau de liquide de direction assistee et la pression de la pompe. Controler l'absence de fuite."
    },
    "geometrie des roues desreglee": {
        "composant": "Geometrie / trains roulants",
        "verification": "Controler sur banc de geometrie (carrossage, chasse, parallelisme). Verifier l'etat des suspensions avant reglage."
    },
    "sonde lambda defectueuse": {
        "composant": "Sonde lambda (oxygene)",
        "verification": "Lire les valeurs en temps reel via valise OBD, comparer aux valeurs constructeur. Remplacer si reponse trop lente ou figee."
    },
    "silencieux perce": {
        "composant": "Silencieux d'echappement",
        "verification": "Inspecter visuellement la ligne d'echappement pour percage ou corrosion. Ecouter le bruit moteur tournant a l'arret."
    },
    "catalyseur defectueux": {
        "composant": "Catalyseur",
        "verification": "Controler la contre-pression d'echappement et lire les codes defaut sonde lambda associes. Verifier l'etat physique (colmatage)."
    },
    "embrayage use": {
        "composant": "Disque d'embrayage",
        "verification": "Verifier le point de patinage (embrayage qui patine en cote). Controler l'usure du disque a la depose si necessaire."
    },
    "butee d embrayage defectueuse": {
        "composant": "Butee d'embrayage",
        "verification": "Ecouter le bruit pedale embrayage enfoncee (sifflement = butee). Remplacer generalement avec le kit d'embrayage complet."
    },
    "huile de boite automatique usee": {
        "composant": "Boite de vitesses automatique",
        "verification": "Controler le niveau et la couleur de l'huile de boite (rouge/brune = a vidanger). Effectuer une vidange complete."
    },
    "amortisseurs uses": {
        "composant": "Amortisseurs",
        "verification": "Test de rebond (appuyer sur chaque coin de la voiture). Inspecter visuellement une fuite d'huile sur la tige d'amortisseur."
    },
    "ressorts de suspension fatigues": {
        "composant": "Ressorts de suspension",
        "verification": "Comparer la hauteur de caisse des 2 cotes. Inspecter visuellement une fissure ou une spire cassee."
    },
    "biellette de barre stabilisatrice cassee": {
        "composant": "Biellette de barre stabilisatrice",
        "verification": "Verifier le jeu de la biellette a la main, vehicule sur pont. Un bruit au passage de bosse confirme generalement le diagnostic."
    },
    "gaz climatisation manquant": {
        "composant": "Circuit de climatisation (gaz refrigerant)",
        "verification": "Controler la pression du circuit avec un manometre dedie. Rechercher une fuite au colorant UV avant de recharger."
    },
    "compresseur de climatisation en panne": {
        "composant": "Compresseur de climatisation",
        "verification": "Verifier l'enclenchement de l'embrayage du compresseur et l'alimentation electrique. Controler le niveau de gaz avant de conclure."
    },
    "filtre habitacle encrasse": {
        "composant": "Filtre d'habitacle (filtre pollen)",
        "verification": "Deposer et inspecter visuellement le filtre (encrassement, moisissure). Remplacer, generalement accessible sous le tableau de bord."
    },
    "capteur de vilebrequin defectueux": {
        "composant": "Capteur de position vilebrequin",
        "verification": "Lire les codes defaut via valise OBD. Tester la resistance du capteur et l'entrefer avec la cible."
    },
    "capteur airbag defectueux": {
        "composant": "Calculateur/capteur airbag",
        "verification": "Lire les codes defaut specifiques airbag via valise dediee. Ne jamais intervenir sans debrancher la batterie au prealable."
    },
    "mecanisme retracteur bloque": {
        "composant": "Retracteur de ceinture de securite",
        "verification": "Verifier le fonctionnement manuel du retracteur. Remplacer l'ensemble ceinture si le mecanisme est bloque."
    },
    "fusible klaxon grille": {
        "composant": "Fusible du circuit klaxon",
        "verification": "Localiser le fusible dans la boite a fusibles (voir notice constructeur) et le remplacer par un fusible de meme calibre."
    },
    "capteur de vitesse defectueux": {
        "composant": "Capteur de vitesse (ABS ou boite)",
        "verification": "Lire les codes defaut via valise OBD. Tester la continuite et la resistance du capteur."
    },
    "pignon du demarreur use": {
        "composant": "Pignon du demarreur (lanceur)",
        "verification": "Deposer le demarreur et inspecter visuellement l'usure des dents du pignon face a la couronne du volant moteur."
    },
    "niveau liquide de frein bas": {
        "composant": "Liquide de frein",
        "verification": "Controler le niveau au reservoir. Rechercher une fuite (usure plaquettes normale ou fuite circuit) avant de faire l'appoint."
    },
    "cable de frein a main detendu": {
        "composant": "Cable de frein a main",
        "verification": "Verifier la course du levier de frein a main (trop de course = cable detendu). Regler ou remplacer le cable."
    },
    "courroie de distribution usee": {
        "composant": "Courroie de distribution",
        "verification": "Verifier la tension et l'etat visuel (craquelures). Remplacer selon preconisation kilometrique stricte du constructeur."
    },
    "courroie de distribution cassee": {
        "composant": "Courroie de distribution",
        "verification": "URGENT — ne pas tenter de redemarrer (risque de casse moteur sur moteur avec pistons/soupapes en contact). Remorquage recommande."
    },
    "radiateur perce": {
        "composant": "Radiateur de refroidissement",
        "verification": "Inspecter visuellement les ailettes et raccords. Effectuer un test de pression pour confirmer et localiser la fuite."
    },
    "thermostat bloque": {
        "composant": "Thermostat",
        "verification": "Verifier l'ouverture du thermostat a chaud (test dans l'eau bouillante hors vehicule). Remplacer si bloque ferme."
    },
    "thermostat bloque en position ouverte": {
        "composant": "Thermostat",
        "verification": "Si la temperature ne monte jamais, le thermostat reste probablement ouvert en permanence. Remplacer la piece."
    },
    "capteur abs defectueux": {
        "composant": "Capteur ABS (roue)",
        "verification": "Lire les codes defaut via valise OBD pour identifier la roue concernee. Verifier l'etat de la couronne dentee et du capteur."
    },
    "verrouillage centralise en panne": {
        "composant": "Systeme de verrouillage centralise",
        "verification": "Verifier la pile de la telecommande, puis le fusible dedie. Tester la synchronisation de la telecommande si besoin."
    },
    "module de verrouillage centralise defectueux": {
        "composant": "Module de verrouillage centralise",
        "verification": "Tester chaque actionneur de porte individuellement. Remplacer le module central si un seul actionneur ne suffit pas a expliquer le probleme."
    },
    "moteur retroviseur electrique en panne": {
        "composant": "Moteur de retroviseur electrique",
        "verification": "Verifier le fusible dedie et l'alimentation au connecteur du retroviseur. Tester le moteur en direct si accessible."
    },
    "filtre a air encrasse": {
        "composant": "Filtre a air moteur",
        "verification": "Deposer et inspecter visuellement l'encrassement. Remplacer selon preconisation kilometrique du constructeur."
    },
    "relais de demarreur defectueux": {
        "composant": "Relais de demarreur",
        "verification": "Verifier le relais dans la boite a fusibles/relais (souvent interchangeable avec un relais identique pour tester)."
    },
    "capteur de recul defectueux": {
        "composant": "Capteur de stationnement (recul)",
        "verification": "Nettoyer les capteurs (souvent encrasses = faux positifs). Lire les codes defaut via valise si le probleme persiste."
    },
    "regime moteur instable avec climatisation": {
        "composant": "Regulation de ralenti / compresseur clim",
        "verification": "Verifier la regulation de ralenti (vanne IAC) et la sollicitation du compresseur de climatisation au demarrage."
    },
    "pompe lave glace en panne": {
        "composant": "Pompe de lave-glace",
        "verification": "Verifier le fusible dedie et l'alimentation electrique de la pompe. Controler que le reservoir n'est pas vide ou gele."
    },
    "ampoule feu de position grillee": {
        "composant": "Ampoule de feu de position",
        "verification": "Verifier visuellement le filament ou la led. Remplacer par une ampoule de meme reference."
    },
    "calculateur moteur defaillant": {
        "composant": "Calculateur moteur (ECU)",
        "verification": "Lire l'integralite des codes defaut via valise OBD. Verifier les masses electriques et connecteurs du calculateur avant remplacement."
    },
    "calculateur moteur en mode degrade": {
        "composant": "Calculateur moteur (mode securise)",
        "verification": "Lire les codes defaut ayant declenche le mode degrade via valise OBD. Traiter la cause racine avant de reinitialiser."
    },
    "fuite de courant electrique": {
        "composant": "Circuit electrique (consommateur parasite)",
        "verification": "Mesurer le courant de repos (mA) toutes portes fermees, batterie debranchee en serie avec un amperemetre. Debrancher les fusibles un par un pour isoler le circuit fautif."
    },
    "bornes de batterie corrodees": {
        "composant": "Bornes / cosses de batterie",
        "verification": "Nettoyer les cosses a la brosse metallique et verifier le serrage. Appliquer de la graisse dielectrique apres nettoyage."
    },
    "cable ou circuit d embrayage casse": {
        "composant": "Commande d'embrayage (cable ou circuit hydraulique)",
        "verification": "Verifier l'etat du cable d'embrayage ou le niveau de liquide si commande hydraulique. Rechercher une fuite au cylindre recepteur."
    },
    "moteur de reglage de siege en panne": {
        "composant": "Moteur electrique de reglage de siege",
        "verification": "Verifier le fusible dedie et l'alimentation au connecteur sous le siege. Tester le moteur en direct si accessible."
    },
}

def obtenir_explication(panne):
    """Retourne le composant et la verification recommandee pour une panne."""
    return EXPLICATIONS.get(panne, {
        "composant": "Composant a identifier",
        "verification": "Effectuer une inspection visuelle et un controle avec valise de diagnostic OBD."
    })