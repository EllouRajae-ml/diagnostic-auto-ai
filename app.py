import streamlit as st
import json

with open("solutions_completes.json", encoding="utf-8") as f:
    SOLUTIONS = json.load(f)
from codes_defaut import CODES_DEFAUT, rechercher_code
from guides_generiques import obtenir_guide_generique
from moteurs_connus import identifier_moteur
from auth import afficher_connexion
from ia_fallback import diagnostic_gemini
from frequences_modeles import est_panne_frequente
from diagnostic import diagnostiquer_multiple
from regles import analyser_mesures
from explications import obtenir_explication
from base_donnees import (
    initialiser_bdd, ajouter_diagnostic, recuperer_historique,
    enregistrer_feedback, statistiques_fiabilite, recuperer_historique_recent
)
from guides_reparation import rechercher_guide, codes_disponibles

initialiser_bdd()

st.set_page_config(page_title="AutoDiag AI", page_icon="⬥", layout="wide")

st.markdown("""
<style>
.stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
[data-testid="stBottomBlockContainer"], .block-container {
    background-color: #0a0a0a !important;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
    border-right: 3px solid #FFD100;
}
section[data-testid="stSidebar"] * { color: #f0f0f0 !important; }
h1 {
    color: #FFD100; text-align: center; font-size: 2.4em; font-weight: 900;
    letter-spacing: 1px; text-shadow: 0 4px 12px rgba(255,209,0,0.35);
}
h2, h3 { color: #FFD100 !important; }
.sous-titre { text-align: center; color: #bbbbbb; margin-bottom: 1.8em; font-size: 1.05em; }
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background-color: #1c1c1c; color: #ffffff; border: 1px solid #FFD100; border-radius: 8px;
}
.stButton button {
    background: linear-gradient(145deg, #FFD100, #d9b100); color: #0a0a0a;
    border-radius: 10px; font-weight: bold; border: none; width: 100%;
    box-shadow: 0 6px 14px rgba(255,209,0,0.3);
}
.stButton button:hover { transform: translateY(-2px); }
.stChatMessage {
    border-radius: 14px; border: 1px solid #2a2a2a;
    background: linear-gradient(145deg, #181818, #101010);
    color: #ffffff !important;
}
.stChatMessage [data-testid="stChatMessageContent"] *,
.stChatMessage p,
.stChatMessage span,
.stChatMessage li,
.stChatMessage strong,
.stMarkdownContainer *,
div[data-testid="stMarkdownContainer"] * {
    color: #ffffff !important;
}
.stChatInput textarea {
    background-color: #1a1a1a !important; color: white !important; border: 2px solid #FFD100 !important;
}
p, span, label { color: #e0e0e0 !important; }
.logo-conteneur { display: flex; justify-content: center; margin-bottom: 0.3em; }

/* --- Barre d'historique --- */
.hist-item {
    background: #161616; border: 1px solid #2a2a2a; border-radius: 8px;
    padding: 8px 10px; margin-bottom: 6px; font-size: 0.82em;
}
.hist-item .hist-panne { color: #FFD100; font-weight: 600; }
.hist-item .hist-meta { color: #888; font-size: 0.9em; }

/* --- Carte guide de reparation --- */
.guide-etape {
    background: #1a1a10; border: 1px solid #FFD100; border-radius: 8px;
    padding: 10px 12px; margin-bottom: 6px; font-size: 0.9em;
    color: #FFF8D8 !important; line-height: 1.5;
}
.guide-badge {
    display:inline-block; background:#2a2410; color:#FFD100; font-size:0.75em;
    padding:2px 9px; border-radius:10px; font-weight:600; margin-bottom:8px;
}
.guide-details {
    color: #FFF8D8 !important; background: #171711; border-left: 3px solid #FFD100;
    padding: 10px 12px; border-radius: 8px; margin-top: 6px;
}
.guide-details *, .pro-card *, .pro-section * {
    color: #ffffff !important;
}
.pro-card {
    background: linear-gradient(135deg, #1b1b1b, #0f0f0f);
    border: 1px solid #3a3a3a; border-radius: 18px;
    padding: 16px 18px; margin: 10px 0 16px 0;
    box-shadow: 0 12px 30px rgba(0,0,0,0.45);
}
.pro-title {
    color: #FFD100 !important; font-size: 1.14em; font-weight: 900; margin-bottom: 8px;
    letter-spacing: 0.3px;
}
.pro-meta {
    color: #f0f0f0 !important; font-size: 0.95em; margin-bottom: 8px;
    line-height: 1.5;
}
.pro-section {
    color: #ffffff !important; background: #1a1a13; border-left: 3px solid #FFD100;
    padding: 12px 14px; border-radius: 8px; margin: 10px 0;
    line-height: 1.6;
}
.premium-badge {
    display:inline-block; padding:4px 10px; border-radius:999px;
    font-size:0.72em; font-weight:800; margin-right:6px;
}
.premium-badge.low { background:#113d1d; color:#76ff9c; }
.premium-badge.medium { background:#3a3108; color:#ffd85c; }
.premium-badge.high { background:#451717; color:#ff8d8d; }
div[data-testid="stExpander"] > details > summary {
    background: #141414; border: 1px solid #2f2f2f; border-radius: 10px; color: #FFD100 !important;
    padding: 10px 12px;
    font-weight: 700;
}
div[data-testid="stExpander"] > details > div {
    padding: 10px 12px;
}
</style>
""", unsafe_allow_html=True)

