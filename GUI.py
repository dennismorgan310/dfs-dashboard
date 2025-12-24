import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import subprocess
import pandas as pd

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

# define more readable title's to display in the combo box to user
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
    "cbs_QB_projections.csv": ("Fantasy Points", True),
    "cbs_RB_projections.csv": ("Fantasy Points", True),
    "cbs_WR_projections.csv": ("Fantasy Points", True),
    "cbs_TE_projections.csv": ("Fantasy Points", True),

    "stokastic_passing.csv": ("Attempts", True),
    "stokastic_rushing.csv": ("Rush", True),
    "stokastic_receiving.csv": ("Targets", True),

    "stokastic_Salary_Projections.csv": ("Projection", True)
} # True sets default sort to descending


current_df = None
sort_state = {
    "column": None,
    "descending": False
}

def run_script(script_name):
    try:
        subprocess.run(["python3", script_name], check=True)
        csv_files = script_outputs[script_name]

        # Get the nice display titles instead of file names
        display_titles = [titles_for_combo[file_name] for file_name in csv_files]

        # Combine with existing combo box values
        current_values = list(csv_combo["values"])  # convert to list in case it's empty
        csv_combo["values"] = current_values + display_titles

        if csv_combo["values"]:
            csv_combo.current(0)

        messagebox.showinfo("Success", f"{script_name} finished. Select a CSV to view.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run {script_name}: {e}")


def autosize_columns(tree, dataframe):
    font = tkfont.nametofont("TkDefaultFont")

    for col in dataframe.columns:
        max_width = font.measure(col)  # start with header width

        for value in dataframe[col].astype(str):
            max_width = max(max_width, font.measure(value))

        # Add padding so text isn't cramped
        tree.column(col, width=max_width + 20, stretch=False)

def load_csv():
    global current_df, sort_state

    try:
        title = csv_combo.get()
        filename = [k for k, v in titles_for_combo.items() if v == title][0]
        if not filename:
            messagebox.showwarning("No file", "Please select a CSV file.")
            return

        current_df = pd.read_csv(filename)
        sort_state = {"column": None, "descending": False}

        # Clear table
        for row in tree.get_children():
            tree.delete(row)

        tree["columns"] = list(current_df.columns)
        tree["show"] = "headings"

        for col in current_df.columns:
            tree.heading(
                col,
                text=col,
                command=lambda c=col: sort_by_column(c)
            )

        for _, row in current_df.iterrows():
            tree.insert("", "end", values=list(row))
        
        autosize_columns(tree, current_df)

        default = default_sorts.get(filename)

        if default:
            col, descending = default
            if col in current_df.columns:
                sort_by_column(col, force_descending=descending)


    except Exception as e:
        messagebox.showerror("Error", f"Failed to load {filename}: {e}")

def sort_by_column(col, force_descending=None):
    global current_df, sort_state

    if current_df is None:
        return

    if force_descending is not None:
        sort_state["column"] = col
        sort_state["descending"] = force_descending
    else:
        if sort_state["column"] == col:
            sort_state["descending"] = not sort_state["descending"]
        else:
            sort_state["column"] = col
            sort_state["descending"] = False

    descending = sort_state["descending"]

    current_df = current_df.sort_values(by=col, ascending=not descending)

    for row in tree.get_children():
        tree.delete(row)

    for _, row in current_df.iterrows():
        tree.insert("", "end", values=list(row))

    for c in current_df.columns:
        arrow = ""
        if c == col:
            arrow = " ▼" if descending else " ▲"
        tree.heading(c, text=c + arrow)


# Main window
root = tk.Tk()
root.title("DFS Cash Game Dashboard")
root.geometry("1000x700")

btn_cbs = tk.Button(root, text="Run CBS Script", command=lambda: run_script("pullCBS.py"))
btn_stokastic = tk.Button(root, text="Run Stokastic Script", command=lambda: run_script("pullStokasticStatsAPI.py"))
btn_salary = tk.Button(root, text="Run Projection Script", command=lambda: run_script("pullStokasticSalaryProj.py"))
btn_cbs.pack(pady=5)
btn_stokastic.pack(pady=5)
btn_salary.pack(pady=5)

csv_combo = ttk.Combobox(root, state="readonly")
csv_combo.pack(pady=5)

btn_load = tk.Button(root, text="Load Selected CSV", command=load_csv)
btn_load.pack(pady=5)

tree = ttk.Treeview(root)
tree.pack(expand=True, fill="both")

# --- Run all scripts automatically on launch ---
for script in ["pullCBS.py", "pullStokasticStatsAPI.py", "pullStokasticSalaryProj.py"]:
    run_script(script)

root.mainloop()
