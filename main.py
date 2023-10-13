from fastapi import FastAPI
import sqlite3

app = FastAPI(
    title="FastAPI Monitor Memory",
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
    """
     Connect to the SQLite database and configure the row factory to return results as dictionaries.

     Returns:
         sqlite3.Connection: A connection to the SQLite database.
     """
    conn = sqlite3.connect('memory_usage.db')
    conn.row_factory = sqlite3.Row  # To get results as dictionaries
    return conn

@app.get("/")
async def root():
    return {"FastAPI Get Monitor data"}


@app.get("/memory-reports")
async def get_usage_items(skip: int = 0, limit: int = 10):
    """
       Retrieve memory reports from the SQLite database.

       Args:
           skip (int, optional): Number of records to skip. Defaults to 0.
           limit (int, optional): Maximum number of records to retrieve. Defaults to 10.

       Returns:
           list: A list of dictionaries representing memory report data.
    """

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM memory_report LIMIT ? OFFSET ?", (limit, skip))
    items = cursor.fetchall()

    conn.close()

    return [dict(item) for item in items]
