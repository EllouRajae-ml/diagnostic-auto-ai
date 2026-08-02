import pandas as pd

# Charger le fichier CSV
df = pd.read_csv('pannes.csv')

# Afficher les 5 premières lignes
print("Aperçu des données :")
print(df.head())
print()

# Compter combien de lignes au total
print(f"Nombre total de pannes enregistrées : {len(df)}")
print()

# Voir combien de pannes différentes existent
print("Répartition par système :")
print(df['systeme'].value_counts())