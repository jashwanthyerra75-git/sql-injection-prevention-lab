
import sqlite3

def setup_database():
    db = sqlite3.connect("users.db")
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL
        )
    """)
    db.execute(
        "INSERT OR IGNORE INTO users (username) VALUES (?)",
        ("ravi",)
    )
    db.execute(
        "INSERT OR IGNORE INTO users (username) VALUES (?)",
        ("priya",)
    )
    db.commit()
    return db

def main():
    db = setup_database()

    print("\n=== User Database Security Lab ===")
    print("1. Search for a user")
    print("2. List all usernames")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        username = input("Enter username: ")
        result = db.execute(
            "SELECT id, username FROM users WHERE username = ?",
            (username,)
        ).fetchall()
        print("Results:", result)

    elif choice == "2":
        result = db.execute(
            "SELECT id, username FROM users"
        ).fetchall()
        print("Users:", result)

    elif choice == "3":
        print("Goodbye!")

    else:
        print("Invalid option.")

    db.close()

if __name__ == "__main__":
    main()
