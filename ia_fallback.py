import os
import streamlit as st
from explications import EXPLICATIONS
from guides_generiques import obtenir_guide_generique


MODELE_DETAILS = {
    "Dacia Sandero": {
        "remarque": "Sur les Sandero / Logan, privilégiez le contrôle des liaisons électrique moteur-habitacle et des connecteurs de capteurs de pression/position."
    },
    "Dacia Duster": {
        "remarque": "Sur Duster, vérifiez particulièrement la chaîne / courroie de distribution, le capteur de pression collecteur et l'état des injecteurs en cas de ratés ou de manque de puissance."
    },
    "Renault Clio": {
        "remarque": "Sur Clio, réalisez le contrôle des fusibles sous tableau, des capteurs MAF/MAP et de l'état des bobines en priorité si le symptôme touche la combustion."
    },
    "Renault Megane": {
        "remarque": "Sur Mégane, contrôlez la gestion du ralenti, les capteurs d'arbre à cames/vilebrequin et les pressions de carburant ou d'air sur les versions turbo."
    },
    "Renault Captur": {
        "remarque": "Sur Captur, vérifiez le bus CAN interne, les connecteurs de capteurs et les fusibles de modules confort/électronique en cas de défauts intermittents."
    },
    "Renault Kadjar": {
        "remarque": "Sur Kadjar, les symptômes électriques intermittents doivent être testés sur le réseau CAN et sur les modules de confort/traction avec lecture des défauts complets."
    },
}


def _taille_texte(texte):
    return len((texte or "").strip())


def _recuperer_cle_api():
    """
    Retourne (api_key, base_url, modele_llm) pour le premier fournisseur
    trouvé, dans cet ordre de priorité :
    1) OpenAI natif — OPENAI_API_KEY (st.secrets à plat, section [openai], ou env)
    2) NVIDIA (build.nvidia.com) — NVIDIA_API_KEY, API compatible OpenAI via
       une simple URL de base différente (aucune dépendance supplémentaire).

    base_url vaut None pour OpenAI natif (URL par défaut du SDK).
    """
    # 1) OpenAI — Secrets à plat
    try:
        cle = st.secrets.get("OPENAI_API_KEY")
        if cle:
            return cle.strip(), None, "gpt-4o-mini"
    except Exception:
        pass

    # 1) OpenAI — Secrets en section [openai]
    try:
        section = st.secrets.get("openai")
        if section and section.get("OPENAI_API_KEY"):
            return section.get("OPENAI_API_KEY").strip(), None, "gpt-4o-mini"
    except Exception:
        pass

    # 1) OpenAI — variable d'environnement
    cle_env = (os.getenv("OPENAI_API_KEY") or "").strip()
    if cle_env:
        return cle_env, None, "gpt-4o-mini"

    # 2) NVIDIA (build.nvidia.com) — Secrets à plat
    try:
        cle_nvidia = st.secrets.get("NVIDIA_API_KEY")
        if cle_nvidia:
            return cle_nvidia.strip(), "https://integrate.api.nvidia.com/v1", "meta/llama-3.1-70b-instruct"
    except Exception:
        pass

    # 2) NVIDIA — variable d'environnement
    cle_nvidia_env = (os.getenv("NVIDIA_API_KEY") or "").strip()
    if cle_nvidia_env:
        return cle_nvidia_env, "https://integrate.api.nvidia.com/v1", "meta/llama-3.1-70b-instruct"

    return None, None, None


