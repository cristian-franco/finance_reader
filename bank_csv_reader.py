from dataclasses import dataclass
from datetime import date

import pandas as pd
from pandas.io.sas.sasreader import abstractmethod


@dataclass
class BankCsvReader:
    total_charges: int|None = None
    csv_df: pd.DataFrame|None = None


    def read_csv(self, path_str: str):
        csv_df = pd.read_csv(path_str, index_col=False)
        self.csv_df = csv_df.reset_index(drop=True)

        return


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
        self.csv_df["is_shared_groceries"] = self.csv_df["description"].str.contains(
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

    def format_df(self) -> None:
        if self.csv_df is None:
            return

        formatted_df = self.csv_df.copy()

        # rename all columns names to lower
        formatted_df.columns = formatted_df.columns.str.lower()

        columns_to_drop = [
            "status",
            "check #"
        ]
        formatted_df = formatted_df.drop(
            columns=columns_to_drop,
            errors="ignore"
        )

        # keep only negative amounts
        formatted_df = formatted_df.loc[
            formatted_df["amount"] <= 0
        ]

        # turn all negative amounts to positive
        formatted_df["amount"] = formatted_df["amount"] * -1

        # format date column
        formatted_df["date"] = pd.to_datetime(formatted_df["date"])

        self.csv_df = formatted_df

        return

    def filter_to_shared_groceries(self) -> None:
        if self.csv_df is None:
            return

        if "is_shared_groceries" not in self.csv_df.columns:
            print("No is_shared_groceries column")
            return

        self.csv_df = self.csv_df.loc[
            self.csv_df["is_shared_groceries"]
        ]

        return

    def save(self) -> None:
        if self.csv_df is None:
            return

        today = date.today()

        first_value = self.csv_df.iloc[0]["date"].date()

        month_str = first_value.strftime("%B")
        month_int = first_value.strftime("%m")
        year_int = first_value.year


        self.csv_df.to_csv(
            f"files/outputs/wells_fargo_cc/{year_int}_{month_int}_{month_str}_generated_{today}.csv",
            index=False
        )
        return


@dataclass
class AppleCsvReader(BankCsvReader):
    def format_df(self):
        print("AppleCsvReader")
