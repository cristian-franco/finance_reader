from dataclasses import dataclass

import pandas as pd

# TODO - can make this the main point for
# csv ingestion and basic formatting
@dataclass
class BankCsvReader:
    total_charges: int|None = None
    csv_df: pd.DataFrame|None = None

    def read_csv(self, path_str: str):
        self.csv_df = pd.read_csv(path_str)
        return
