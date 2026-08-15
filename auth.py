import psycopg2
import bcrypt
import streamlit as st

def verifier_identifiants(nom_utilisateur, mot_de_passe):
    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute(
        "SELECT mot_de_passe_hash, nom_complet FROM techniciens WHERE nom_utilisateur = %s",
        (nom_utilisateur,)
    )
    resultat = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultat is None:
        return False, None

    hash_stocke, nom_complet = resultat
    if bcrypt.checkpw(mot_de_passe.encode(), hash_stocke.encode()):
        return True, nom_complet
    return False, None


def creer_compte(nom_utilisateur, mot_de_passe, nom_complet):
    if len(nom_utilisateur.strip()) < 3:
        return False, "Le nom d'utilisateur doit faire au moins 3 caracteres."
    if len(mot_de_passe) < 6:
        return False, "Le mot de passe doit faire au moins 6 caracteres."

    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM techniciens WHERE nom_utilisateur = %s", (nom_utilisateur,))
    if cursor.fetchone() is not None:
        cursor.close()
        conn.close()
        return False, "Ce nom d'utilisateur est deja pris."

    hash_mdp = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO techniciens (nom_utilisateur, mot_de_passe_hash, nom_complet) VALUES (%s, %s, %s)",
        (nom_utilisateur, hash_mdp.decode(), nom_complet)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Compte cree avec succes ! Vous pouvez vous connecter."


LOGO_SVG_BADGE = """
<div style="display:flex; justify-content:center; margin-bottom: 1.2em;">
  <div style="
      width:90px; height:90px; border-radius:22px;
      background: linear-gradient(145deg, #FFE566, #FFD100 55%, #D9A400);
      display:flex; align-items:center; justify-content:center;
      box-shadow: 0 10px 30px rgba(255,209,0,0.35);
  ">
    <svg width="52" height="52" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <path d="M50 8 L88 50 L50 92 L12 50 Z" fill="none" stroke="#0a0a0a" stroke-width="8"/>
      <path d="M50 28 L70 50 L50 72 L30 50 Z" fill="#0a0a0a"/>
    </svg>
  </div>
</div>
"""

LOGIN_CSS = """
<style>
.login-wrapper { max-width: 440px; margin: 0 auto; }
.login-title {
    text-align:center; color:#FFD100; font-size:2.3em; font-weight:900;
    letter-spacing: 1px; text-shadow: 0 4px 16px rgba(255,209,0,0.35);
    margin-bottom: 0.1em;
}
.login-subtitle {
    text-align:center; color:#9a9a9a; font-size:1em; margin-bottom: 1.8em;
}
.login-card {
    background: #141414; border: 1px solid #262626; border-radius: 20px;
    padding: 28px 26px 22px 26px; box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}
.login-card .stTextInput label {
    color: #e8e8e8 !important; font-weight: 600; font-size: 0.92em;
}
.login-card .stTextInput input {
    background-color: #1c1c1c !important; color: #fff !important;
    border: 1px solid #333 !important; border-radius: 10px !important;
    padding: 10px 12px !important;
}
.login-card .stButton button {
    background: linear-gradient(135deg, #FFE566, #FFD100 60%, #D9A400) !important;
    color: #0a0a0a !important; font-weight: 800 !important; font-size: 1.02em !important;
    border-radius: 12px !important; border: none !important;
    padding: 12px 0 !important; box-shadow: 0 8px 20px rgba(255,209,0,0.3) !important;
}
.login-card .stButton button:hover { transform: translateY(-1px); }
</style>
"""


def afficher_connexion():
    if "connecte" not in st.session_state:
        st.session_state.connecte = False
        st.session_state.nom_technicien = None
    if "mode_auth" not in st.session_state:
        st.session_state.mode_auth = "connexion"

    if not st.session_state.connecte:
        st.markdown(LOGIN_CSS, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='login-wrapper'>", unsafe_allow_html=True)
            st.markdown(LOGO_SVG_BADGE, unsafe_allow_html=True)
            st.markdown("<div class='login-title'>AutoDiag AI</div>", unsafe_allow_html=True)
            st.markdown("<div class='login-subtitle'>Diagnostic Dacia &amp; Renault</div>", unsafe_allow_html=True)

            st.markdown("<div class='login-card'>", unsafe_allow_html=True)

            if st.session_state.mode_auth == "connexion":
                st.markdown("<h3 style='color:#FFD100; margin-top:0;'>Connexion</h3>", unsafe_allow_html=True)

                nom_utilisateur = st.text_input("Nom d'utilisateur", key="login_user", placeholder="technicien.garage")
                mot_de_passe = st.text_input("Mot de passe", type="password", key="login_pass", placeholder="••••••")
                if st.button("Se connecter", key="btn_login", use_container_width=True):
                    valide, nom_complet = verifier_identifiants(nom_utilisateur, mot_de_passe)
                    if valide:
                        st.session_state.connecte = True
                        st.session_state.nom_technicien = nom_complet
                        st.rerun()
                    else:
                        st.error("Identifiants incorrects.")

                st.markdown("<p style='text-align:center; color:#999; margin-top:14px;'>Pas encore de compte ?</p>", unsafe_allow_html=True)
                if st.button("Créer un compte", key="switch_to_register", use_container_width=True):
                    st.session_state.mode_auth = "inscription"
                    st.rerun()

            else:
                st.markdown("<h3 style='color:#FFD100; margin-top:0;'>Créer un compte</h3>", unsafe_allow_html=True)

                nouveau_nom_complet = st.text_input("Votre nom complet", key="reg_nomcomplet", placeholder="Prénom Nom")
                nouveau_utilisateur = st.text_input("Choisissez un nom d'utilisateur", key="reg_user")
                nouveau_mdp = st.text_input("Choisissez un mot de passe", type="password", key="reg_pass")
                nouveau_mdp_confirm = st.text_input("Confirmez le mot de passe", type="password", key="reg_pass2")
                if st.button("Créer mon compte", key="btn_register", use_container_width=True):
                    if nouveau_mdp != nouveau_mdp_confirm:
                        st.error("Les mots de passe ne correspondent pas.")
                    elif not nouveau_nom_complet.strip():
                        st.error("Merci d'indiquer votre nom complet.")
                    else:
                        succes, message = creer_compte(nouveau_utilisateur, nouveau_mdp, nouveau_nom_complet)
                        if succes:
                            st.success(message)
                        else:
                            st.error(message)

                st.markdown("<p style='text-align:center; color:#999; margin-top:14px;'>Déjà un compte ?</p>", unsafe_allow_html=True)
                if st.button("Retour à la connexion", key="switch_to_login", use_container_width=True):
                    st.session_state.mode_auth = "connexion"
                    st.rerun()

            st.markdown("</div></div>", unsafe_allow_html=True)
        return False

    return True