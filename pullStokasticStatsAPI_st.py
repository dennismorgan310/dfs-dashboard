
import requests
import pandas as pd

def main(slate_id):
    def process(Type, slate_id):
        url = f"https://app-api-dfs-prod-main.azurewebsites.net/api/slatedata/stats?sport=NFL&type={Type}"
        params = {
            "SlateId": slate_id
        }

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Origin": "https://tools.stokastic.com",
            "Referer": "https://tools.stokastic.com/"
        }

        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()

        data = r.json()

        df = pd.DataFrame(data)

        # drop unnecessary columns
        colsToDrop = ['catchPercent', 'targetsBase', 'catchBase']
        if Type == 'receiving':
            df.drop(columns=colsToDrop, inplace=True)

        # round to 2 decimal places
        df = df.round(2)

        # capitalize column titles
        df.columns = df.columns.str.capitalize()

        df.to_csv(f"stokastic_{Type}.csv", index=False)

    for Type in ['passing', 'rushing', 'receiving']:
        process(Type)

if __name__ == "__main__":
    main(slate_id)