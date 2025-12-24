import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def pull(pos):
    url = f"https://www.cbssports.com/fantasy/football/stats/{pos}/2025/tp/projections/nonppr/"
    headers = {"User-Agent": "Mozilla/5.0"}  # helps avoid being blocked
    resp = requests.get(url, headers=headers)

    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the table by class
    table = soup.find("table", {"class": "TableBase-table"})

    if table:
        # Wrap in StringIO to avoid the FutureWarning
        df = pd.read_html(StringIO(str(table)))[0]
        
        # Drop first level of multi-index, it's not needed
        df.columns = df.columns.get_level_values(1)

        # drop abbreviated part of column names
        df.columns = df.columns.str.split(' ', n=1).str[1]

        # put the Name column back in
        df.rename(columns={df.columns[0]: 'Name'}, inplace=True)

        df.to_csv(f"cbs_{pos}_projections.csv", index=False)
    else:
        print(f"No {pos} table found")

# pull each position's table
for pos in ['QB', 'RB', 'WR', 'TE']:
    pull(pos) # call pull function
