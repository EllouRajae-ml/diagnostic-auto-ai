import streamlit as st
from auth import afficher_connexion 
from ia_fallback import diagnostic_gemini
from frequences_modeles import est_panne_frequente
from diagnostic import diagnostiquer_multiple
from regles import analyser_mesures
from explications import obtenir_explication
from base_donnees import initialiser_bdd, ajouter_diagnostic, recuperer_historique, enregistrer_feedback, statistiques_fiabilite

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
    }
    .stChatInput textarea {
        background-color: #1a1a1a !important; color: white !important; border: 2px solid #FFD100 !important;
    }
    p, span, label { color: #e0e0e0 !important; }
    .logo-conteneur { display: flex; justify-content: center; margin-bottom: 0.3em; }
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
    kilometrage = st.number_input("Kilométrage", min_value=0, max_value=500000, value=0, step=1000)

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

    st.markdown("---")
    confirmes, incorrects, taux = statistiques_fiabilite()
    if confirmes + incorrects > 0:
        st.markdown(f"<p style='color:#FFD100; font-weight:bold;'>📊 Fiabilité mesurée</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:0.85em;'>{taux:.0f}% confirmés sur {confirmes+incorrects} retours</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("⚠️ Diagnostic indicatif — validation technicien requise.")

st.markdown("<h1>⬥ AutoDiag AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sous-titre'>Assistant de diagnostic pour techniciens — Dacia & Renault</p>", unsafe_allow_html=True)

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

AVATAR_ASSISTANT = "🔧"
AVATAR_USER = "🧑"

for message in st.session_state.messages:
    avatar = AVATAR_ASSISTANT if message["role"] == "assistant" else AVATAR_USER
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

def traiter_phrase(phrase):
    st.session_state.messages.append({"role": "user", "content": phrase})
    resultats = diagnostiquer_multiple(phrase)
    if not resultats or all("non identifiee" in r[1] for r in resultats):
        panne, composant, controle = diagnostic_gemini(phrase)
        reponse = f"**Diagnostic (IA avancée) : {panne}**\n\n"
        reponse += f"🔧 **Composant à vérifier :** {composant}\n\n"
        reponse += f"📋 **Contrôle recommandé :** {controle}\n\n"
        reponse += "🤖 *Analyse par IA générative — cas non couvert par la base locale.*\n"
        reponse += "\n⚠️ *Diagnostic indicatif, validation technicien requise.*"
        st.session_state.messages.append({"role": "assistant", "content": reponse})
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

    reponse += "\n⚠️ *Diagnostic indicatif, validation technicien requise.*"
    st.session_state.messages.append({"role": "assistant", "content": reponse})

    if matricule:
        panne_principale = resultats[0][1]
        id_diag = ajouter_diagnostic(matricule, modele, kilometrage, phrase, panne_principale)
        st.session_state.dernier_diagnostic_id = id_diag

if prompt := st.chat_input("Décrivez les symptômes observés..."):
    with st.chat_message("user", avatar=AVATAR_USER):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=AVATAR_ASSISTANT):
        with st.spinner("Analyse en cours..."):
            traiter_phrase(prompt)
            st.markdown(st.session_state.messages[-1]["content"])

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