import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from regles import chercher_regle

# Charger et entrainer le modele ML (une seule fois)
df = pd.read_csv('pannes.csv')
X = df['symptome']
y = df['panne']

vectorizer = TfidfVectorizer()
X_vectorise = vectorizer.fit_transform(X)

modele = MultinomialNB()
modele.fit(X_vectorise, y)

def diagnostiquer(phrase):
    """
    Fonction principale : essaie d'abord les regles,
    sinon utilise le modele ML.
    """
    # 1. Essayer les regles d'abord
    resultat_regle = chercher_regle(phrase)
    if resultat_regle:
        return resultat_regle, "regle (haute confiance)"
    
    # 2. Sinon, utiliser le ML
    vect = vectorizer.transform([phrase])
    prediction = modele.predict(vect)[0]
    return prediction, "machine learning (confiance moyenne)"

# Tests
phrases_test = [
    "la voiture ne demarre pas et les phares sont eteints",
    "grincement quand j appuie sur la pedale de frein",
    "le moteur fume blanc et chauffe beaucoup",
    "la clim souffle de l air chaud",
    "bruit bizarre quand je tourne le volant"
]

for phrase in phrases_test:
    panne, source = diagnostiquer(phrase)
    print(f"'{phrase}'")
    print(f"  -> {panne} [{source}]")
    print()