def _appel_externe(phrase, modele=None, debug=False):
    """
    Appelle l'API IA (OpenAI natif, ou NVIDIA build.nvidia.com en repli —
    voir _recuperer_cle_api). Si debug=True, les erreurs sont affichées
    dans l'app via st.warning au lieu d'être avalées silencieusement.

    NB : le paramètre 'modele' est le MODÈLE DU VÉHICULE (ex: "Dacia Duster"),
    pas le modèle d'IA — celui-ci est déterminé automatiquement par
    _recuperer_cle_api() selon le fournisseur disponible.
    """
    api_key, base_url, modele_llm = _recuperer_cle_api()
    if not api_key:
        if debug:
            st.warning(
                "Aucune clé API trouvée (ni OPENAI_API_KEY, ni NVIDIA_API_KEY — "
                "ni dans st.secrets, ni en variable d'environnement). Le diagnostic "
                "va utiliser le fallback local."
            )
        return None

    try:
        from openai import OpenAI

        if base_url:
            client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            client = OpenAI(api_key=api_key)

        system_prompt = (
            "Tu es un technicien diagnostic automobile senior, spécialisé Dacia/Renault, "
            "certifié niveau atelier (type formation constructeur). Tu réponds à un autre "
            "technicien, pas à un client final : sois précis, dense, et évite les généralités. "
            "Ta réponse doit ressembler à une fiche d'intervention d'atelier, pas à un résumé grand public."
        )

        prompt = (
            f"Symptôme rapporté : {phrase or ''}\n"
            f"Véhicule : {modele or 'non précisé'}\n\n"
            "Structure ta réponse EXACTEMENT selon ces sections, avec des détails techniques concrets "
            "(valeurs numériques, plages de tolérance, codes défauts OBD-II plausibles au format Pxxxx/Bxxxx/Cxxxx/Uxxxx, "
            "noms d'outils précis) :\n\n"
            "1. PANNE PROBABLE — désignation technique précise + code(s) défaut OBD-II les plus probables associés à ce symptôme.\n"
            "2. COMPOSANT(S) CONCERNÉ(S) — nom exact du composant/système (référence fonctionnelle, pas juste 'capteur').\n"
            "3. VALEURS DE RÉFÉRENCE — valeurs attendues (tension, résistance, pression, fréquence, etc. selon le cas) "
            "avec unités et plages de tolérance constructeur typiques.\n"
            "4. PROCÉDURE DE CONTRÔLE — étapes de mesure/diagnostic dans l'ordre, avec l'outil à utiliser pour chaque étape "
            "(valise diag, multimètre, oscilloscope, manomètre, etc.) et ce qu'il faut observer exactement.\n"
            "5. CAUSES PROBABLES PAR ORDRE DE FRÉQUENCE — liste ordonnée du plus probable au moins probable.\n"
            "6. ACTION CORRECTIVE — intervention précise (remplacement, réparation, recalibrage) et points de vigilance "
            "(couple de serrage, procédure d'apprentissage/réinitialisation si nécessaire).\n"
            "7. VALIDATION — comment confirmer que la réparation a résolu le défaut (essai routier, relevé de valeurs, "
            "effacement et re-scan des codes).\n\n"
            "Réponds en français, dans un style dense et technique, sans reformulation vague, "
            "sans phrase d'introduction ni de conclusion générique."
        )

        rep = client.chat.completions.create(
            model=modele_llm,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.15,
            max_tokens=400
        )

        contenu = rep.choices[0].message.content if rep.choices else None
        if contenu:
            return contenu.strip()

        if debug:
            st.warning("L'API IA a répondu mais sans contenu exploitable.")
        return None

    except Exception as erreur:
        if debug:
            st.error(f"Erreur appel IA ({'NVIDIA' if base_url else 'OpenAI'}) : {erreur}")
        return None


def _classer_type_probleme(texte, panne):
    texte = (texte or "").lower()
    panne = (panne or "").lower()

    if any(mot in texte or mot in panne for mot in ["electrique", "circuit", "fusible", "connecteur", "court-circuit", "can", "module", "alimentation", "masse"]):
        return "electrique", "priorite_electrique"
    if any(mot in texte or mot in panne for mot in ["injecteur", "carburant", "allumage", "bobine", "rat", "combustion", "sonde lambda", "lambda"]):
        return "combustion", "priorite_combustion"
    if any(mot in texte or mot in panne for mot in ["frein", "disque", "plaquette", "embrayage", "suspension", "distribution", "courroie", "thermostat"]):
        return "mecanique", "priorite_mecanique"
    if any(mot in texte or mot in panne for mot in ["huile", "refroidissement", "liquide", "hydraulique", "fuite"]):
        return "hydraulique", "priorite_hydraulique"
    return "general", "priorite_generale"


def _est_demande_explication(texte):
    """
    Détecte si la phrase est une question / demande d'explication
    plutôt qu'un simple symptôme brut à diagnostiquer.
    Dans ce cas, on privilégie l'appel IA (plus adapté à une vraie
    réponse conversationnelle) même si un mot-clé existe en base locale.
    """
    texte = (texte or "").lower()
    mots_declencheurs = [
        "pourquoi", "comment", "explique", "expliquer", "explication",
        "détail", "détaille", "précise", "précision", "qu'est-ce",
        "que signifie", "que veut dire", "peux-tu", "plus d'info",
        "plus d'informations", "c'est quoi", "définition"
    ]
    if "?" in texte:
        return True
    return any(mot in texte for mot in mots_declencheurs)


