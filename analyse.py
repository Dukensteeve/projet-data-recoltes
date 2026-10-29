"""Projet final : les récoltes agricoles.

Remplacez chaque pass par votre code. Vérifiez avec : uv run test_projet.py
Vous pouvez ajouter vos propres fonctions pour le rapport.
"""


import pandas as pd


def diagnostic(brut):
    """Renvoie un dictionnaire : lignes, manquants (total des valeurs manquantes), doublons (lignes en double)."""
    pass


def nettoyer(brut):
    """Renvoie un tableau sans doublons ni production manquante, surface et production en int, cultures et départements écrits d'une seule façon."""
    pass


def enrichir(propre, cultures, pluies):
    """Renvoie les récoltes avec la famille et le prix de la culture, la pluie de la saison, et la colonne rendement_t_ha arrondie à 2."""
    pass


def production_par_culture(propre):
    """Renvoie la production totale (tonnes) de chaque culture, de la plus grande à la plus petite."""
    pass


def valeur_par_departement(propre, cultures):
    """Renvoie la valeur de la production de chaque département, en millions de gourdes (production × 1000 × prix au kg), arrondie à 1, de la plus grande à la plus petite."""
    pass


def correlation_pluie_rendement(propre, cultures, pluies, culture):
    """Renvoie la corrélation entre la pluie de la saison et le rendement (t/ha) pour une culture, arrondie à 2 décimales."""
    pass


def evolution_par_culture(propre):
    """Renvoie le tableau culture (lignes) × année (colonnes) de la production totale, avec la colonne variation_% = (2025 / 2023 - 1) × 100 arrondie à 1, triée par variation décroissante."""
    pass
