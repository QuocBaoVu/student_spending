from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from models import ExpenseSchema, IncomeSchema
from analysis import generate_chart
from db import get_db_connection
from sqlalchemy import text
import os

app = FastAPI()

# CORS Middleware for Cross-Origin Requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods: GET, POST, etc.
    allow_headers=["*"],  # Allows all headers
)

# Add a New Expense
@app.post("/expenses")
def add_expense(expense: ExpenseSchema):
    engine = get_db_connection()
    try:
        with engine.begin() as connection:
            sql = text("""
                INSERT INTO expenses (amount, category, date, notes) 
                VALUES (:amount, :category, :date, :notes)
            """)
            connection.execute(sql, {
                "amount": expense.amount,
                "category": expense.category,
                "date": expense.date,
                "notes": expense.notes
            })
            return {"message": "Expense added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get All Expenses
@app.get("/expenses")
def get_expenses():
    engine = get_db_connection()
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM expenses"))
            expenses = [dict(row._mapping) for row in result]  # ✅ Fixed row conversion
            return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add a New Income
@app.post("/income")
def add_income(income: IncomeSchema):
    engine = get_db_connection()
    try:
        with engine.begin() as connection:
            sql = text("""
                INSERT INTO income (amount, source, date, notes)
                VALUES (:amount, :source, :date, :notes)
            """)
            connection.execute(sql, {
                "amount": income.amount,
                "source": income.source,
                "date": income.date,
                "notes": income.notes
            })
            return {"message": "Income added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get All Income Entries
@app.get("/income")
def get_income():
    engine = get_db_connection()
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM income"))
            income = [dict(row._mapping) for row in result]  # ✅ Fixed row conversion
            return income
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/charts/monthly-pie")
def get_chart(data_type: str, month: int, year: int, chart_type: str):
    if data_type not in ["expenses", "income"]:
        raise HTTPException(status_code=400, detail="Invalid data type. Choose 'expenses' or 'income'.")

    if chart_type not in ["pie", "annual_bar", "monthly_bar"]:
        raise HTTPException(status_code=400, detail="Invalid chart type. Choose 'pie', 'annual_bar' or 'monthly_bar'.")
    generate_chart(data_type, month, year, chart_type)

    if chart_type == "pie":
        file_name = f"{data_type}_pie_{month}_{year}.png"
    elif chart_type =="annual_bar":
        file_name = f"{data_type}_bar_{year}.png"
    else:
        file_name = f"{data_type}_bar_{month}_{year}.png"

    file_path = os.path.join('static', file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Chart not found.")

    return FileResponse(file_path, media_type='image/png')


# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Spending Tracker API"}
