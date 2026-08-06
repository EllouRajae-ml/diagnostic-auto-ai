import difflib
import re
import pandas as pd
from regles import chercher_regle

# Base locale de symptômes déjà fournie dans le projet.
# Cela évite tout appel réseau, tout téléchargement de modèle et tout timeout HF.
df = pd.read_csv('pannes.csv')
phrases_connues = df['symptome'].fillna('').astype(str).tolist()
pannes_connues = df['panne'].fillna('').astype(str).tolist()


def _normaliser(texte):
    texte = (texte or '').lower()
    texte = re.sub(r"[^a-z0-9\s]", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()
    return texte


def _score_locale(phrase, symptome_connue):
    phrase_norm = _normaliser(phrase)
    symptome_norm = _normaliser(symptome_connue)

    tokens_phrase = set(phrase_norm.split())
    tokens_connue = set(symptome_norm.split())

    if not tokens_phrase or not tokens_connue:
        return 0.0

    intersection = len(tokens_phrase & tokens_connue)
    union = len(tokens_phrase | tokens_connue)
    score_tokens = intersection / max(union, 1)
    score_similarite = difflib.SequenceMatcher(None, phrase_norm, symptome_norm).ratio()

    return 0.7 * score_tokens + 0.3 * score_similarite


def diagnostiquer(phrase):
    resultat_regle = chercher_regle(phrase)
    if resultat_regle:
        return resultat_regle, "regle (haute confiance)"

    meilleur_score = 0.0
    panne_trouvee = "panne non identifiee"
    source = "aucune correspondance locale fiable"

    for symptome_connue, panne in zip(phrases_connues, pannes_connues):
        score = _score_locale(phrase, symptome_connue)
        if score > meilleur_score:
            meilleur_score = score
            panne_trouvee = panne
            source = f"correspondance locale (score {score*100:.0f}%)"

    if meilleur_score >= 0.35:
        return panne_trouvee, source

    return "panne non identifiee", source


def diagnostiquer_multiple(phrase):
    connecteurs = [" et ", " avec ", ", ", " ainsi que ", " en plus de ", " mais ", " puis ", " donc "]
    segments = [phrase]
    for connecteur in connecteurs:
        nouveaux_segments = []
        for seg in segments:
            nouveaux_segments.extend(seg.split(connecteur))
        segments = nouveaux_segments

    segments = [s.strip() for s in segments if len(s.strip()) > 3]

    resultats = []
    pannes_vues = set()
    for seg in segments:
        panne, source = diagnostiquer(seg)
        if panne not in pannes_vues and "non identifiee" not in panne:
            resultats.append((seg, panne, source))
            pannes_vues.add(panne)

    if not resultats:
        panne, source = diagnostiquer(phrase)
        resultats.append((phrase, panne, source))

    return resultats