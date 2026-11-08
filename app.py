
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


# Ces réglages s'appliquent à TOUS les graphiques de la page.
plt.rcParams.update({
    "axes.spines.top": False,     # enlève le trait du haut
    "axes.spines.right": False,   # enlève le trait de droite
    "axes.grid": True,            # ajoute une grille
    "grid.alpha": 0.25,           # grille discrète
    "axes.titleweight": "bold",   # titres en gras
    "axes.titlesize": 12,
    "font.size": 10,
})
VERT = "#2E7D32"
ORANGE = "#E67E22"

# 3. TITRE, CONTEXTE, SOURCE 
st.set_page_config(page_title="Récoltes agricoles", layout="wide")
st.title("Récoltes agricoles 2023-2025")
st.write(
    "Trois ans de récoltes par saison, département et culture, avec la pluie tombée. "
    "Le ministère veut savoir quelles cultures pèsent le plus, où les rendements "
    "sont les meilleurs et si la pluie explique les mauvaises années."
)
st.caption("Source : direction départementale de l'agriculture (données fictives).")


# 4. LECTURE DES DONNÉES
@st.cache_data
def charger():
    return pd.read_csv("donnees/recoltes_propre.csv")


df = charger()

#5. FILTRES (barre latérale)
st.sidebar.header("Filtres")
annee = st.sidebar.selectbox("Année", ["Toutes"] + sorted(df["annee"].unique().tolist()))
deps = st.sidebar.multiselect(
    "Départements",
    sorted(df["departement"].unique()),
    default=sorted(df["departement"].unique()),
)

filtre = df[df["departement"].isin(deps)]
if annee != "Toutes":
    filtre = filtre[filtre["annee"] == annee]

if filtre.empty:
    st.warning("Aucune donnée avec ces filtres.")
    st.stop()

# 6. INDICATEURS
c1, c2, c3 = st.columns(3)
c1.metric("Production (t)", f"{filtre['production_t'].sum():,.0f}")
c2.metric("Valeur (millions HTG)", f"{filtre['valeur_htg'].sum() / 1e6:,.0f}")
c3.metric(
    "Rendement moyen (t/ha)",
    f"{filtre['production_t'].sum() / filtre['surface_ha'].sum():.2f}",
)

#  7. LES ONGLETS
t1, t2, t3, t4, t5 = st.tabs(["Poids", "Rendements", "Pluie", "Évolution", "Par habitant"])

# ONGLET 1 : poids des cultures 
with t1:
    st.subheader("Question 1 : quelles cultures pèsent le plus ?")
    pc = filtre.groupby("culture").agg(
        tonnes=("production_t", "sum"), valeur=("valeur_htg", "sum")
    )
    pc["valeur_millions"] = pc["valeur"] / 1e6

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    pc["tonnes"].sort_values().plot.barh(ax=a1, color=VERT)
    a1.set_title("Production (tonnes)")
    a1.set_ylabel("")
    pc["valeur_millions"].sort_values().plot.barh(ax=a2, color=ORANGE)
    a2.set_title("Valeur (millions de gourdes)")
    a2.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    t, v = pc["tonnes"].idxmax(), pc["valeur_millions"].idxmax()
    if t != v:
        st.write(
            f"Le classement change : {t} est 1re en tonnes ({pc['tonnes'].max():,.0f} t), "
            f"mais {v} est 1re en valeur ({pc['valeur_millions'].max():,.0f} millions de gourdes), "
            "car elle se vend plus cher au kilo."
        )
    else:
        st.write(f"{t} est 1re en tonnes et en valeur : le classement ne change pas en tête.")

