# This script queries the Stokastic NFL data hub API for salary, position, projection, etc
import requests
import pandas as pd

def main(slate_id):
    url = "https://app-api-dfs-prod-main.azurewebsites.net/api/slatedata/projections"
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

    # Dataframe clean up (drop unnecessary columns and round numbers)
    # Drop columns
    df.drop(columns=['id', 'site', 'teamLogo', 'opponentLogo', 'nameAndId', 'gameTime'], inplace=True)

    # convert percentags columns to better display format
    percentageColumns = ['ownership', 'optimal', 'leverage', 'boom', 'bust']
    for col in percentageColumns:
        df[col] = df[col] * 100

    # Round columns
    df = df.round(2)

    # add % symbol to percentage columns
    for col in percentageColumns:
        df[col] = df[col].astype(str) + '%'

    # add $ to salary column
    df['salary'] = '$' + df['salary'].astype(str)

    # capitalize all column names
    df.columns = df.columns.str.capitalize()

    df.to_csv("stokastic_Salary_Projections.csv", index=False)


if __name__ == "__main__":
    main(slate_id)