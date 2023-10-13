import psutil
import time
import sqlite3

conn = sqlite3.connect('memory_usage.db')
cursor = conn.cursor()


def init_database():
    # Create a table for memory data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory_report (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            used REAL,
            free REAL,
            total REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    return conn


def store_data(params: dict):
    init_database()
    cursor.execute('''
        INSERT INTO memory_report (used, free, total)
        VALUES (?, ?, ?)
    ''', (params['used'], params['free'], params['total']))
    conn.commit()


def log_pretty(data):
    print('Start Monitoring.')
    log_entry = f"Total Memory: {data['total']} MB, Used Memory: {data['used']} MB, Free Memory: {data['free']} MB"
    print(log_entry)


def log_memory_usage():
    memory = psutil.virtual_memory()
    total = memory.total / (1024 * 1024)
    used = memory.used / (1024 * 1024)
    free = memory.available / (1024 * 1024)
    data = {
        "total": "{:.2f}".format(total),
        "used": "{:.2f}".format(used),
        "free": "{:.2f}".format(free)
    }
    store_data(data)
    log_pretty(data)


if __name__ == "__main__":
    try:
        while True:
            log_memory_usage()
            time.sleep(60)  # Log memory usage every minute (60 seconds)
    except KeyboardInterrupt:
        print("Monitoring stopped.")
