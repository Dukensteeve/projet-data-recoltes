# Projet final : les récoltes agricoles

**Équipe de 5. Lancé le jeudi 29 octobre, à rendre le vendredi 6 novembre à 23 h 59.**

Une direction départementale de l'agriculture (fictive) vous confie trois ans de récoltes, de 2023 à 2025, par saison (printemps, automne), département et culture, avec la pluie tombée pendant chaque saison. Le ministère veut savoir quelles cultures pèsent le plus, où les rendements sont les meilleurs, et si la pluie explique les mauvaises années.

| Fichier | Une ligne par | Colonnes |
|---|---|---|
| `donnees/recoltes_brut.csv` | saison, département et culture | `annee`, `saison`, `departement`, `culture`, `surface_ha`, `production_t` |
| `donnees/cultures.csv` | culture | `culture`, `famille`, `rendement_moyen_t_ha`, `prix_htg_kg` |
| `donnees/pluies.csv` | année, saison et département | `annee`, `saison`, `departement`, `pluie_mm` |
| `donnees/departements.csv` | département | `departement`, `chef_lieu`, `population`, `superficie_km2` |

## Démarrer

Une seule personne accepte le projet et crée l'équipe, les quatre autres la rejoignent. Puis chacun :

```bash
cd cours-python
gh repo clone esih-classroom/projet-data-recoltes-NOM-DE-L-EQUIPE
cd projet-data-recoltes-NOM-DE-L-EQUIPE
uv sync
code .
```

## Ce qu'il faut rendre

Le fichier `donnees/recoltes_propre.csv` est le résultat attendu de `nettoyer` : il permet de commencer les analyses pendant qu'un membre de l'équipe écrit le nettoyage. `nettoyer` doit le reproduire à partir du fichier brut, sans le lire.

1. **`analyse.py`** : les 7 fonctions demandées, vérifiées par `uv run test_projet.py`. Leur consigne exacte est dans leur docstring. Ajoutez les vôtres pour le rapport.
2. **`rapport.ipynb`** : le rapport rédigé, qui répond aux questions ci-dessous avec des tableaux, des graphiques titrés et des phrases. Exécuté du début à la fin avant le dernier push.
3. **`equipe.md`** : qui a fait quoi.
4. **Une présentation de 5 minutes**, 5 diapositives au plus, le jour fixé par l'enseignant.

### Les fonctions testées

| Fonction | Ce qu'elle renvoie |
|---|---|
| `diagnostic(brut)` | Renvoie un dictionnaire : lignes, manquants (total des valeurs manquantes), doublons (lignes en double). |
| `nettoyer(brut)` | Renvoie un tableau sans doublons ni production manquante, surface et production en int, cultures et départements écrits d'une seule façon. |
| `enrichir(propre, cultures, pluies)` | Renvoie les récoltes avec la famille et le prix de la culture, la pluie de la saison, et la colonne rendement_t_ha arrondie à 2. |
| `production_par_culture(propre)` | Renvoie la production totale (tonnes) de chaque culture, de la plus grande à la plus petite. |
| `valeur_par_departement(propre, cultures)` | Renvoie la valeur de la production de chaque département, en millions de gourdes (production × 1000 × prix au kg), arrondie à 1, de la plus grande à la plus petite. |
| `correlation_pluie_rendement(propre, cultures, pluies, culture)` | Renvoie la corrélation entre la pluie de la saison et le rendement (t/ha) pour une culture, arrondie à 2 décimales. |
| `evolution_par_culture(propre)` | Renvoie le tableau culture (lignes) × année (colonnes) de la production totale, avec la colonne variation_% = (2025 / 2023 - 1) × 100 arrondie à 1, triée par variation décroissante. |

### Les questions du rapport

1. Quelles cultures pèsent le plus, en tonnes puis en valeur (gourdes) ? Le classement change-t-il ?
2. Où les rendements (tonnes par hectare) sont-ils les meilleurs, culture par culture ?
3. La pluie explique-t-elle les rendements ? Pour quelles cultures ? Montrez-le avec des nuages de points.
4. Quelles cultures progressent ou reculent entre 2023 et 2025 ?
5. Rapportez la production à la population de chaque département : quels départements produisent le plus par habitant ?

## Travailler à cinq

Proposition de répartition : un membre pour le diagnostic et `nettoyer`, un pour `enrichir` et les jointures, deux pour les analyses et les graphiques, un pour le rapport et la présentation. Chacun commite son propre travail avec son compte, et tout le monde relit le rapport. Faites `git pull` avant de commencer et avant chaque `git push`.

Ne modifiez pas `test_projet.py` ni les fichiers de `donnees/`.

## Barème proposé (sur 20)

| Élément | Points |
|---|---|
| Tests automatiques (`uv run test_projet.py`), au prorata | 6 |
| Rapport : réponses justes, graphiques lisibles (titre, axes, unités), conclusions prudentes | 8 |
| Présentation de 5 minutes | 4 |
| Commits : chaque membre commite son travail, avec des messages clairs | 2 |

## Si ça coince

| Problème | Solution |
|---|---|
| `rejected ... fetch first` au `git push` | Un coéquipier a poussé avant vous : `git pull`, puis `git push` |
| Un test dit « la fonction renvoie None » | Il reste `pass`, ou il manque `return` |
| Moins ou plus de lignes après un `merge` | Clés écrites différemment, ou clé en double à droite : comptez avant et après |
| `ModuleNotFoundError: No module named 'pandas'` | Mauvais noyau : **Select Kernel**, puis `.venv` |

Bloqué ? Écrivez un commentaire dans l'issue, avec le message d'erreur en entier.
