import requests
from bs4 import BeautifulSoup
import pandas as pd

session = requests.Session()

# Login
login_url = "https://www.stokastic.com/login2"
payload = {
    "log": "",
    "pwd": "",
    "redirect_to": "https://www.stokastic.com/",
    "rememberme": "forever"
}
session.post(login_url, data=payload, headers={"User-Agent": "Mozilla/5.0"})

# Fetch stats page
stats_url = "https://www.stokastic.com/nfl/nfl-dfs-projected-stats/"
resp = session.get(stats_url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(resp.text, "html.parser")

def parse_table(table_id, filename):
    table = soup.find("table", {"id": table_id})
    if not table:
        print(f"No table found with id={table_id}")
        return None

    # Extract headers using aria-label if available
    headers = []
    for th in table.find("thead").find_all("th"):
        label = th.get("aria-label")
        if label:
            headers.append(label.strip())
        else:
            headers.append(th.get_text(strip=True))
    
    # Deduplicate if needed
    headers = list(dict.fromkeys(headers))  # removes duplicates, keeps order

    # Extract rows
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            rows.append(cells)

    # Align headers with row length
    if rows and len(headers) == len(rows[0]):
        df = pd.DataFrame(rows, columns=headers)
    else:
        df = pd.DataFrame(rows)

    print(f"\n{table_id} preview:")
    print(df.head())
    df.to_csv(filename, index=False)
    return df

# Parse Passing, Rushing, Receiving
passing_df = parse_table("table_1", "stokastic_passing.csv")
rushing_df = parse_table("table_2", "stokastic_rushing.csv")
receiving_df = parse_table("table_3", "stokastic_receiving.csv")