# ONGLET 2 : rendements
with t2:
    st.subheader("Question 2 : où les rendements sont-ils les meilleurs ?")
    somme = filtre.groupby(["culture", "departement"])[["production_t", "surface_ha"]].sum()
    somme["rendement"] = somme["production_t"] / somme["surface_ha"]
    tab = somme["rendement"].unstack()
    relatif = tab.div(tab.mean(axis=1), axis=0)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.grid(False)  # pas de grille sur la carte de chaleur
    im = ax.imshow(relatif, cmap="RdYlGn", aspect="auto")
    ax.set_xticks(range(len(tab.columns)))
    ax.set_xticklabels(tab.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(tab.index)))
    ax.set_yticklabels(tab.index)
    for i in range(tab.shape[0]):
        for j in range(tab.shape[1]):
            if pd.notna(tab.iloc[i, j]):
                ax.text(j, i, f"{tab.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    ax.set_title("Rendement (t/ha) par culture et département")
    plt.colorbar(im, label="Par rapport à la moyenne de la culture")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    meilleur = tab.idxmax(axis=1)
    cite = ", ".join(f"{c} : {meilleur[c]} ({tab.loc[c, meilleur[c]]:.2f})" for c in tab.index)
    st.write(f"Meilleur département par culture (t/ha) : {cite}.")

# ONGLET 3 : pluie
with t3:
    st.subheader("Question 3 : la pluie explique-t-elle les rendements ?")
    cultures = sorted(filtre["culture"].unique())
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    axes = axes.flatten()
    corr = {}
    for i, c in enumerate(cultures):
        d = filtre[filtre["culture"] == c]
        axes[i].scatter(d["pluie_mm"], d["rendement_t_ha"], s=18, color=VERT, alpha=0.7)
        axes[i].set_title(c)
        axes[i].set_xlabel("Pluie (mm)")
        axes[i].set_ylabel("t/ha")
        if len(d) > 2:
            corr[c] = d["pluie_mm"].corr(d["rendement_t_ha"])
            # droite de tendance
            z = np.polyfit(d["pluie_mm"], d["rendement_t_ha"], 1)
            x = np.linspace(d["pluie_mm"].min(), d["pluie_mm"].max(), 50)
            axes[i].plot(x, np.polyval(z, x), color=ORANGE, linewidth=2)
    for j in range(len(cultures), len(axes)):
        axes[j].axis("off")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    corr = pd.Series(corr).dropna().round(2).sort_values(ascending=False)
    if corr.empty:
        st.write("Pas assez de points avec ces filtres pour mesurer un lien.")
    else:
        st.write(
            f"La pluie va avec de meilleurs rendements : corrélation de {corr.iloc[0]} "
            f"pour {corr.index[0]} jusqu'à {corr.iloc[-1]} pour {corr.index[-1]}. "
            "C'est un lien, pas une preuve de cause."
        )

# ONGLETS 4 ET 5
with t4:
    st.info("Évolution de la production de chaque culture, de 2023 à 2025")
    # base = le tableau filtré par les filtres de l'équipe, SANS le filtre sur l'année
    base = df[df["departement"].isin(filtre["departement"].unique())]
    premiere, derniere = base["annee"].min(), base["annee"].max()

    prod = base.pivot_table(index="culture", columns="annee", values="production_t", aggfunc="sum")
    prod["variation_pct"] = ((prod[derniere] / prod[premiere] - 1) * 100).round(1)
    prod = prod.sort_values("variation_pct", ascending=False)

    st.bar_chart(prod["variation_pct"])
    st.write(
        f"4. {prod.index[0]} progresse le plus ({prod['variation_pct'].iloc[0]:+.1f} %) "
        f"et {prod.index[-1]} recule le plus ({prod['variation_pct'].iloc[-1]:+.1f} %) entre {premiere} et {derniere}.")
with t5:
    st.info("Production par habitant, par département")
    par_dep = filtre.groupby("departement").agg(
        production_t=("production_t", "sum"),
        population=("population", "first"),
    )
    nb_annees = filtre["annee"].nunique()
    par_dep["kg_par_habitant"] = (par_dep["production_t"] * 1000 / nb_annees / par_dep["population"]).round(1)
    par_dep = par_dep.sort_values("kg_par_habitant", ascending=False)

    st.bar_chart(par_dep["kg_par_habitant"])
    st.write(
        f"5. {par_dep.index[0]} produit le plus par habitant ({par_dep['kg_par_habitant'].iloc[0]} kg par an), "
        f"et {par_dep.index[-1]} le moins ({par_dep['kg_par_habitant'].iloc[-1]} kg par an).")

# 8. CONCLUSION, LIMITES ET DONNÉES FILTRÉES (étape 6)
st.divider()
st.header("Conclusion")

st.write(
    "**Ce qu'il faut retenir** (sur l'ensemble de 2023-2025, tous départements confondus) :"
)
st.markdown(
    "- **Poids** : la banane pèse le plus en tonnes (547 615 t), mais l'igname rapporte "
    "le plus en gourdes (12 069 millions de HTG), car elle se vend plus cher au kilo. "
    "Le classement change.\n"
    "- **Rendements** : aucun département n'est le meilleur partout. Chaque culture a son "
    "département en tête, et seul le Centre y est deux fois (maïs et sorgho).\n"
    "- **Pluie** : elle va avec de meilleurs rendements pour toutes les cultures "
    "(corrélations de 0,42 pour le riz à 0,76 pour le haricot et le maïs).\n"
    "- **Évolution** : l'igname recule de 32,2 % entre 2023 et 2025.\n"
    "- **Par habitant** : Grand'Anse produit le plus (81,4 kg par habitant et par an), "
    "l'Ouest le moins (16,9 kg) à cause de sa forte population."
)

st.subheader("Limites des données")
st.markdown(
    "- **Période courte** : trois ans et deux saisons seulement. Une tendance sur 2023-2025 "
    "ne dit pas ce qui se passera ensuite.\n"
    "- **Corrélation n'est pas cause** : la pluie va avec de meilleurs rendements, mais "
    "d'autres facteurs jouent (sol, semences, irrigation, techniques) et ne sont pas mesurés.\n"
    "- **Pluie moyenne** : une seule valeur par département et par saison, alors que la pluie "
    "varie beaucoup à l'intérieur d'un département.\n"
    "- **Prix fixe** : la valeur est calculée avec un seul prix par culture sur les trois ans. "
    "Le classement en gourdes ne tient donc pas compte des variations de prix.\n"
    "- **Population fixe** : une seule valeur par département, sans évolution sur les trois ans.\n"
    "- **Lignes retirées au nettoyage** : 18 doublons et 14 lignes sans production, "
    "supprimés pour ne pas inventer de chiffres.\n"
    "- **Données fictives** : elles servent à s'exercer, pas à décider pour de vrai."
)

with st.expander("Voir les données filtrées"):
    st.write(f"{len(filtre):,} lignes correspondent aux filtres choisis.")
    st.dataframe(filtre, use_container_width=True)
    st.download_button(
        "Télécharger ces données (CSV)",
        filtre.to_csv(index=False).encode("utf-8"),
        file_name="recoltes_filtrees.csv",
        mime="text/csv",
    )