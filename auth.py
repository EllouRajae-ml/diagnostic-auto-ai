import psycopg2
import bcrypt
import streamlit as st

def verifier_identifiants(nom_utilisateur, mot_de_passe):
    """Verifie si le couple utilisateur/mot de passe est correct."""
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
    """Cree un nouveau compte technicien. Retourne (succes, message)."""
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


def afficher_connexion():
    """Affiche connexion ET inscription, gere la session."""
    if "connecte" not in st.session_state:
        st.session_state.connecte = False
        st.session_state.nom_technicien = None

    if not st.session_state.connecte:
        st.markdown("<h1 style='color:#FFD100; text-align:center;'>⬥ AutoDiag AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#bbb;'>Espace technicien</p>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            onglet_connexion, onglet_inscription = st.tabs(["🔑 Connexion", "📝 Créer un compte"])

            with onglet_connexion:
                nom_utilisateur = st.text_input("Nom d'utilisateur", key="login_user")
                mot_de_passe = st.text_input("Mot de passe", type="password", key="login_pass")
                if st.button("Se connecter"):
                    valide, nom_complet = verifier_identifiants(nom_utilisateur, mot_de_passe)
                    if valide:
                        st.session_state.connecte = True
                        st.session_state.nom_technicien = nom_complet
                        st.rerun()
                    else:
                        st.error("Identifiants incorrects.")

            with onglet_inscription:
                nouveau_nom_complet = st.text_input("Votre nom complet", key="reg_nomcomplet")
                nouveau_utilisateur = st.text_input("Choisissez un nom d'utilisateur", key="reg_user")
                nouveau_mdp = st.text_input("Choisissez un mot de passe", type="password", key="reg_pass")
                nouveau_mdp_confirm = st.text_input("Confirmez le mot de passe", type="password", key="reg_pass2")
                if st.button("Créer mon compte"):
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
        return False

    return True