import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid threading issues
import matplotlib.pyplot as plt
import os
from db import get_db_connection

# ✅ Fetch Expenses Data
def fetch_expenses():
    engine = get_db_connection()
    try:
        with engine.connect() as connection:
            query = 'SELECT category, amount, date FROM expenses'
            df_expenses = pd.read_sql(query, connection)
            return df_expenses
    except Exception as e:
        print(f"Error fetching expenses: {e}")
        return pd.DataFrame()

# ✅ Fetch Income Data
def fetch_income():
    engine = get_db_connection()
    try:
        with engine.connect() as connection:
            query = 'SELECT source, amount, date FROM income'
            df_income = pd.read_sql(query, connection)
            return df_income
    except Exception as e:
        print(f"Error fetching income: {e}")
        return pd.DataFrame()

# Generate and Save the Pie Chart for Expenses
def generate_expenses_pie_chart():
    df_expenses = fetch_expenses()

    if df_expenses.empty:
        print("No expense data available.")
        return

    # Group data by category and sum amounts
    grouped_data = df_expenses.groupby('category')['amount'].sum()

    # Plot the Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=140)
    plt.title('Spending Distribution by Category')
    plt.axis('equal')

    # Ensure 'static' folder exists
    os.makedirs('static', exist_ok=True)

    # Save the Pie Chart to the 'static' folder
    output_path = os.path.join('static', 'expense_pie_chart.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Expense pie chart saved to {output_path}")

# Generate and save the Pie chart for income
def generate_income_pie_chart():
    df_income = fetch_income()

    if df_income.empty:
        print("No data for income")
        return
    
    #Grouping data by category
    grouped_data = df_income.groupby('source')['amount'].sum()

    #Plot the Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=140)
    plt.title('Income Distribution by Source')
    plt.axis('equal')

    # Ensure 'static' folder exists
    os.makedirs('static', exist_ok=True)

    #save plot to static
    output_path = os.path.join('static', 'income_pie_chart.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Income pie chart saved to {output_path}")


if __name__ == "__main__":
    generate_income_pie_chart()