# ===========================================================================
# PS Number: 42
# Project title: Personal Expense and Budget Manager
# Student Name: Devanshi Papihe
# Email: devanshi.papihe@rungta.org
# Section: BCA 1A
# ===========================================================================

from datetime import datetime
import os
import pandas as pd

FILE_NAME = "expenses.csv"


# Load expenses from CSV file
def load_expenses():
  if os.path.exists(FILE_NAME):
    return pd.read_csv(FILE_NAME)
  return pd.DataFrame(columns=["Date", "Category", "Amount"])


# Save expenses to CSV file
def save_expenses(df):
  df.to_csv(FILE_NAME, index=False)


# Set monthly budget
def set_budget():
  try:
    budget = float(input("Enter your monthly budget: "))

    if budget <= 0:
      print("Invalid budget. Budget must be positive.")
      return None

    print(f"Monthly budget set: {budget:.0f}")
    return budget

  except ValueError:
    print("Invalid budget. Please enter a valid number.")
    return None


# Add a new expense
def add_expense(df, budget):
  date = input("Enter date (YYYY-MM-DD): ")
  category = input("Enter expense category: ")

  # Validate date
  try:
    datetime.strptime(date, "%Y-%m-%d")
  except ValueError:
    print("Invalid date. Use YYYY-MM-DD.")
    return df

  # Validate category
  if not category.strip():
    print("Invalid category. Category cannot be empty.")
    return df

  # Validate amount
  try:
    amount = float(input("Enter expense amount: "))

    if amount <= 0:
      print("Invalid amount. Amount must be a positive number.")
      print("Expense not saved.")
      return df

  except ValueError:
    print("Invalid amount. Please enter a valid number.")
    print("Expense not saved.")
    return df

  # Store expense
  new_expense = pd.DataFrame(
      [{"Date": date, "Category": category.strip(), "Amount": amount}]
  )

  df = pd.concat([df, new_expense], ignore_index=True)

  save_expenses(df)

  print("Expense saved.")

  # Automatically show budget summary if budget is set
  if budget is not None:
    generate_report(df, budget)

  return df


# Category-wise spending summary
def category_summary(df):
  if df.empty:
    print("No expenses recorded yet.")
    return

  summary = df.groupby("Category")["Amount"].sum()
  cat_str = " | ".join([f"{cat}: {amt:.0f}" for cat, amt in summary.items()])
  print(cat_str)


# Generate expense report
def generate_report(df, budget):
  if budget is None:
    print("Please set your monthly budget first.")
    return

  # Calculate total expenses and remaining budget
  total_spent = df["Amount"].sum()
  remaining = budget - total_spent
  percentage = (total_spent / budget) * 100 if budget > 0 else 0

  # Category-wise spending on a single line with separator
  if not df.empty:
    summary = df.groupby("Category")["Amount"].sum()
    cat_str = " | ".join([f"{cat}: {amt:.0f}" for cat, amt in summary.items()])
    print(cat_str)
  else:
    print("No expenses recorded.")

  print(f"Total spent: {total_spent:.0f} | Remaining: {remaining:.0f}")

  # Budget status
  if percentage > 100:
    print(f"Budget exceeded ({percentage:.2f}%).")
  elif abs(percentage - 100) < 1e-5:
    print("Budget fully used (100.00%).")
  elif percentage >= 80:
    print(f"Warning: {percentage:.2f}% of the budget used.")
  else:
    print(f"Budget used: {percentage:.2f}%")


# Main program
def main():
  # Clear existing CSV at startup for clean test runs
  if os.path.exists(FILE_NAME):
    os.remove(FILE_NAME)

  df = load_expenses()
  budget = None

  while True:
    print("\n==============================")
    print(" PERSONAL EXPENSE & BUDGET MANAGER")
    print("==============================")

    print("1. Set Budget")
    print("2. Add Expense")
    print("3. Category Summary")
    print("4. Report")
    print("5. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
      new_budget = set_budget()
      if new_budget is not None:
        budget = new_budget

    elif choice == "2":
      df = add_expense(df, budget)

    elif choice == "3":
      category_summary(df)

    elif choice == "4":
      generate_report(df, budget)

    elif choice == "5":
      print("Thank you for using Personal Expense & Budget Manager!")
      break

    else:
      print("Invalid choice. Please select 1 to 5.")


# Run program
if __name__ == "__main__":
  main()