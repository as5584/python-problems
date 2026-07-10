import pandas as pd
from datetime import date
import os
import matplotlib.pyplot as plt

File = "expense_tracker.csv"
CATEGORIES = {1: "FOOD", 2: "CLOTHES", 3: "VEHICLES", 4: "ELECTRONICS"}

if not os.path.exists(File):
    df = pd.DataFrame(columns=["Date", "Category", "Item", "Amount", "Payment Method"])
    df.to_csv(File, index=False)
    print("New expense file created")


def add_expenses():
    current_date = date.today().strftime("%Y-%m-%d")
    print("CATEGORIES:")
    for num, cat in CATEGORIES.items():
        print(f"{num}. {cat}")
    while True:
        try:
            categ = int(input("enter the option from above menu: "))
        except ValueError:
            print("only numeric value excepted")
            continue
        if categ in CATEGORIES:
            category = CATEGORIES[categ]
            while True:
                item_input = input(f"enter the {category} you bought: ").strip()
                if not item_input:
                    print("Item name cannot be empty.")
                    continue
                elif item_input.isdigit():
                    print(f"please enter valid {category}")
                    continue
                else:
                    break
            while True:
                try:
                    amount_input = float(input(f"enter the amount of {item_input}: "))
                    if amount_input < 0:
                        print("amount can't be negative")
                        continue
                    break
                except ValueError:
                    print("only numerical value")
                    continue
            break
        else:
            print("wrong option! try again")

    print(
        """Payment Method
        1. Online
        2. Cash"""
    )
    while True:
        try:
            ch = int(input("enter your payment method: "))
            if ch == 1:
                payment_method = "Online"
            elif ch == 2:
                payment_method = "Cash"
            else:
                print("wrong input. try again")
                continue
            break
        except ValueError:
            print("wrong datatype . only integer")
    new_expense = pd.DataFrame(
        [[current_date, category, item_input, amount_input, payment_method]],
        columns=["Date", "Category", "Item", "Amount", "Payment Method"],
    )
    new_expense.to_csv(File, mode="a", index=False, header=False)
    print("Expense added successfully!")
    return


def view_all_expenses():
    rd = pd.read_csv(File)
    if rd.empty:
        print("No expenses yet")
        return
    else:
        rd.index = rd.index + 1
        print("All expenses:")
        print(rd.to_string(index=True))
        return


def show_total():
    rd = pd.read_csv(File)
    total_expense = rd["Amount"].sum()
    print("The Total Expense is:", total_expense)
    return


def expenses_by_category():
    while True:
        expenses_category = pd.read_csv(File)
        print(
            """
        CATEGORIES:
        1. FOOD
        2. CLOTHES
        3. VEHICLES
        4. ELECTRONICS"""
        )
        while True:
            try:
                user_input = input("enter the category you want to see record of (in words): ").upper().strip()
                if not user_input.isalpha():
                    print("please enter only alphabetical character")
                    continue
                break
            except ValueError:
                print("enter only alphabet not numeric")
                continue
        filter1 = expenses_category[expenses_category["Category"] == user_input]
        if filter1.empty:
            print("no record under this category")
        else:
            print(f"There is the expense record for your entered category:-")
            filter1.index += 1
            print(filter1)
        break


def filter_by_date():
    while True:
        try:
            rd = pd.read_csv(File)
            year = int(input("Enter a year (e.g., 2024): "))
            month = int(input("Enter a month (1-12): "))
            day = int(input("Enter a day (1-31): "))
            date1 = date(year, month, day)
            filter_df = rd[rd["Date"] == str(date1)]
            if filter_df.empty:
                print(f"There is no expenses on {date1}")
            else:
                print(f"Here is the expenses for your date {date1}")
                filter_df.index += 1
                print(filter_df)
            break
        except ValueError:
            print("wrong date format . try again")
            continue


def monthly_expenses():
    df = pd.read_csv(File, parse_dates=["Date"])
    if df.empty:
        print("No Expenses Yet...")
        return
    monthly = df.groupby(df["Date"].dt.strftime("%Y-%m"))["Amount"].sum().reset_index()
    print("\nMonthly Spending Summary:")
    for index, row in monthly.iterrows():
        print(f"{row['Date']}: ₹{row['Amount']:.2f}")
    print(f"Grand Total: ₹{monthly['Amount'].sum():.2f}")
    return


def highest_expense_category():
    df = pd.read_csv(File)
    if df.empty:
        print("No expenses yet")
        return
    category_totals = df.groupby("Category")["Amount"].sum()
    if category_totals.empty:
        print("No expenses recorded.")
        return
    max_cat = category_totals.idxmax()
    max_amount = category_totals.max()
    print(f"\nHighest Expense Category: {max_cat} (₹{max_amount:.2f})")
    print("\nAll Category Totals:")
    for cat, amt in category_totals.items():
        print(f"{cat}: ₹{amt:.2f}")


def plot_pie_chart():
    df = pd.read_csv(File)
    if df.empty:
        print("No expenses yet to visualize.")
        return
    category_totals = df.groupby("Category")["Amount"].sum()
    if category_totals.empty:
        print("No data for pie chart.")
        return

    plt.figure(figsize=(8, 8))
    plt.pie(
        category_totals,
        labels=category_totals.index,
        autopct="%1.1f%%",
        startangle=140,
        shadow=True,
    )
    plt.title("Expense Distribution by Category")
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    print("Pie chart displayed!")


def main():
    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")
        print("1. ADD EXPENSES")
        print("2. VIEW YOUR EXPENSES")
        print("3. SHOW TOTAL EXPENSES")
        print("4. EXPENSES BY CATEGORY")
        print("5. FILTER BY DATE")
        print("6. MONTHLY EXPENSES")
        print("7. HIGHEST EXPENSE CATEGORY")
        print("8. PIE CHART (Expense by Category)")
        print("9. EXIT")
        while True:
            try:
                ch = int(input("Enter your choice from above menu: "))
                break
            except ValueError:
                print("Enter only integer")
                continue
        if ch == 1:
            add_expenses()
        elif ch == 2:
            view_all_expenses()
        elif ch == 3:
            show_total()
        elif ch == 4:
            expenses_by_category()
        elif ch == 5:
            filter_by_date()
        elif ch == 6:
            monthly_expenses()
        elif ch == 7:
            highest_expense_category()
        elif ch == 8:
            plot_pie_chart()
        elif ch == 9:
            print("Thanks for using my expense tracker!")
            break
        else:
            print("Invalid choice. Try again")


if __name__ == "__main__":
    main()