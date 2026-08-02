import streamlit as st
from diagnostic import diagnostiquer

# Configuration de la page
st.set_page_config(
    page_title="AutoDiag AI",
    page_icon="🚗",
    layout="centered"
)

# CSS personnalisé - style agent conversationnel
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 2.2em;
    }
    .sous-titre {
        text-align: center;
        color: #888888;
        margin-bottom: 2em;
        font-size: 1em;
    }
    .stChatMessage {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("<h1>🚗 AutoDiag AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sous-titre'>Assistant intelligent de diagnostic Dacia & Renault</p>", unsafe_allow_html=True)

# Initialiser l'historique de conversation (mémoire de session)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour 👋 Décrivez-moi les symptômes de votre véhicule et je vous aide à identifier la panne probable."}
    ]

# Afficher tout l'historique de conversation
for message in st.session_state.messages:
    avatar = "🚗" if message["role"] == "assistant" else "🧑"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Zone de saisie en bas (comme ChatGPT)
if prompt := st.chat_input("Décrivez le problème de votre véhicule..."):
    
    # Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    
    # Générer et afficher la réponse de l'agent
    with st.chat_message("assistant", avatar="🚗"):
        with st.spinner("Analyse en cours..."):
            panne, source = diagnostiquer(prompt)
        
        if "regle" in source:
            reponse = f"**Diagnostic : {panne}**\n\n✅ Confiance élevée — détecté par règle experte.\n\n⚠️ *Ce diagnostic est indicatif, consultez un professionnel pour confirmation.*"
        else:
            reponse = f"**Diagnostic probable : {panne}**\n\n🔎 Confiance moyenne — estimé par IA.\n\n⚠️ *Ce diagnostic est indicatif, consultez un professionnel pour confirmation.*"
        
        st.markdown(reponse)
    
    # Sauvegarder la réponse dans l'historique
    st.session_state.messages.append({"role": "assistant", "content": reponse})