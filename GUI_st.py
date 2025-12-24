import streamlit as st
import subprocess
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="DFS Cash Game Dashboard",
    layout="wide"
)

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

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

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

import pullCBS_st
import pullStokasticStatsAPI_st
import pullStokasticSalaryProj_st

def run_script(script_name: str, slate_id: str):
    with st.spinner(f"Running {script_name}..."):
        if script_name == "pullCBS.py":
            pullCBS_st.main()
        elif script_name == "pullStokasticStatsAPI.py":
            pullStokasticStatsAPI_st.main(slate_id)
        elif script_name == "pullStokasticSalaryProj.py":
            pullStokasticSalaryProj_st.main(slate_id)
    st.success(f"{script_name} finished successfully")

def available_csvs():
    files = []
    for csvs in script_outputs.values():
        for f in csvs:
            if Path(f).exists():
                files.append(f)
    return files

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------

st.sidebar.title("DFS Dashboard")

if st.sidebar.button("Run CBS Script"):
    run_script("pullCBS.py")

if st.sidebar.button("Run Stokastic Stats"):
    run_script("pullStokasticStatsAPI.py")

if st.sidebar.button("Run Salary Projections"):
    run_script("pullStokasticSalaryProj.py")

slate_id = st.sidebar.text_input(
    "Stokastic Slate ID",
    placeholder="e.g. 27878"
)

slate_id = slate_id.strip() # enforce numeric input

st.sidebar.divider()

csv_files = available_csvs()
display_map = {titles_for_combo[f]: f for f in csv_files}

selected_title = st.sidebar.selectbox(
    "Select dataset",
    options=list(display_map.keys())
)

# ------------------------------------------------------------------
# Main View
# ------------------------------------------------------------------

st.title("DFS Cash Game Dashboard")

if selected_title:
    filename = display_map[selected_title]
    df = pd.read_csv(filename)

    # Default sorting
    default_sort = default_sorts.get(filename)
    if default_sort:
        col, descending = default_sort
        if col in df.columns:
            df = df.sort_values(col, ascending=descending)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )