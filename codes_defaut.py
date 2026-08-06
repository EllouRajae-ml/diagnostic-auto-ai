import csv

def charger_codes():
    codes = {}
    with open('codes_defaut.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            codes[row['code'].upper()] = row['description']
    return codes

CODES_DEFAUT = charger_codes()

def rechercher_code(texte):
    """
    Cherche si le texte contient un code defaut valide (ex: P0301, C0035, B1200, U0001).
    Retourne (code, description) si trouve, sinon None.
    """
    texte_maj = texte.upper().strip()
    for code in CODES_DEFAUT:
        if code in texte_maj:
            return code, CODES_DEFAUT[code]
    return None