if not afficher_connexion():
    st.stop()

LOGO_SVG = """
<svg width="75" height="75" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="grad3d" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#FFE566"/>
<stop offset="100%" style="stop-color:#D9B100"/>
</linearGradient>
</defs>
<path d="M50 8 L88 50 L50 92 L12 50 Z" fill="none" stroke="url(#grad3d)" stroke-width="6"/>
<path d="M50 28 L70 50 L50 72 L30 50 Z" fill="url(#grad3d)"/>
</svg>
"""

MODELES = ["Non precise", "Dacia Sandero", "Dacia Duster", "Dacia Logan", "Dacia Spring",
           "Renault Clio", "Renault Megane", "Renault Captur", "Renault Kadjar", "Autre"]

with st.sidebar:
    st.markdown(f"<div class='logo-conteneur'>{LOGO_SVG}</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#FFD100; text-align:center; margin-top:0;'>AutoDiag AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#999; font-size:0.85em;'>Diagnostic Dacia & Renault</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"<p style='color:#FFD100;'>👤 Connecté : {st.session_state.nom_technicien}</p>", unsafe_allow_html=True)
    if st.button("🚪 Déconnexion"):
        st.session_state.connecte = False
        st.session_state.nom_technicien = None
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='color:#FFD100; font-weight:bold;'>🔧 Fiche véhicule</p>", unsafe_allow_html=True)
    matricule = st.text_input("Matricule / Immatriculation", placeholder="Ex : 12345-A-6")
    modele = st.selectbox("Modèle du véhicule", MODELES)
    carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique", "Non précisé"])
    type_moteur = st.text_input("Code moteur / Type moteur", placeholder="Ex : K9K, H4D, TCe")
    kilometrage = st.number_input("Kilométrage", min_value=0, max_value=500000, value=0, step=1000)

    if st.button("🔧 Afficher infos moteur"):
        st.session_state.info_moteur_affiche = type_moteur
    if st.button("🛢️ Afficher notes carburant"):
        st.session_state.info_carburant_affiche = carburant

    st.markdown("---")
    utiliser_mesures = st.checkbox("Ajouter des mesures techniques")
    tension_batterie = temperature_moteur = niveau_huile = None
    if utiliser_mesures:
        tension_batterie = st.number_input("Tension batterie (V)", min_value=0.0, max_value=15.0, value=12.6, step=0.1)
        temperature_moteur = st.number_input("Température moteur (°C)", min_value=0, max_value=150, value=90, step=1)
        niveau_huile = st.number_input("Niveau d'huile (%)", min_value=0, max_value=100, value=80, step=5)

    st.markdown("---")
    if matricule and st.button("📜 Voir historique du véhicule"):
        st.session_state.afficher_historique = matricule

    # --- Guide de reparation par code panne ---
    st.markdown("---")
    st.markdown("<p style='color:#FFD100; font-weight:bold;'>📘 Guide par code panne</p>", unsafe_allow_html=True)
    code_panne = st.text_input("Code affiché sur la valise", placeholder="Ex : P0300")
    if st.button("🔎 Afficher le guide"):
        st.session_state.guide_affiche = code_panne
        # Mémorise ce code comme "dernier code discuté" pour que les questions
        # de suivi dans le chat (ex: "plus de détails ?") gardent le contexte.
        if code_panne:
            c = code_panne.strip().upper()
            if c in CODES_DEFAUT:
                st.session_state.dernier_code_discute = (c, CODES_DEFAUT[c])
    with st.expander("Codes disponibles"):
        st.caption(", ".join(codes_disponibles()))

    # --- Barre d'historique recent (tous vehicules) ---
    st.markdown("---")
    st.markdown("<p style='color:#FFD100; font-weight:bold;'>🕘 Historique récent</p>", unsafe_allow_html=True)
    derniers = recuperer_historique_recent(limite=6)
    if derniers:
        for matr, mod, panne, date, fb in derniers:
            statut = {"confirme": "✅", "incorrect": "❌"}.get(fb, "⏳")
            st.markdown(f"""
            <div class='hist-item'>
                <span class='hist-panne'>{statut} {panne}</span><br>
                <span class='hist-meta'>{matr} — {mod} — {date}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Aucun diagnostic enregistré pour le moment.")

    st.markdown("---")
    confirmes, incorrects, taux = statistiques_fiabilite()
    if confirmes + incorrects > 0:
        st.markdown(f"<p style='color:#FFD100; font-weight:bold;'>📊 Fiabilité mesurée</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:0.85em;'>{taux:.0f}% confirmés sur {confirmes+incorrects} retours</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("⚠️ Diagnostic indicatif — validation technicien requise.")

st.markdown("<h1>⬥ AutoDiag AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sous-titre'>Assistant de diagnostic pour techniciens — Dacia & Renault</p>", unsafe_allow_html=True)

if "info_moteur_affiche" in st.session_state and st.session_state.info_moteur_affiche:
    moteur = identifier_moteur(st.session_state.info_moteur_affiche)
    if moteur:
        code_moteur, details = moteur
        st.markdown(
            f"<div class='pro-card'>"
            f"<div class='pro-title'>🔧 Informations moteur — {code_moteur}</div>"
            f"<div class='pro-meta'><strong>Nom :</strong> {details['nom']}</div>"
            f"<div class='pro-meta'><strong>Usage :</strong> {details['usage']}</div>"
            f"<div class='pro-meta'><strong>Points connus :</strong></div>"
            f"<div class='pro-section'>" + "<br>".join([f"• {point}" for point in details['points_connus']]) + f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("Aucune information moteur connue pour ce code. Vérifiez le code moteur saisi.")

if "info_carburant_affiche" in st.session_state and st.session_state.info_carburant_affiche:
    carburant_actif = st.session_state.info_carburant_affiche
    if carburant_actif != "Non précisé":
        st.markdown(
            f"<div class='pro-card'>"
            f"<div class='pro-title'>🛢️ Note carburant — {carburant_actif}</div>"
            f"<div class='pro-meta'>Le type de carburant est pris en compte pour les recommandations techniques du guide local.</div>"
            f"</div>",
            unsafe_allow_html=True
        )


def _detail_guide_step(step):
    texte = (step or "").lower()
    if any(mot in texte for mot in ["cable", "câble", "faisceau", "connecteur", "broche", "fil"]):
        return (
            "Détails de contrôle : isolez le circuit, repérez le point de passage du câble ou du faisceau, "
            "inspectez la corrosion/les pinces desserrées, puis mesurez la continuité ou la tension avec un multimètre. "
            "Si la continuité est ouverte ou que le connecteur est oxydé, le câblage doit être réparé ou remplacé."
        )
    if any(mot in texte for mot in ["bougie", "bobine", "allumage", "raté"]):
        return (
            "Détails de contrôle : identifiez le cylindre concerné, vérifiez l'état de la bougie, l'écartement, puis "
            "testez la bobine par permutation avec une autre bobine. Si le défaut suit la bobine, la pièce est défectueuse."
        )
    if any(mot in texte for mot in ["injecteur", "rampe", "carburant"]):
        return (
            "Détails de contrôle : vérifiez l'alimentation de l'injecteur, sa résistance électrique, son débit et son étanchéité. "
            "Un défaut d'injection ou une pression de carburant anormale peut reproduire le même symptôme sur plusieurs cylindres."
        )
    if any(mot in texte for mot in ["sonde", "capteur", "vilebrequin", "arbre", "position"]):
        return (
            "Détails de contrôle : confirmez la localisation du capteur, vérifiez son entrefer ou sa fixation, puis mesurez "
            "sa tension ou sa résistance selon le type de capteur. Une valeur incohérente ou un signal instable est un indice fort de panne."
        )
    if any(mot in texte for mot in ["masse", "alimentation", "fusible", "tension"]):
        return (
            "Détails de contrôle : testez la tension d'alimentation au contact, vérifiez la présence de masse correcte "
            "et confirmez l'état du fusible et du relais associé. Une alimentation ou une masse insuffisante peut simuler un défaut du composant."
        )
    return (
        "Détails de contrôle : localisez précisément le composant, vérifiez son alimentation, sa masse, sa continuité, "
        "puis confirmez l'état mécanique ou électrique avant remplacement."
    )


def _afficher_etapes_guide(guide):
    if not guide:
        return

    etapes = guide.get("etapes", []) if isinstance(guide, dict) else guide
    if not etapes:
        return

    for index, etape in enumerate(etapes, 1):
        if isinstance(etape, dict):
            titre = f"{index}. {etape.get('titre', 'Étape')}"
            instruction = etape.get('instruction', '')
            contenu = f"{instruction}\n\n{_detail_guide_step(instruction)}"
        else:
            titre = f"{index}. {etape}"
            contenu = _detail_guide_step(etape)

        with st.expander(titre, expanded=False):
            st.markdown(f"<div class='guide-details'>{contenu}</div>", unsafe_allow_html=True)


if matricule:
    if st.button("📜 Historique du véhicule", key="btn_historique_principal"):
        st.session_state.afficher_historique = matricule
else:
    st.info("Saisissez un matricule pour afficher l'historique du véhicule.")

# --- Affichage du guide de reparation si un code a ete recherche ---
if "guide_affiche" in st.session_state and st.session_state.guide_affiche:
    guide = rechercher_guide(st.session_state.guide_affiche, modele=modele)
    st.subheader(f"📘 Guide de réparation — {st.session_state.guide_affiche.strip().upper()}")
    if guide:
        st.markdown(f"<span class='guide-badge'>Gravité : {guide['gravite'].upper()}</span>", unsafe_allow_html=True)
        st.markdown(f"**{guide['titre']}**")
        _afficher_etapes_guide(guide)
        st.caption("⚠️ Procédure indicative — se référer à la revue technique constructeur pour les valeurs précises (couples, tolérances, références pièces).")
    else:
        st.warning(f"Aucun guide enregistré pour le code « {st.session_state.guide_affiche} ». "
                   f"Codes disponibles : {', '.join(codes_disponibles())}")
    st.markdown("---")

if "afficher_historique" in st.session_state and st.session_state.afficher_historique:
    hist = recuperer_historique(st.session_state.afficher_historique)
    st.subheader(f"📜 Historique — {st.session_state.afficher_historique}")
    if hist:
        for km, symptome, panne, date, fb in hist:
            statut = {"confirme": "✅", "incorrect": "❌"}.get(fb, "⏳")
            st.markdown(f"{statut} **{date}** — {km} km — *{symptome}* → **{panne}**")
        st.markdown("---")
    else:
        st.info("Aucun historique pour ce véhicule.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour 👋 Renseignez le matricule et le modèle du véhicule, puis décrivez les symptômes observés."}
    ]
if "dernier_diagnostic_id" not in st.session_state:
    st.session_state.dernier_diagnostic_id = None
if "dernier_code_discute" not in st.session_state:
    # Mémorise (code, description) du dernier code OBD évoqué, dans le chat
    # ou via le guide en sidebar, pour donner du contexte aux questions de
    # suivi ("plus de détails ?") qui ne redonnent pas le code explicitement.
    st.session_state.dernier_code_discute = None

AVATAR_ASSISTANT = "🔧"
AVATAR_USER = "🧑"


def _render_message(message):
    avatar = AVATAR_ASSISTANT if message["role"] == "assistant" else AVATAR_USER
    with st.chat_message(message["role"], avatar=avatar):
        if message.get("guide") and message["role"] == "assistant":
            st.markdown(
                "<div class='pro-card'>"
                "<div class='pro-title'>Diagnostic structuré</div>"
                "<div class='pro-meta'>Guide de contrôle local, sans appel externe — réponse technique et exploitable</div>"
                "</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"<div class='pro-section'>{message['content']}</div>", unsafe_allow_html=True)
            if message.get("guide"):
                guide = message["guide"]
                gravite = str(guide.get("gravite", "moyenne")).lower()
                badge = "low" if gravite in ["faible", "low"] else "medium" if gravite in ["moyenne", "medium"] else "high"
                st.markdown(
                    f"<span class='premium-badge {badge}'>{gravite.upper()}</span>",
                    unsafe_allow_html=True
                )
                _afficher_etapes_guide(guide)
        else:
            st.markdown(message["content"])


for message in st.session_state.messages:
    _render_message(message)


def traiter_phrase(phrase):
    st.session_state.messages.append({"role": "user", "content": phrase})

    # Recherche directe d'un code OBD dans la phrase
    resultat_code = rechercher_code(phrase)

    if resultat_code:
        code, description = resultat_code
        code = code.upper()
        # Mémorise ce code : les prochaines questions de suivi ("plus de
        # détails ?") sans code explicite réutiliseront ce contexte.
        st.session_state.dernier_code_discute = (code, description)
        guide = rechercher_guide(code, modele=modele)

        reponse = f"## 🔧 Code détecté : {code}\n\n"

        if description:
            reponse += f"**Description :** {description}\n\n"

        if guide:
            reponse += f"**Guide : {guide['titre']}**\n\n"
            reponse += f"**Gravité :** {guide['gravite'].upper()}\n\n"
            for i, etape in enumerate(guide["etapes"], 1):
                reponse += f"{i}. {etape}\n"
                reponse += f"   Détails : {_detail_guide_step(etape)}\n"
        else:
            reponse += "\nAucun guide détaillé trouvé pour ce code.\n"

        reponse += "\n⚠️ Validation technicien requise."
        st.session_state.messages.append({"role": "assistant", "content": reponse, "guide": guide})
        return

    resultats = diagnostiquer_multiple(phrase)

    if not resultats or all("non identifiee" in r[1] for r in resultats):
        # Aucun code ni règle locale trouvés dans CE message : si un code
        # OBD était discuté juste avant (chat ou sidebar), on le rappelle
        # explicitement à l'IA pour qu'elle reste sur le même sujet au lieu
        # d'improviser une réponse hors-contexte.
        phrase_pour_ia = phrase
        dernier = st.session_state.get("dernier_code_discute")
        if dernier:
            dernier_code, dernier_description = dernier
            phrase_pour_ia = (
                f"(Contexte de la conversation en cours : on discutait du code défaut "
                f"{dernier_code} - {dernier_description}. La question suivante du technicien "
                f"porte sur ce même code, sauf si elle mentionne explicitement autre chose.)\n\n"
                f"Question du technicien : {phrase}"
            )

        panne, composant, solution, guide = diagnostic_gemini(phrase_pour_ia, modele=modele)
        reponse = f"**Solution technique recommandée : {panne}**\n\n"
        reponse += f"🔧 **Composant ciblé :** {composant}\n\n"
        reponse += f"✅ **Action directe :** {solution}\n\n"
        reponse += "🧠 *Fallback technique local, basé sur la base savoir-faire du projet.*\n"

        info_moteur = None
        if "type_moteur" in globals():
            info_moteur = identifier_moteur(type_moteur)

        if info_moteur:
            code_moteur, details = info_moteur
            reponse += f"\n**🔧 Points connus sur ce moteur ({code_moteur} — {details['nom']}) :**\n"
            for point in details['points_connus']:
                reponse += f"- {point}\n"
            reponse += "\n⚠️ *Diagnostic indicatif, validation technicien requise.*"

        st.session_state.messages.append({"role": "assistant", "content": reponse, "guide": guide})
        if matricule:
            ajouter_diagnostic(matricule, modele, kilometrage, phrase, panne)
        return

    if len(resultats) == 1:
        seg, panne, source = resultats[0]
        exp = obtenir_explication(panne)
        confiance = "✅ Confiance élevée — règle experte" if "regle" in source else f"🔎 {source}"
        reponse = f"**Diagnostic : {panne}**\n\n"
        reponse += f"🔧 **Composant à vérifier :** {exp['composant']}\n\n"
        reponse += f"📋 **Contrôle recommandé :** {exp['verification']}\n\n"
        reponse += f"{confiance}\n"
        if modele != "Non precise" and est_panne_frequente(panne, modele):
            reponse += f"\n⭐ *Panne connue comme frequente sur {modele} — diagnostic renforce.*\n"
    else:
        reponse = f"**{len(resultats)} problèmes détectés dans la description :**\n\n"
        for i, (seg, panne, source) in enumerate(resultats, 1):
            exp = obtenir_explication(panne)
            confiance = "✅ règle experte" if "regle" in source else f"🔎 {source}"
            reponse += f"**{i}. \"{seg}\" → {panne}** ({confiance})\n"
            reponse += f"   🔧 Composant : {exp['composant']}\n"
            reponse += f"   📋 Contrôle : {exp['verification']}\n\n"

    info_moteur = None
    if utiliser_mesures:
        alertes = analyser_mesures(
            tension_batterie=tension_batterie if tension_batterie != 12.6 else None,
            temperature_moteur=temperature_moteur if temperature_moteur != 90 else None,
            niveau_huile=niveau_huile if niveau_huile != 80 else None,
            kilometrage=kilometrage if kilometrage != 0 else None
        )
        if alertes:
            reponse += "\n**Alertes mesures techniques :**\n"
            for a in alertes:
                reponse += f"- {a}\n"

        if "type_moteur" in globals():
            info_moteur = identifier_moteur(type_moteur)

    if info_moteur:
        code_moteur, details = info_moteur
        reponse += f"\n**🔧 Points connus sur ce moteur ({code_moteur} — {details['nom']}) :**\n"
        for point in details['points_connus']:
            reponse += f"- {point}\n"

    reponse += "\n⚠️ *Diagnostic indicatif, validation technicien requise.*"
    st.session_state.messages.append({"role": "assistant", "content": reponse})

    if matricule:
        panne_principale = resultats[0][1]
        id_diag = ajouter_diagnostic(matricule, modele, kilometrage, phrase, panne_principale)
        st.session_state.dernier_diagnostic_id = id_diag


if prompt := st.chat_input("Décrivez les symptômes observés..."):
    with st.chat_message("user", avatar=AVATAR_USER):
        st.markdown(prompt)
    with st.spinner("Analyse en cours..."):
        traiter_phrase(prompt)
    _render_message(st.session_state.messages[-1])

# Boutons de feedback sur le dernier diagnostic
if st.session_state.dernier_diagnostic_id:
    st.markdown("---")
    st.caption("Ce diagnostic était-il correct ?")
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("✅ Confirmé"):
            enregistrer_feedback(st.session_state.dernier_diagnostic_id, "confirme")
            st.session_state.dernier_diagnostic_id = None
            st.success("Merci, feedback enregistré !")
            st.rerun()
    with col2:
        if st.button("❌ Incorrect"):
            enregistrer_feedback(st.session_state.dernier_diagnostic_id, "incorrect")
            st.session_state.dernier_diagnostic_id = None
            st.warning("Merci, feedback enregistré.")
            st.rerun()

if "guide_code_actif" in st.session_state and st.session_state.guide_code_actif:
    guide = st.session_state.guide_code_contenu
    idx = st.session_state.etape_courante_code
    etapes = guide["etapes"]

    st.markdown("---")
    st.markdown(f"### 📖 Guide : {guide['nom']} — Code {st.session_state.guide_code_actif}")
    st.caption(f"Étape {idx + 1}/{len(etapes)}")
    if guide.get("notes_carburant"):
        for note in guide["notes_carburant"]:
            st.warning(note)

    etape = etapes[idx]
    st.markdown(f"**{etape['titre']}**")
    st.info(etape['instruction'])

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if idx > 0 and st.button("⬅️ Précédent", key="prec_code"):
            st.session_state.etape_courante_code -= 1
            st.rerun()
    with col2:
        if idx < len(etapes) - 1:
            if st.button("Suivant ➡️", key="suiv_code"):
                st.session_state.etape_courante_code += 1
                st.rerun()
        else:
            if st.button("✅ Terminer", key="fin_code"):
                st.success("Réparation marquée comme terminée !")
                st.session_state.guide_code_actif = None
                st.session_state.etape_courante_code = 0
                st.rerun()