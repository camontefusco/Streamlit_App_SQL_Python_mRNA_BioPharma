from sqlalchemy import create_engine, text
import pandas as pd
import getpass

schema = "mRNA_BioPharma_DB"
host = "127.0.0.1"
user = "root"
port = 3306

try:
    password = getpass.getpass("Enter password: ")
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema}")
    engine.connect().close()
    print("✅ Database engine created successfully.")
except Exception as e:
    print(f"❌ Could not create engine: {e}")

def run_query(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        if result.returns_rows:
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        return None

def execute_command(query, params=None):
    with engine.begin() as conn:
        conn.execute(text(query), params or {})