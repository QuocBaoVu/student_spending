import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid threading issues
import matplotlib.pyplot as plt
import os
from db import get_db_connection

#fetch_data function
def fetch_data(data_type, month=None, year=None, chart_type=None):

    if data_type not in ["income", "expenses"]:
        print("Invalid data type. Choose 'income' or 'expenses'.")
        return pd.DataFrame()

    engine = get_db_connection()

    try:
        with engine.connect() as connection:
            # ✅ PIE CHART DATA
            if chart_type == "pie":
                query = f"SELECT {'source' if data_type == 'income' else 'category'}, amount, date FROM {data_type}"
                params = {}
                if month and year:
                    query += " WHERE strftime('%m', date) = :month AND strftime('%Y', date) = :year"
                    params = {
                        "month": f"{int(month):02d}",
                        "year": str(year)
                    }
                df_data = pd.read_sql(query, connection, params=params)

            # ✅ ANNUAL BAR CHART DATA
            elif chart_type == "annual_bar":
                query = f"""
                    SELECT strftime('%m', date) AS month, SUM(amount) AS total_amount 
                    FROM {data_type} 
                    WHERE strftime('%Y', date) = :year 
                    GROUP BY month 
                    ORDER BY month
                """
                df_data = pd.read_sql(query, connection, params={
                    "year": str(year)
                })

            # ✅ MONTHLY BAR CHART DATA
            elif chart_type == "monthly_bar":
                query = f"""
                    SELECT strftime('%d', date) AS day, SUM(amount) AS total_amount 
                    FROM {data_type} 
                    WHERE strftime('%m', date) = :month AND strftime('%Y', date) = :year 
                    GROUP BY day 
                    ORDER BY day
                """
                df_data = pd.read_sql(query, connection, params={
                    "month": f"{int(month):02d}",
                    "year": str(year)
                })

            else:
                print("Invalid chart type. Choose 'pie', 'annual_bar', or 'monthly_bar'.")
                return pd.DataFrame()

            # ✅ Empty Data Check
            if df_data.empty:
                print(f"No data found for {data_type} - {chart_type} in {month}/{year}")
                return pd.DataFrame()

            return df_data

    except Exception as e:
        print(f"Error fetching data from {data_type}: {e}")
        return pd.DataFrame()


# Generate and save the Monthly Pie chart 
def generate_chart(data_type, month, year, chart_type):

    df = fetch_data(data_type, month, year, chart_type)
    if df.empty:
        print(f"No data for {data_type} in {month}/{year}")
        return
    
    def save_chart(output_path, title):
        # Ensure 'static' folder exists
        os.makedirs('static', exist_ok=True)

        plt.savefig(output_path)
        plt.close()
        print(f"{filename} pie chart saved to {output_path}")

    if chart_type == "pie":
        if data_type == "expenses":
            title = f'Spend Distribution - {month}/{year}'
            filename = f'expenses_pie_{month}_{year}.png'
            label_col = 'category'
        elif data_type == "income":
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

        #save plot to static
        output_path = os.path.join('static', filename)
        save_chart(output_path, title)

    elif chart_type == "annual_bar":
        xlabel = "Month"
        ylabel = "Dollars"

        if data_type == "expenses":
            title = f"Spending Chart - {year}"
            filename = f"expenses_bar_{year}.png"
        elif data_type == "income":
            title = f"Income Chart - {year}"
            filename = f"income_bar_{year}.png"
        else:
            print("Invalid data types: 'expenses' or 'income'")

        if df.empty: 
            print(f"No data for {data_type}")
            return
        
        labels = df['month']
        data = df['total_amount']

        plt.figure(figsize=(10,6))
        plt.bar(labels, data, color='skyblue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)


        #save plot to static
        output_path = os.path.join('static', filename)
        save_chart(output_path, title)

        
    elif chart_type == "monthly_bar":
        xlabel = "Day"
        ylabel = "Dollars"
        if data_type == "expenses":
            title = f"Spending Chart - {month}/{year}"
            filename = f"expenses_bar_{month}_{year}.png"
        elif data_type == "income":
            title = f"Income Chart - {month}/{year}"
            filename = f"income_bar_{month}_{year}.png"
        else:
            print("Invalid data types: 'expenses' or 'income'")
        
        if df.empty: 
            print(f"No data for {data_type}")
            return
        
        labels = df['day']
        data = df['total_amount']

        plt.figure(figsize=(10,6))
        plt.bar(labels, data)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        #save plot to static
        output_path = os.path.join('static', filename)
        save_chart(output_path, title)

def main():
    # 🔎 Test generating different types of charts
    
    # Test Pie Chart for Expenses (January 2025)
    generate_chart(data_type="expenses", month=3, year=2025, chart_type="pie")
    
    # Test Annual Bar Chart for Income (2025)
    generate_chart(data_type="income", month=None, year=2025, chart_type="annual_bar")
    
    # Test Monthly Bar Chart for Expenses (March 2025)
    generate_chart(data_type="expenses", month=3, year=2025, chart_type="monthly_bar")


if __name__ == "__main__":
    main()



            