def _note_modele(modele, panne, composant):
    modele = (modele or "").strip()
    info = MODELE_DETAILS.get(modele)
    if not info:
        return ""

    if "bobine" in panne or "allumage" in panne or "rat" in panne:
        return (
            f"Pour {modele}, le contrôle prioritaire est la bobine, le faisceau d'allumage et la bougie associée. "
            f"Vérifiez également la stabilité du signal de commande à l'oscilloscope si le défaut est intermittent."
        )

    if "injecteur" in panne or "carburant" in panne:
        return (
            f"Pour {modele}, vérifiez la pression rail/rampe, le débit injecteur et la qualité du retour carburant. "
            f"Sur les versions à injection directe, la pression doit être inspectée en temps réel avec la valise."
        )

    if "capteur" in panne or "sonde" in panne:
        return (
            f"Pour {modele}, contrôlez l'entrefer, le câblage et la tension de référence du capteur. "
            f"La valeur réelle doit être comparée à la plage constructeur du signal du {composant}."
        )

    return info["remarque"]


def _construire_guide(phrase, code_heuristique=None):
    guide = obtenir_guide_generique(code_heuristique or phrase)
    etapes = []

    for index, etape in enumerate(guide.get("etapes", []), 1):
        etapes.append(f"{index}. {etape['titre']} : {etape['instruction']}")

    if not etapes:
        return {"titre": "Guide local", "gravite": "moyenne", "etapes": []}, "Aucune procédure locale détaillée n'a été trouvée."

    return guide, "\n".join(etapes)


def _solution_directe(panne, composant, controle, modele=None):
    panneau = (panne or "").lower()
    base = (
        f"Solution la plus probable : commencez par {controle}. "
        f"Si le contrôle confirme le défaut, remplacez ou réparez le {composant} puis effacez le code et réalisez un cycle de validation."
    )

    if any(mot in panneau for mot in ["electrique", "circuit", "fusible", "connecteur", "court-circuit", "court circuit", "can", "module"]):
        return (
            f"Pour le {composant}, isolez d'abord le circuit concerné, vérifiez le fusible, l'alimentation +12V, la masse et le bon enclenchement du connecteur. "
            f"Si la continuité ou la tension est absente sur le circuit, réparez le câblage ou remplacez le module/actionneur concerné puis validez le défaut en diagnostic."
        )

    if "batterie" in panneau:
        return (
            f"Pour le {composant}, vérifiez d'abord la tension au repos, puis réalisez un test de charge. "
            f"Si la batterie est faible ou hors capacité, nettoyez les cosses, chargez la batterie, puis remplacez-la si le test de charge échoue."
        )
    if "bobine" in panneau or "allumage" in panneau or "rat" in panneau:
        return (
            f"Sur le {composant}, réalisez une permutation de bobine et contrôlez l'état de la bougie associée. "
            f"Si le raté suit la bobine, remplacez cette bobine et vérifiez le faisceau d'allumage avant une reprise sur route."
        )
    if "injecteur" in panneau or "carburant" in panneau:
        return (
            f"Contrôlez la pression rail/rampe et le débit injecteur sur le {composant}. "
            f"Si la pression est basse ou le débit incohérent, nettoyez ou remplacez l'injecteur concerné, puis testez l'étanchéité et le retour carburant."
        )
    if "capteur" in panneau or "sonde" in panneau or "vilebrequin" in panneau or "arbre" in panneau:
        return (
            f"Pour le {composant}, inspectez le câblage, l'entrefer et la tension de référence. "
            f"Si la valeur est hors plage constructeur ou le signal figé, remplacez le capteur puis effacez le défaut après validation sur route."
        )
    if "alternateur" in panneau:
        return (
            f"Vérifiez la tension à vide et sous charge sur le {composant}, puis contrôlez la courroie d'entraînement et les cosses de masse. "
            f"Si la charge est insuffisante, remplacez l'alternateur ou réparez le circuit de charge."
        )
    if "courroie" in panneau or "distribution" in panneau:
        return (
            f"Pour le {composant}, vérifiez immédiatement l'état de la courroie/chaîne, le tendeur, le calage et l'absence de craquelures. "
            f"Si le système est usé ou en mauvais calage, remplacez le kit complet, puis faites un contrôle de calage avant remise en service."
        )
    if "frein" in panneau or "plaquette" in panneau or "disque" in panneau:
        return (
            f"Pour le {composant}, contrôlez l'épaisseur des plaquettes, l'usure du disque et l'état hydraulique associé. "
            f"Si les pièces sont usées, remplacez le kit de frein adapté, purgez le circuit et validez le freinage sur route."
        )
    if "thermostat" in panneau or "refroidissement" in panneau:
        return (
            f"Pour le {composant}, vérifiez la température réelle du moteur, le thermostat et la pression du circuit de refroidissement. "
            f"Si le thermostat est bloqué ou si le circuit fuit, remplacez la pièce concernée puis refaites un contrôle de pression."
        )
    return base


