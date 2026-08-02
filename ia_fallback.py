import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
modele_gemini = genai.GenerativeModel('gemini-1.5-flash')

@st.cache_data(ttl=86400, show_spinner=False)
def diagnostic_gemini(phrase):
    """
    Utilise Gemini pour analyser un symptome que le systeme local
    n'a pas reussi a identifier avec confiance.
    Le cache evite de rappeler l'API pour la meme phrase (24h de cache).
    """
    prompt = f"""Tu es un expert en mecanique automobile specialise Dacia et Renault.
Un client decrit ce symptome : "{phrase}"

Reponds UNIQUEMENT sous ce format exact, sans autre texte :
PANNE: [nom court de la panne probable]
COMPOSANT: [piece a verifier]
CONTROLE: [action de verification recommandee en une phrase]
"""
    try:
        reponse = modele_gemini.generate_content(prompt)
        texte = reponse.text

        panne = "non determinee"
        composant = "a identifier"
        controle = "inspection generale recommandee"

        for ligne in texte.split("\n"):
            if ligne.startswith("PANNE:"):
                panne = ligne.replace("PANNE:", "").strip()
            elif ligne.startswith("COMPOSANT:"):
                composant = ligne.replace("COMPOSANT:", "").strip()
            elif ligne.startswith("CONTROLE:"):
                controle = ligne.replace("CONTROLE:", "").strip()

        return panne, composant, controle

    except Exception as e:
        message_erreur = str(e).lower()
        if "quota" in message_erreur or "rate" in message_erreur or "429" in message_erreur:
            return (
                "quota atteint",
                "service IA temporairement indisponible",
                "Le quota gratuit journalier est atteint. Merci de reessayer plus tard ou de proceder a une inspection manuelle."
            )
        return "erreur IA", "non disponible", f"Service IA indisponible, verification manuelle recommandee."