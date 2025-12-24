import streamlit as st
import subprocess
import pandas as pd

st.set_page_config(
    page_title="DFS Cash Game Dashboard",
    layout="wide"
)

# -------------------------------
# Config
# -------------------------------
script_outputs = {
    "pullCBS.py": [
        "cbs_QB_projections.csv",
        "cbs_RB_projections.csv",
        "cbs_WR_projections.csv",
        "cbs_TE_projections.csv"
    ],
    "pullStokasticStatsAPI.py": [
        "stokastic_passing.csv",
        "stokastic_rushing.csv",
        "stokastic_receiving.csv"
    ],
    "pullStokasticSalaryProj.py": [
        "stokastic_Salary_Projections.csv"
    ]
}

titles_for_combo = {
    "cbs_QB_projections.csv": "QB Stats, CBS",
    "cbs_RB_projections.csv": "RB Stats, CBS",
    "cbs_WR_projections.csv": "WR Stats, CBS",
    "cbs_TE_projections.csv": "TE Stats, CBS",

    "stokastic_passing.csv": "Passing Stats, Stokastic",
    "stokastic_rushing.csv": "Rushing Stats, Stokastic",
    "stokastic_receiving.csv": "Receiving Stats, Stokastic",

    "stokastic_Salary_Projections.csv": "Salaries and Projections"
}

default_sorts = {
    "cbs_QB_projections.csv": ("Fantasy Points", False),
    "cbs_RB_projections.csv": ("Fantasy Points", False),
    "cbs_WR_projections.csv": ("Fantasy Points", False),
    "cbs_TE_projections.csv": ("Fantasy Points", False),

    "stokastic_passing.csv": ("Attempts", False),
    "stokastic_rushing.csv": ("Rush", False),
    "stokastic_receiving.csv": ("Targets", False),

    "stokastic_Salary_Projections.csv": ("Projection", False)
}

# -------------------------------
# Helpers
# -------------------------------
@st.cache_data(show_spinner=False)
def load_csv(filename):
    return pd.read_csv(filename)

def run_script(script_name):
    subprocess.run(["python3", script_name], check=True)

# -------------------------------
# Sidebar – Controls
# -------------------------------
st.sidebar.titl
