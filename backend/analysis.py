import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid threading issues
import matplotlib.pyplot as plt
import os
from db import get_db_connection

#Fetch Expenses Data
def fetch_expenses(month=None, year=None):
    engine = get_db_connection()
    try:
        with engine.connect() as connection:
            query = 'SELECT category, amount, date FROM expenses'
            if month and year:
                query += " WHERE strftime('%m', date) = :month AND strftime('%Y', date) = :year"
            df_expenses = pd.read_sql(query, connection, params={
                "month": f"{int(month):02d}",
                "year": str(year)
            })
            return df_expenses
    except Exception as e:
        print(f"Error fetching expenses: {e}")
        return pd.DataFrame()

#Fetch Income Data
def fetch_income(month=None, year=None):
    engine = get_db_connection()
    try:
        with engine.connect() as connection:
            query = 'SELECT source, amount, date FROM income'
            if month and year:
                query += " WHERE strftime('%m', date) = :month AND strftime('%Y', date) = :year"
            df_income = pd.read_sql(query, connection, params={
                "month": f"{int(month):02d}",
                "year": str(year)
            })
            return df_income
    except Exception as e:
        print(f"Error fetching income: {e}")
        return pd.DataFrame()

# Generate and save the Monthly Pie chart 
def generate_monthly_pie_chart(data_type, month, year):

    if data_type == "expenses":
        df = fetch_expenses(month, year)
        title = f'Spend Distribution - {month}/{year}'
        filename = f'expense_pie_{month}_{year}.png'
        label_col = 'category'
    elif data_type == "income":
        df = fetch_income(month, year)
        title = f'Income Distribution - {month}/{year}'
        filename = f'income_pie_{month}_{year}.png'
        label_col = 'source'
    else:
        print("Invalid data type. Use 'expenses' or 'income'.")
    

    if df.empty: 
        print(f"No data for {data_type}")
        return
    
    #Grouping data by category
    grouped_data = df.groupby(label_col)['amount'].sum()

    #Plot the Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')

    # Ensure 'static' folder exists
    os.makedirs('static', exist_ok=True)

    #save plot to static
    output_path = os.path.join('static', filename)
    plt.savefig(output_path)
    plt.close()
    print(f"{filename} pie chart saved to {output_path}")


if __name__ == "__main__":
    generate_monthly_pie_chart('income', 1 , 2025)