"""
Fetch World Bank Data (2000–2024)
=================================
Fetches Life Expectancy at birth (SP.DYN.LE00.IN) and GDP (NY.GDP.MKTP.CD)
for Chile, China, Germany, Mexico, USA, and Zimbabwe directly from the
official World Bank Open Data API.
"""

import json
import urllib.request
from pathlib import Path
import pandas as pd

COUNTRIES = {
    "CL": "Chile",
    "CN": "China",
    "DE": "Germany",
    "MX": "Mexico",
    "US": "United States of America",
    "ZW": "Zimbabwe",
}

INDICATORS = {
    "SP.DYN.LE00.IN": "Life expectancy at birth (years)",
    "NY.GDP.MKTP.CD": "GDP",
}

BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date=2000:2024&format=json&per_page=1000"
OUTPUT_FILE = Path(__file__).parent / "all_data_extended.csv"


def fetch_indicator(country_code: str, indicator_code: str) -> list[dict]:
    url = BASE_URL.format(country=country_code.lower(), indicator=indicator_code)
    req = urllib.request.Request(url, headers={"User-Agent": "DataScienceResearch/1.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
        if len(payload) > 1 and payload[1]:
            return payload[1]
    return []


def build_extended_dataset() -> pd.DataFrame:
    rows = {}  # (Country, Year) -> dict

    for code, country_name in COUNTRIES.items():
        print(f"Fetching data for {country_name} ({code})...")
        for ind_code, ind_name in INDICATORS.items():
            records = fetch_indicator(code, ind_code)
            for item in records:
                year_str = item.get("date")
                val = item.get("value")
                if not year_str or val is None:
                    continue
                year = int(year_str)
                key = (country_name, year)
                if key not in rows:
                    rows[key] = {"Country": country_name, "Year": year}
                rows[key][ind_name] = val

    df = pd.DataFrame(list(rows.values()))
    
    # Drop rows that don't have both GDP and Life Expectancy
    df = df.dropna(subset=["Life expectancy at birth (years)", "GDP"])
    df["Year"] = df["Year"].astype(int)
    df = df.sort_values(by=["Country", "Year"]).reset_index(drop=True)
    
    # Ensure correct column ordering
    columns = ["Country", "Year", "Life expectancy at birth (years)", "GDP"]
    df = df[columns]
    
    return df


def main():
    print("=" * 60)
    print(" World Bank API Ingestion: 2000–2024")
    print("=" * 60)
    df = build_extended_dataset()
    print(f"\nFetched {len(df)} records across {df['Country'].nunique()} nations.")
    print(f"Year coverage: {df['Year'].min()} – {df['Year'].max()}")
    print("\nSample rows:")
    print(df.head(10).to_string(index=False))
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved extended dataset to: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()

