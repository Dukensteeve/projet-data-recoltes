"""Vérifie le projet : uv run test_projet.py. Ne pas modifier : la note est calculée avec ce fichier d'origine."""

from pathlib import Path

import pandas as pd

import inspect

import analyse

DOSSIER = Path(__file__).parent / "donnees"

def forme(objet):
    if isinstance(objet, pd.DataFrame):
        valeurs = objet.round(2).astype(object).where(objet.notna(), None).values.tolist()
        return {"index": [str(i) for i in objet.index], "colonnes": [str(c) for c in objet.columns], "valeurs": valeurs}
    if isinstance(objet, pd.Series):
        valeurs = objet.round(2).astype(object).where(objet.notna(), None).tolist()
        return {"index": [str(i) for i in objet.index], "valeurs": valeurs}
    if isinstance(objet, float):
        return round(objet, 2)
    if isinstance(objet, list):
        return [str(v) for v in objet]
    return objet


def resume_nettoyage(propre):
    texte = [c for c in propre.columns if not pd.api.types.is_numeric_dtype(propre[c])]
    nombres = [c for c in propre.columns if pd.api.types.is_numeric_dtype(propre[c])]
    return {
        "forme": list(propre.shape),
        "manquants": int(propre.isna().sum().sum()),
        "doublons": int(propre.duplicated().sum()),
        "nombres": {c: round(float(propre[c].sum()), 1) for c in nombres},
        "textes": {c: sorted(propre[c].unique().tolist()) for c in texte if propre[c].nunique() <= 30},
    }


def resume_jointure(complet):
    return {"lignes": len(complet), "colonnes": sorted(str(c) for c in complet.columns), "manquants": int(complet.isna().sum().sum())}


def lire(nom):
    return pd.read_csv(DOSSIER / f"{nom}.csv")


def contexte():
    return {"brut": lire("recoltes_brut"), "propre": lire("recoltes_brut".replace("brut", "propre")), "cultures": lire("cultures"), "pluies": lire("pluies")}


ATTENDU = {'diagnostic': {'lignes': 408, 'manquants': 15, 'doublons': 18}, 'nettoyer': {'forme': [376, 6], 'manquants': 0, 'doublons': 0, 'nombres': {'annee': 761026.0, 'surface_ha': 469296.0, 'production_t': 1321756.0}, 'textes': {'saison': ['Automne', 'Printemps'], 'departement': ['Artibonite', 'Centre', "Grand'Anse", 'Nippes', 'Nord', 'Nord-Est', 'Nord-Ouest', 'Ouest', 'Sud', 'Sud-Est'], 'culture': ['Banane', 'Haricot', 'Igname', 'Maïs', 'Pois congo', 'Riz', 'Sorgho']}}, 'enrichir': {'lignes': 376, 'colonnes': ['annee', 'culture', 'departement', 'famille', 'pluie_mm', 'prix_htg_kg', 'production_t', 'rendement_moyen_t_ha', 'rendement_t_ha', 'saison', 'surface_ha'], 'manquants': 0}, 'production_par_culture': {'index': ['Banane', 'Igname', 'Riz', 'Maïs', 'Sorgho', 'Pois congo', 'Haricot'], 'valeurs': [547615, 402302, 136225, 75311, 61354, 56626, 42323]}, 'valeur_par_departement': {'index': ['Artibonite', 'Ouest', 'Sud', 'Centre', 'Nord', "Grand'Anse", 'Nord-Ouest', 'Nord-Est', 'Sud-Est', 'Nippes'], 'valeurs': [6950.0, 5429.7, 4047.4, 3666.5, 3052.0, 2663.5, 2057.7, 1815.2, 1716.9, 1167.4]}, 'correlation_pluie_rendement': 0.75, 'evolution_par_culture': {'index': ['Riz', 'Sorgho', 'Banane', 'Pois congo', 'Maïs', 'Haricot', 'Igname'], 'colonnes': ['2023', '2024', '2025', 'variation_%'], 'valeurs': [[44064, 39660, 52501, 19.1], [20478, 16785, 24091, 17.6], [182892, 166401, 198322, 8.4], [17484, 22271, 16871, -3.5], [27006, 24333, 23972, -11.2], [16081, 12159, 14083, -12.4], [161924, 130569, 109809, -32.2]]}}

MESSAGES = {'diagnostic': "diagnostic : résultat différent de l'attendu. Relisez la consigne : Renvoie un dictionnaire : lignes, manquants (total des valeurs manquantes), doublons (lignes en double).", 'nettoyer': "nettoyer : résultat différent de l'attendu. Relisez la consigne : Renvoie un tableau sans doublons ni production manquante, surface et production en int, cultures et départements écrits d'une seule façon.", 'enrichir': "enrichir : résultat différent de l'attendu. Relisez la consigne : Renvoie les récoltes avec la famille et le prix de la culture, la pluie de la saison, et la colonne rendement_t_ha arrondie à 2.", 'production_par_culture': "production_par_culture : résultat différent de l'attendu. Relisez la consigne : Renvoie la production totale (tonnes) de chaque culture, de la plus grande à la plus petite.", 'valeur_par_departement': "valeur_par_departement : résultat différent de l'attendu. Relisez la consigne : Renvoie la valeur de la production de chaque département, en millions de gourdes (production × 1000 × prix au kg), arrondie à 1, de la plus grande à la plus petite.", 'correlation_pluie_rendement': "correlation_pluie_rendement : résultat différent de l'attendu. Relisez la consigne : Renvoie la corrélation entre la pluie de la saison et le rendement (t/ha) pour une culture, arrondie à 2 décimales.", 'evolution_par_culture': "evolution_par_culture : résultat différent de l'attendu. Relisez la consigne : Renvoie le tableau culture (lignes) × année (colonnes) de la production totale, avec la colonne variation_% = (2025 / 2023 - 1) × 100 arrondie à 1, triée par variation décroissante."}


def verifier(nom, appel):
    try:
        resultat = appel(contexte())
        assert resultat is not None, "la fonction renvoie None : il reste pass, ou il manque return"
        if nom == "nettoyer":
            assert "read_csv" not in inspect.getsource(analyse.nettoyer), "nettoyer doit partir du tableau brut reçu, sans lire de fichier"
            obtenu = resume_nettoyage(resultat)
        elif nom == "enrichir":
            obtenu = resume_jointure(resultat)
        else:
            obtenu = forme(resultat)
        assert obtenu == ATTENDU[nom], MESSAGES[nom]
        print(f"  ✔ {nom}")
        return 1
    except Exception as erreur:
        print(f"  ✘ {nom} : {str(erreur) or type(erreur).__name__}")
        return 0


def main():
    total = 0
    total += verifier("diagnostic", lambda c: analyse.diagnostic(c["brut"]))
    total += verifier("nettoyer", lambda c: analyse.nettoyer(c["brut"]))
    total += verifier("enrichir", lambda c: analyse.enrichir(c["propre"], c["cultures"], c["pluies"]))
    total += verifier("production_par_culture", lambda c: analyse.production_par_culture(c["propre"]))
    total += verifier("valeur_par_departement", lambda c: analyse.valeur_par_departement(c["propre"], c["cultures"]))
    total += verifier("correlation_pluie_rendement", lambda c: analyse.correlation_pluie_rendement(c["propre"], c["cultures"], c["pluies"], "Maïs"))
    total += verifier("evolution_par_culture", lambda c: analyse.evolution_par_culture(c["propre"]))
    print(f"\nTests : {total} / 7")


if __name__ == "__main__":
    main()
