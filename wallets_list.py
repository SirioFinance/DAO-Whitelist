# extract_owner_wallets.py

import pandas as pd
import json
import re
from pathlib import Path

def extract_owner_from_csv(file_path: Path) -> str | None:
    """Extract 'Owner' from the second row in a CSV file."""
    try:
        df = pd.read_csv(file_path)
        if 'Owner' in df.columns and len(df) > 1:
            return df.loc[1, 'Owner']
        return None
    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")
        return None

def extract_wallets_from_json(json_path: Path) -> list[str]:
    """Extract wallet addresses like '0.0.XXXXX' from 'results' list in JSON."""
    wallets = []
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        for result in data.get('results', []):
            for key in result:
                if re.fullmatch(r"0\.0\.\d+", key):
                    wallets.append(key)
    except Exception as e:
        print(f"Error reading {json_path.name}: {e}")
    return wallets

def save_wallets_to_csv(wallets: list[str], output_path: Path):
    """Save wallet addresses to a CSV file."""
    df = pd.DataFrame(wallets, columns=['WalletAddress'])
    df.to_csv(output_path, index=False)

def main():
    csv1_owner = extract_owner_from_csv(Path("0.0.7089383.csv"))
    csv2_owner = extract_owner_from_csv(Path("0.0.7829347.csv"))
    wallets = extract_wallets_from_json(Path("SUPPLIERS_LIST.json"))

    print("CSV 1 Owner:", csv1_owner)
    print("CSV 2 Owner:", csv2_owner)
    print("Wallet Addresses:", wallets)

    save_wallets_to_csv(wallets, Path("wallet_addresses.csv"))

if __name__ == "__main__":
    main()

