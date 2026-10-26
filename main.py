import sqlite3
import hashlib
import secrets
import hmac
import getpass

DB_NAME = "users.db"
ITERATIONS = 600_000


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )
    return salt.hex(), password_hash.hex()


def setup_database():
    with sqlite3.connect(DB_NAME) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        users = [
            ("ravi", "RaviDemo!42"),
            ("priya", "PriyaDemo!57")
        ]

        for username, password in users:
            salt, password_hash = hash_password(password)
            db.execute("""
                INSERT OR IGNORE INTO accounts
                (username, salt, password_hash)
                VALUES (?, ?, ?)
            """, (username, salt, password_hash))


def login():
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    with sqlite3.connect(DB_NAME) as db:
        row = db.execute("""
            SELECT salt, password_hash
            FROM accounts
            WHERE username = ?
        """, (username,)).fetchone()

    if row is None:
        print("Login failed.")
        return

    salt = bytes.fromhex(row[0])
    expected_hash = bytes.fromhex(row[1])

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    if hmac.compare_digest(actual_hash, expected_hash):
        print("Login successful!")
    else:
        print("Login failed.")


def main():
    setup_database()

    print("\n=== Secure Login Lab ===")
    print("1. Login")
    print("2. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        login()
    elif choice == "2":
        print("Goodbye!")
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
    
