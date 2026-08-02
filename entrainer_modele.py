import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. Charger les données
df = pd.read_csv('pannes.csv')

X = df['symptome']
y = df['panne']

# 2. Transformer le texte en nombres
vectorizer = TfidfVectorizer()
X_vectorise = vectorizer.fit_transform(X)

# 3. Entraîner sur TOUTES les données (pas de split pour l'instant)
modele = MultinomialNB()
modele.fit(X_vectorise, y)

# 4. Tester avec plusieurs phrases inventées, différentes du CSV
phrases_test = [
    "la voiture ne demarre pas et les phares sont eteints",
    "grincement quand j appuie sur la pedale de frein",
    "le moteur fume blanc et chauffe beaucoup",
    "la clim souffle de l air chaud",
    "bruit bizarre quand je tourne le volant"
]

for phrase in phrases_test:
    vect = vectorizer.transform([phrase])
    prediction = modele.predict(vect)
    print(f"'{phrase}' → {prediction[0]}")