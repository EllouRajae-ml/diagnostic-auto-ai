import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer, util
from regles import chercher_regle

# Charger le modele qui comprend le sens des phrases (multilingue, comprend le francais)
print("Chargement du modele semantique (peut prendre quelques secondes)...")
modele_semantique = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
nlp = spacy.load("fr_core_news_sm")

# Charger les donnees
df = pd.read_csv('pannes.csv')
phrases_connues = df['symptome'].tolist()
pannes_connues = df['panne'].tolist()

# Calculer une seule fois le "sens" de toutes les phrases connues
embeddings_connus = modele_semantique.encode(phrases_connues, convert_to_tensor=True)


def diagnostiquer(phrase):
    """
    1. Essaie les regles d'abord (haute confiance)
    2. Sinon, cherche la phrase connue la plus proche en SENS
    """
    resultat_regle = chercher_regle(phrase)
    if resultat_regle:
        return resultat_regle, "regle (haute confiance)"

    embedding_phrase = modele_semantique.encode(phrase, convert_to_tensor=True)
    scores = util.cos_sim(embedding_phrase, embeddings_connus)[0]

    meilleur_index = scores.argmax().item()
    meilleur_score = scores[meilleur_index].item()
    panne_trouvee = pannes_connues[meilleur_index]

    if meilleur_score > 0.5:
        return panne_trouvee, f"IA semantique (confiance {meilleur_score*100:.0f}%)"
    else:
        return "panne non identifiee", "aucune correspondance fiable"


def diagnostiquer_multiple(phrase):
    """
    Decoupe la phrase en propositions grammaticales distinctes avec spaCy,
    puis diagnostique chaque proposition separement.
    """
    doc = nlp(phrase)
    segments = []
    segment_courant = []

    for token in doc:
        segment_courant.append(token.text)
        if token.text.lower() in ["et", "mais", "puis", "donc"] or token.text in [",", ";"]:
            texte_segment = " ".join(segment_courant[:-1]).strip()
            if len(texte_segment) > 3:
                segments.append(texte_segment)
            segment_courant = []

    if segment_courant:
        texte_segment = " ".join(segment_courant).strip()
        if len(texte_segment) > 3:
            segments.append(texte_segment)

    if not segments:
        segments = [phrase]

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