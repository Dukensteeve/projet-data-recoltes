from pathlib import Path

import pandas as pd
import streamlit as st

DOSSIER = Path(__file__).parent / "donnees"

st.set_page_config(page_title="Les récoltes agricoles", page_icon="🌾", layout="wide")

st.title("Les récoltes agricoles")
st.caption("Projet final, Python pour l'analyse de données, ESIH 2026. Données fictives.")

brut = pd.read_csv(DOSSIER / "recoltes_brut.csv")
st.write(f"Le fichier brut compte {len(brut)} lignes.")
st.dataframe(brut.head(10), hide_index=True)
