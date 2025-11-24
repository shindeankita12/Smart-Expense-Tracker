import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ExpenseTracker:
    def __init__(self, filepath="expenses.csv"):
        self.filepath = filepath

        if os.path.exists(filepath):
            self.data = pd.read_csv(filepath)
        else:
            self.data = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
            self.data.to_csv(filepath, index=False)

   
    def add_expense(self, date, amount, category, description):

        if amount <= 0:
            print("Error: Amount must be positive.")
            return

        valid_categories = ["Food", "Transport", "Utilities", "Entertainment", "Other"]
        if category not in valid_categories:
            print("Invalid category! Choose from:", valid_categories)
            return

        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }

        self.data = pd.concat([self.data, pd.DataFrame([new_entry])], ignore_index=True)
        self.data.to_csv(self.filepath, index=False)
        print(" Expense added successfully!")

   
    def get_summary(self):
        if self.data.empty:
            print("No expense data available.")
            return

        total = np.sum(self.data["Amount"])
        average = np.mean(self.data["Amount"])
        category_totals = self.data.groupby("Category")["Amount"].sum()

        summary = {
            "Total Spending": total,
            "Average Spending": average,
            "Category Totals": category_totals.to_dict()
        }

        print("\n Expense Summary:")
        print(summary)
        return summary

    def filter_expenses(self, condition):
        filtered_data = self.data.query(condition)
        print("\n Filtered Results:")
        print(filtered_data)
        return filtered_data

    def generate_report(self):
        if self.data.empty:
            print("No data available for visualization.")
            return

        print("Generating report...")

        plt.figure(figsize=(6, 4))
        sns.barplot(x="Category", y="Amount", data=self.data, estimator=sum)
        plt.title("Total Expenses by Category")
        plt.tight_layout()
        plt.show()

        self.data["Date"] = pd.to_datetime(self.data["Date"])
        sorted_data = self.data.sort_values("Date")

        plt.figure(figsize=(6, 4))
        plt.plot(sorted_data["Date"], sorted_data["Amount"], marker="o")
        plt.title("Spending Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(6, 4))
        self.data.groupby("Category")["Amount"].sum().plot(kind="pie", autopct="%1.1f%%")
        plt.title("Spending by Category")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.hist(self.data["Amount"], bins=10, color="skyblue", edgecolor="black")
        plt.title("Expense Amount Frequency")
        plt.xlabel("Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

        print("Report generated successfully!")

if __name__ == "__main__":
    tracker = ExpenseTracker()

    tracker.add_expense("2025-01-10", 50, "Food", "Lunch")
    tracker.add_expense("2025-01-12", 20, "Transport", "Bus fare")

    tracker.get_summary()
    tracker.filter_expenses("Amount > 20")

    tracker.generate_report()
