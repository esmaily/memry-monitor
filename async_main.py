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
    __tablename__ = "memory_report"
    id = Column(Integer, primary_key=True, index=True)
    used = Column(Float)
    free = Column(Float)
    total = Column(Float)
    timestamp = Column(DateTime)

    # @validator("timestamp", pre=True)
    # def format_datetime(cls, value):
    #     return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


# Function to connect to the database
async def connect_to_db():
    await database.connect()


# Function to disconnect from the database
async def close_db_connection():
    await database.disconnect()


@app.on_event("startup")
async def startup():
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db_connection()


class MemoryReportResponse(BaseModel):
    id: int
    used: float
    free: float
    total: float
    timestamp: datetime

@app.get("/memory-reports/")
async def get_items():
    query = select([MemoryReport])
    results = await database.fetch_all(query)
    item_responses = [MemoryReportResponse(**result) for result in results]

    return item_responses
