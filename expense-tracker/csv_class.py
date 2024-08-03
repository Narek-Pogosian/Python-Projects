import pandas as pd
import csv

from datetime import datetime
from data_entry import DATE_FORMAT


class Csv_Class:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added succesfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=DATE_FORMAT)
        start_date = datetime.strptime(start_date, DATE_FORMAT)
        end_date = datetime.strptime(end_date, DATE_FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in this give date range.\n")
        else:
            print(f"Transactions from {start_date.strftime(DATE_FORMAT)} to {end_date.strftime(DATE_FORMAT)}.\n")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(DATE_FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\nSummary:")
            print(f"Total income: ${total_income:.2f}")
            print(f"Total expense: ${total_expense:.2f}")
            print(f"Net savings: ${(total_income - total_expense):.2f}")

        return filtered_df
