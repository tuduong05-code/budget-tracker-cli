import os 
import csv
from datetime import datetime

# for add_transaction  

EXPENSE_CATEGORIES = [
    "groceries",
    "dine out",
    "transport",
    "housing",
    "shopping",
    "others"
]

INCOME_CATEGORIES = [
    "salary",
    "investments",
    "bonuses",
    "others"
]

# add a constant for the CSV file path

TRANSACTIONS_FILE = "data/transactions.csv"

def get_transactions_file_path() -> str:
    """Return the full path to the transactions CSV file."""
    return TRANSACTIONS_FILE 

def ensure_transactions_file_exists():
    file_path = get_transactions_file_path()

    # if the data folder does not exist, create it
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # if the file does not exist, create it with a header row
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "type", "category", "amount", "description"])

# from list-of-lists to list-of-dictionaries using csv.DictReader 
# make the code easier to read for anyone viewing GitHub

def read_all_transactions():
    """Return all rows from the transactions CSV as a list of dictionaries."""
    ensure_transactions_file_exists()
    file_path = get_transactions_file_path()
    with open(file_path, mode='r', newline='') as file:
        return list(csv.DictReader(file))


# phase 1 step 3: plan helper functions and data model (no heavy logic yet)

def show_menu():
    print("\n==== PERSONAL BUDGET MANAGER ====")
    print("1. Add a transaction")
    print("2. View all transactions")
    print("3. View spending by category")
    print("4. View summary")
    print("5. View monthly statistics")
    print("6. Evaluate monthly spending")
    print("7. Quit")

def add_transaction():
    """Prompt user for transaction details and save to CSV."""
    ensure_transactions_file_exists()
    file_path = get_transactions_file_path()

    # handle date with validation + default to today rows

    today = datetime.today().strftime("%Y-%m-%d")
    date_input = input(f"\nEnter the date (YYYY-MM-DD) [default: {today}]: ").strip()

    # use today's date if user presses enter without input
    if not date_input:
        transaction_date = today
    else:
        transaction_date = date_input

    # validate the date format until correct
    while True:
        try:
            datetime.strptime(transaction_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD, like 2025-06-01.")
            date_input = input(f"Enter the date (YYYY-MM-DD) [default: {today}]: ").strip()
            if not date_input:
                transaction_date = today
            else:
                transaction_date = date_input



    transaction_type = input("Type of transaction (income/expense): ").strip().lower()
    while transaction_type not in ["income", "expense"]:
        transaction_type = input("Please enter 'income' or 'expense': ").strip().lower()

    # choose category list based on transaction type
    if transaction_type == "expense":
        categories = EXPENSE_CATEGORIES
    else:
        categories = INCOME_CATEGORIES

    # show category options
    print("\nSelect a category:")
    for i, cat in enumerate(categories, 1):  # use 'categories' here
        print(f"{i}. {cat}")

    while True:
        choice = input("-> Choose a corresponding number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):  # use 'categories' here
            category = categories[int(choice) - 1]  # use 'categories' here
            break
        else:
            print("Invalid choice. Please enter a valid number.")

    # validate amount
    while True:
        amount_text = input("Enter the amount (for example, 25.50): ").strip()
        try:
            amount = float(amount_text)
            break
        except ValueError:
            print("Invalid amount. Please enter a number like 12.50.")

    description = input("Any notes?: ").strip()

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            transaction_date, 
            transaction_type, 
            category, 
            amount,
            description
        ])
        
    print("\nTransaction added successfully! 👍")

def view_all_transactions():
    """Display all stored transactions in a formatted table."""
    rows = read_all_transactions() 

    if not rows:
        print("\nNo transactions found yet.\n")
        return
    
    # column width
    date_w = 12
    type_w = 10
    category_w = 12
    amount_w = 12
    description_w = 14

    print("\nAll transactions:\n")

    # header
    print("date".ljust(date_w) +
          "type".ljust(type_w) +
          "category".ljust(category_w) +
          "amount".ljust(amount_w) +
          "description".ljust(description_w))

    print("-" * (date_w + type_w + category_w + amount_w + description_w))

    # rows

    for row in rows:
        date = row["date"]
        ttype = row["type"]
        category = row["category"]
        amount = float(row["amount"])
        description = row["description"]

        print(
            date.ljust(date_w) +
            ttype.ljust(type_w) +
            category.ljust(category_w) +
            f"${amount:,.2f}".ljust(amount_w) +
            description.ljust(description_w)
        )

    print()

