import pandas as pd
import polars as pl
import bank_csv_reader
import os
from pathlib import Path
from dotenv import load_dotenv

# TODO - replace pandas with polars
def validate_folders(
    FILES_PATH: str | None
):
    input_folder_lists = [
        f"{FILES_PATH}/inputs/wells_fargo_cc",
        f"{FILES_PATH}/inputs/capital_one_cc",
        f"{FILES_PATH}/inputs/apple_cc",
        f"{FILES_PATH}/outputs/wells_fargo_cc",
        f"{FILES_PATH}/outputs/capital_one_cc",
        f"{FILES_PATH}/outputs/apple_cc",
    ]

    for folder_path in input_folder_lists:
        if not os.path.exists(folder_path):
            print(f"{folder_path} does not exist, creating...")
            try:
                os.makedirs(folder_path)
                print(f"{folder_path} created!")
            except FileExistsError:
                print(f"One or more directories in '{folder_path}' already exists")
            except PermissionError:
                print(f"Permission denied: Unable to create '{folder_path}'.")
            except Exception as e:
                print(f"An error occurred: {e}")


# def instantiate_readers() -> BankCsvReader:


def main():
    # read .env for file path
    load_dotenv()

    FILES_PATH = os.getenv("FILES_PATH")

    # print(FILES_PATH)

    # validate_folders(FILES_PATH)

    # idk why I wrote a class for this
    # but can have child classes that each implement
    # read_csv function differently, or along those lines
    wf_bank_csv_reader = bank_csv_reader.WellsFargoCsvReader()
    # co_bank_csv_reader = bank_csv_reader.CapitalOneCsvReader()
    # apple_bank_csv_reader = bank_csv_reader.AppleCsvReader()

    # TODO - read .env for what csv types we will need

    # TODO - find a better way to organize inputs and outputs
    # inputs should be labeled 2026_August, for all transactions in
    # August 2026
    #
    # General order here
    # 1. Identify latest unmarked csv
    # 2. Ingest into df, tag transactions, save to outputs folder
    # with proper date file name
    # 3. Can make a sqlite table to store transactions in, makes it easier
    # to move to home server and a service
    wf_bank_csv_reader.read_csv('CreditCard.csv')
    wf_bank_csv_reader.regex_tag_groceries()
    wf_bank_csv_reader.save()

    # TODO - find a good way to have the script automatically
    # determine what month its for
    # e.g. running it several times through the month
    # will overwrite the same output file
    #
    # TODO - drop index on output csv
    # TODO - make function to create groceries csv only
    # TODO - drop records for payments
    #

if __name__ == "__main__":
    main()
