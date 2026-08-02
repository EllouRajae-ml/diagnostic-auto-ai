import psycopg2
import streamlit as st
from datetime import datetime

def obtenir_connexion():
    return psycopg2.connect(st.secrets["DATABASE_URL"])

def initialiser_bdd():
    """La table est deja creee sur Supabase, rien a faire ici."""
    pass

def ajouter_diagnostic(matricule, modele, kilometrage, symptome, panne):
    conn = obtenir_connexion()
    cursor = conn.cursor()
    date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute('''
        INSERT INTO diagnostics (matricule, modele, kilometrage, symptome, panne, date_diagnostic)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
    ''', (matricule, modele, kilometrage, symptome, panne, date_actuelle))
    id_diagnostic = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return id_diagnostic

def enregistrer_feedback(id_diagnostic, feedback):
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute('UPDATE diagnostics SET feedback = %s WHERE id = %s', (feedback, id_diagnostic))
    conn.commit()
    cursor.close()
    conn.close()

def recuperer_historique(matricule):
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT kilometrage, symptome, panne, date_diagnostic, feedback
        FROM diagnostics WHERE matricule = %s ORDER BY date_diagnostic DESC
    ''', (matricule,))
    resultats = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultats

def statistiques_fiabilite():
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM diagnostics WHERE feedback = 'confirme'")
    confirmes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM diagnostics WHERE feedback = 'incorrect'")
    incorrects = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    total = confirmes + incorrects
    taux = (confirmes / total * 100) if total > 0 else 0
    return confirmes, incorrects, taux