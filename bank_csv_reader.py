from dataclasses import dataclass
from datetime import date

import pandas as pd
from pandas.io.sas.sasreader import abstractmethod

# TODO - can make this the main point for
# csv ingestion and basic formatting
@dataclass
class BankCsvReader:
    total_charges: int|None = None
    csv_df: pd.DataFrame|None = None

    def read_csv(self, path_str: str):
        self.csv_df = pd.read_csv(path_str)
        return

    # TODO - regex is great, but isn't very scalable
    # let's see if we can replace this with a simple model
    def regex_tag_groceries(self) -> None:
        if self.csv_df is None:
            return

        grocery_list = [
            "RALPHS",
            "VONS",
            "TARGET",
            "NORTHGATE",
            "TRADER JOE"
        ]

        pattern = "|".join(grocery_list)
        self.csv_df["shared"] = self.csv_df["DESCRIPTION"].str.contains(
            pattern,
            case=False,
            na=False,
            regex=True
        )

        return

    @abstractmethod
    def save(self) -> None:
        ...

@dataclass
class CapitalOneCsvReader(BankCsvReader):
    def format_df(self):
        print("CapitalOne")


@dataclass
class WellsFargoCsvReader(BankCsvReader):
    def read_csv(
        self,
        path_str: str
    ):
        return super().read_csv(
            f"files/inputs/wells_fargo_cc/{path_str}"
        )

    def format_df(self):
        print("WellsFargo")

    def save(self) -> None:
        if self.csv_df is None:
            return

        today = date.today()
        self.csv_df.to_csv(
            f"files/outputs/wells_fargo_cc/{today}.csv"
        )
        return


@dataclass
class AppleCsvReader(BankCsvReader):
    def format_df(self):
        print("AppleCsvReader")