@st.cache_data(ttl=86400, show_spinner=False)
def diagnostic_gemini(phrase, modele=None, debug=False):
    """
    Chemin local prioritaire (rapide, gratuit, cohérent sur les 2393 codes).
    L'appel IA externe (OpenAI) n'est déclenché que dans deux cas :
    1) aucune correspondance trouvée dans la base locale (EXPLICATIONS),
    2) la phrase saisie est une vraie question / demande d'explication
       (ex: "pourquoi...", "explique...", présence d'un "?"), auquel cas
       une réponse conversationnelle générée par l'IA est plus adaptée
       qu'une fiche de diagnostic figée.

    Passe debug=True depuis l'app (ex: une checkbox dans la sidebar)
    pour voir pourquoi l'appel externe échoue au lieu de basculer
    silencieusement sur le fallback local.
    """
    texte = (phrase or "").lower().strip()

    # 1) Recherche dans la base locale D'ABORD
    correspondance = None
    score_max = 0
    for mot_cle, donnees in EXPLICATIONS.items():
        if mot_cle in texte:
            score = _taille_texte(mot_cle)
            if score > score_max:
                score_max = score
                correspondance = (mot_cle, donnees)

    demande_explication = _est_demande_explication(texte)

    # 2) Appel IA seulement si rien trouvé localement,
    #    OU si l'utilisateur pose une vraie question / demande des explications
    if (not correspondance) or demande_explication:
        reponse_externe = _appel_externe(phrase, modele=modele, debug=debug)
        if reponse_externe:
            return "diagnostic externe", "système concerné", reponse_externe, None
        # Si l'appel IA échoue (pas de clé API, erreur réseau, quota atteint...),
        # on continue ci-dessous avec le fallback local normal, sans planter.

    panne = "panne non identifiee"
    composant = "composant a identifier"
    controle = "Vérifier le câblage, l'alimentation, la masse et le composant concerné."
    details = "Le système est à confirmer localement à partir du symptôme saisi."
    guide = None
    guide_detaille = "Aucune procédure locale détaillée n'a été trouvée."

    if correspondance:
        mot_cle, donnees = correspondance
        panne = mot_cle
        composant = donnees["composant"]
        controle = donnees["verification"]
        details = (
            f"Cause probable : le symptôme est cohérent avec un défaut sur le {composant}. "
            f"Vérifiez d'abord l'alimentation, la masse et le câblage avant toute intervention mécanique. "
            f"Le contrôle doit être mené via valise OBD, multimètre, oscilloscope ou test de continuité selon le type de composant."
        )
        guide, guide_detaille = _construire_guide(phrase, code_heuristique=mot_cle)
    else:
        panne = "diagnostic local genere"
        composant = "systeme concerné"
        controle = (
            "Inspectez visuellement le circuit concerné, vérifiez la présence de fusibles, "
            "de pannes de connecteur, de câblage endommagé, et contrôlez la tension ainsi que la masse."
        )
        details = (
            "Le symptôme saisi ne correspond pas à une fiche connue dans la base locale. "
            "Le guide ci-dessous permet de poursuivre un contrôle structuré sans appel IA externe."
        )
        guide, guide_detaille = _construire_guide(phrase, code_heuristique="diagnostic moteur")

    categorie, priorite = _classer_type_probleme(texte, panne)
    note_modele = _note_modele(modele, panne, composant)
    solution = _solution_directe(panne, composant, controle, modele=modele)

    if categorie == "electrique":
        solution = (
            f"Intervention de niveau IA locale : priorité système électrique. "
            f"Contrôlez d'abord le fusible, la tension d'alimentation, la masse, puis le connecteur/module. "
            f"{solution}"
        )
    elif categorie == "combustion":
        solution = (
            f"Intervention de niveau IA locale : priorité combustion. "
            f"Commencez par le contrôle du cylindre, de la bobine, de la bougie et de l'injection. "
            f"{solution}"
        )
    elif categorie == "mecanique":
        solution = (
            f"Intervention de niveau IA locale : priorité mécanique. "
            f"Vérifiez le jeu, l'usure des pièces et le calage mécanique avant toute pièce électrique. "
            f"{solution}"
        )
    elif categorie == "hydraulique":
        solution = (
            f"Intervention de niveau IA locale : priorité hydraulique. "
            f"Contrôlez le niveau, l'étanchéité et la pression du circuit concerné avant toute substitution de pièce. "
            f"{solution}"
        )

    # La réponse finale est construite à partir de la panne réelle identifiée
    # par la base locale, ce qui évite l'impression d'une seule et même solution.
    if note_modele:
        solution = f"{solution}\n\n{note_modele}"

    return panne, composant, solution, guide