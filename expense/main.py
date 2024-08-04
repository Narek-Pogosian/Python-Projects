import matplotlib.pyplot as plt
import pandas as pd

from csv_class import Csv_Class
from data_entry import get_amount, get_category, get_date, get_description


def main():
    while True:
        print("\n1. Add new transaction.  ")
        print("2. View transactions within a date range.  ")
        print("3. Exit")

        choice = input("Enter your choice 1-3: ")
        match choice:
            case "1":
                add()
            case "2":
                start_date = get_date("Enter the start date (dd-mm-yyyy): \n")
                end_date = get_date("Enter the end date (dd-mm-yyyy): \n")
                df = Csv_Class.get_transactions(start_date, end_date)
                if input("Do you want to see a plot? (y/n) ").lower() == "y":
                    plot_transactions(df)
            case "3":
                break
            case _:
                print("Invalid choice. Enter 1,2 or 3.")


def add():
    Csv_Class.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or blank for todays date: \n",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()

    Csv_Class.add_entry(date, amount, category, description)


def plot_transactions(df: pd.DataFrame):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, income_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
