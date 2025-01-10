from fastapi import FastAPI, HTTPException
from models import ExpenseSchema, IncomeSchema
from db import get_db_connection


app = FastAPI()

@app.post("/expenses")
def add_expense(expense: ExpenseSchema):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO expenses (amount, category, date, notes) VALUES (%s, %s, %s, %s)"
        values = (expense.amount, expense.category, expense.date, expense.notes)
        cursor.execute(sql, values)
        connection.commit()
        return {"message" : "Expense added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

@app.get("/expenses")
def get_expenses():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM expenses")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

@app.post("/income")
def add_income(income: IncomeSchema):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO (amount, source, date, notes) VALUES (%s, %s, %s, %s)"
        values = (income.amount, income.source, income.date, income.notes)
        cursor.execute(sql, values)
        connection.commit()
        return {"message": "income added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

@app.get("/income")
def get_income():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM income")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

@app.get('/')
def read_root():
    return {"message" : "Welcome"}




