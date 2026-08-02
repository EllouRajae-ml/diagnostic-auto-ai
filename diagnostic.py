import pandas as pd
from sentence_transformers import SentenceTransformer, util
from regles import chercher_regle

print("Chargement du modele semantique (peut prendre quelques secondes)...")
modele_semantique = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

df = pd.read_csv('pannes.csv')
phrases_connues = df['symptome'].tolist()
pannes_connues = df['panne'].tolist()

embeddings_connus = modele_semantique.encode(phrases_connues, convert_to_tensor=True)


def diagnostiquer(phrase):
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