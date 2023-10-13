from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, select, DateTime
from databases import Database
from pydantic import BaseModel,validator
from datetime import datetime

DATABASE_URL = "sqlite:///./memory_usage.db"
database = Database(DATABASE_URL)

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


# Define a SQLAlchemy model
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MemoryReport(Base):
    """
        Represents a memory report entity.

        Attributes:
            id (int): The unique identifier for the memory report.
            used (float): The amount of used memory.
            free (float): The amount of free memory.
            total (float): The total available memory.
            timestamp (datetime): The timestamp of the memory report.
    """
    __tablename__ = "memory_report"
    id = Column(Integer, primary_key=True, index=True)
    used = Column(Float)
    free = Column(Float)
    total = Column(Float)
    timestamp = Column(DateTime)



# Function to connect to the database
async def connect_to_db():
    """
       Asynchronously connect to the database.
     """
    await database.connect()


# Function to disconnect from the database
async def close_db_connection():
    """
       Asynchronously disconnect to the database.
    """
    await database.disconnect()


@app.on_event("startup")
async def startup():
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db_connection()


class MemoryReportResponse(BaseModel):
    """
        Represents a response model for a memory report.

        Attributes:
            id (int): The unique identifier for the memory report.
            used (float): The amount of used memory.
            free (float): The amount of free memory.
            total (float): The total available memory.
            timestamp (datetime): The timestamp of the memory report.
    """
    id: int
    used: float
    free: float
    total: float
    timestamp: datetime

@app.get("/memory-reports/")
async def get_items():
    """
        Retrieve a list of memory reports from the database.

        Returns:
            List[MemoryReportResponse]: A list of memory report responses.
    """
    query = select([MemoryReport])
    results = await database.fetch_all(query)
    item_responses = [MemoryReportResponse(**result) for result in results]

    return item_responses
