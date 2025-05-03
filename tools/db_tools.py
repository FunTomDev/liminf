import os
import subprocess
import argparse
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DUMP_FILE = "db.dump"

def export_db():
    cmd = [
        "pg_dump",
        "-U", DB_USER,
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-d", DB_NAME,
        "-Fc",
        "-f", DUMP_FILE,
    ]
    print(f"Exporting database '{DB_NAME}' to {DUMP_FILE}...")
    subprocess.run(cmd, check=True)
    print("Done!")

def import_db():
    cmd = [
        "pg_restore",
        "-U", DB_USER,
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-d", DB_NAME,
        "-c",  # Clean (drop) before recreate
        DUMP_FILE,
    ]
    print(f"Importing dump from {DUMP_FILE} to database '{DB_NAME}'...")
    subprocess.run(cmd, check=True)
    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PostgreSQL DB dump/import")
    parser.add_argument("action", choices=["export", "import"], help="What to do")

    args = parser.parse_args()
    if args.action == "export":
        export_db()
    elif args.action == "import":
        import_db()
