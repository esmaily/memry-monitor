from fastapi.testclient import TestClient
import pytest
from async_main import app
from databases import Database

# Initialize a test client for the FastAPI app
client = TestClient(app)

# Database connection URL for testing
TEST_DATABASE_URL = "sqlite:///test_memory_usage.db"

# Define test cases
@pytest.fixture(scope="module")
def test_database():
    """
    Create a test database for testing the application.
    """
    test_db = Database(TEST_DATABASE_URL)

    yield test_db
    test_db.disconnect()


@pytest.fixture(autouse=True)
def clear_database(test_database):
    """
    Clear the test database before each test.
    """
    test_db = test_database

    query = "DELETE FROM memory_report"
    test_db.execute(query)


@pytest.mark.asyncio
async def test_monitor_memory_usage(test_database):
    """
    Test monitoring memory usage and writing to the database.
    """
    # Simulate memory usage monitoring and write to the test database
    data_to_insert = {
        "used": 1024.0,  # Replace with your actual memory usage data
        "free": 2048.0,
        "total": 3072.0,
    }

    insert_query = "INSERT INTO memory_report (used, free, total) VALUES (:used, :free, :total)"

    await test_database.execute(insert_query, values=data_to_insert)

    # Check if the data was successfully inserted
    query = "SELECT * FROM memory_report"
    result =  await test_database.fetch_one(query)

    assert result is not None
    assert result["used"] == data_to_insert["used"]
    assert result["free"] == data_to_insert["free"]
    assert result["total"] == data_to_insert["total"]


@pytest.mark.asyncio
async def test_get_memory_reports(test_database):
    """
    Test retrieving memory usage reports from the database.
    """
    # Simulate inserting data into the test database (you can use the same method as in the previous test)

    # Simulate retrieving data from the API endpoint
    response =   client.get("/memory-reports/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    # You can add more assertions to validate the response data as needed

# Add more test cases as required for your application