def view_spending_by_category():
    """Display total expenses grouped by category."""
    rows = read_all_transactions() 

    if not rows:
        print("\nNo transactions found yet. Add some!\n")
        return
    
    category_totals = {} # an empty dictionary to hold totals per category

    for row in rows:
        ttype = row["type"].lower()
        category = row["category"]
        amount = float(row["amount"])

        if ttype == "expense": # only track expenses per category, not income
            if category in category_totals: 
                # if the category already exists, add the current amount
                category_totals[category] += amount
            else:
                # otherwise, create a new entry for the category with the current amount 
                category_totals[category] = amount

    print("\nSpending by category:\n")
    print("category".ljust(20) + "total spent")
    print("-" * 30)

    for category, total in category_totals.items():
        print(f"{category.ljust(20)}${total:,.2f}")

    print()

def view_summary():
    """Print total income, total expenses, and current balance."""
    rows = read_all_transactions() 

    if not rows:
        print("\nNo transactions found yet. Add some!\n")
        return
    
    total_income = 0.0
    total_expenses = 0.0

    for row in rows:
        ttype = row["type"]
        amount = float(row["amount"])

        if ttype == "income":
            total_income += amount
        elif ttype == "expense":
            total_expenses += amount
        
    current_balance = total_income - total_expenses

    print("\nSummary:")
    print(f"- Total income:    ${total_income:,.2f}")
    print(f"- Total Expenses:  ${total_expenses:,.2f}")
    print(f"- Current Balance: ${current_balance:,.2f}")

# Example of a transaction dictionary
# transaction = {
#     "date": "2025-06-01",
#     "type": "income", # or "expense"
#     "category": "rent",
#     "amount": 1200.00,
#     "description": "June rent"
# }

def view_monthly_stats():
    """Show monthly totals for income, expenses, and balance."""
    rows = read_all_transactions() 

    if not rows:
        print("\nNo transactions found yet. Add some!\n")
        return

    monthly = {}

    for row in rows:
        year_month = row["date"][:7]
        ttype = row["type"].lower()
        amount = float(row["amount"])

        if year_month not in monthly:
            monthly[year_month] = {"income": 0.0, "expense": 0.0}
        if ttype in monthly[year_month]:
            monthly[year_month][ttype] += amount

    print("\nmonthly statistics:\n")
    print("month".ljust(10) + "income".rjust(12) + "expenses".rjust(12) + "balance".rjust(12))
    print("-" * 46)

    for month, totals in sorted(monthly.items()):
        income = totals["income"]
        expense = totals["expense"]
        balance = income - expense
        print(f"{month.ljust(10)}$ {income:>10,.2f}  {expense:>10,.2f}  {balance:>10,.2f}")

    print()

def evaluate_monthly_spending():
    """Evaluate each month's spending based on expense/income ratio."""
    rows = read_all_transactions() 

    if not rows:
        print("\nNo transactions found yet. Add some!\n")
        return

    monthly = {}

    for row in rows:
        year_month = row["date"][:7]  # extract YYYY-MM
        ttype = row["type"].lower()
        amount = float(row["amount"])

        if year_month not in monthly:
            monthly[year_month] = {"income": 0.0, "expense": 0.0}
        if ttype in monthly[year_month]:
            monthly[year_month][ttype] += amount

    print("\nMonthly Financial Health:\n")
    print(f"{'Month':<10}{'Income ($)':>15}{'Expense ($)':>15}{'Exp/Inc (%)':>15}{'Status':>15}")
    print("-" * 70)

    for month, totals in sorted(monthly.items()):
        income = totals["income"]
        expense = totals["expense"]
        expense_ratio = (expense / income * 100) if income > 0 else 0

        if expense_ratio <= 50:
            status = "Good 👍"
        elif expense_ratio <= 70:
            status = "Caution ⚠️"
        else:
            status = "Overspending ❌"

        print(f"{month:<10}"
            f"{income:>14,.2f}"
            f"{expense:>14,.2f}"
            f"{expense_ratio:>14.1f}"
            f"{status:>15}")

    print()


def main():
    ensure_transactions_file_exists()
    print("Welcome to Personal Budget Manager!")
    print("Using data file:", get_transactions_file_path())

    while True:
        show_menu()
        choice = input("\n-> Choose an option (1-7): ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_all_transactions()
        elif choice == "3":
            view_spending_by_category()
        elif choice == "4":
            view_summary()
        elif choice == "5":
            view_monthly_stats()
        elif choice == "6":
            evaluate_monthly_spending()
        elif choice == "7":
            print("Bye Bye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")           

if __name__ == "__main__":
    main()
