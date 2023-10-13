from fastapi import FastAPI
import sqlite3

app = FastAPI(
    title="FastAPI Elastic Monitor Memory",
    description="develop by Jafar Esmaili",
    contract={
        "name": "Jafar Esmaili",
        "url": "devcoach.ir",
        "email": "jaffar9898@gmail.com",
    },
    version="0.0.1"
)


# Function to connect to the SQLite database
def connect_to_db():
    conn = sqlite3.connect('memory_usage.db')
    conn.row_factory = sqlite3.Row  # To get results as dictionaries
    return conn

@app.get("/")
async def root():
    return {"FastAPI Get Monitor data"}


@app.get("/memory-reports")
async def get_usage_items(skip: int = 0, limit: int = 10):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM memory_report LIMIT ? OFFSET ?", (limit, skip))
    items = cursor.fetchall()

    conn.close()

    return [dict(item) for item in items]
