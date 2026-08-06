import re
import csv

with open('codes_bruts.txt', 'r', encoding='utf-8') as f:
    contenu = f.read()

codes_extraits = []

# Cherche les lignes du type "P0001   Description du defaut"
pattern = r'^([PBCU]\d{4})\s+(.+)$'

for ligne in contenu.split('\n'):
    ligne = ligne.strip()
    match = re.match(pattern, ligne)
    if match:
        code = match.group(1)
        description = match.group(2).strip()
        if description and "Réservé" not in description:
            codes_extraits.append((code, description))

# Ecrire dans un fichier CSV propre
with open('codes_defaut.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['code', 'description'])
    for code, description in codes_extraits:
        writer.writerow([code, description])

print(f"{len(codes_extraits)} codes extraits et sauvegardes dans codes_defaut.csv")