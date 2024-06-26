import sqlite3
import json

def create_list(list_name):
    """Creates a new list object."""
    return {"name": list_name, "items": []}

def save_list(list_data):
    """Saves the list to the database."""
    try:
        with sqlite3.connect("slacksync.db") as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS lists
                         (name TEXT PRIMARY KEY, items TEXT)''')

            items_json = json.dumps(list_data["items"])  # Serialize items to JSON

            c.execute(
                "INSERT OR REPLACE INTO lists VALUES (?, ?)",
                (list_data["name"], items_json),
            )
    except sqlite3.Error as e:
        print(f"Error saving list: {e}")

def get_list(list_name):
    """Retrieves a list from the database."""
    try:
        with sqlite3.connect("slacksync.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM lists WHERE name=?", (list_name,))
            row = c.fetchone()
            if row:
                items = json.loads(row[1])  # Deserialize items from JSON
                return {"name": row[0], "items": items}
    except sqlite3.Error as e:
        print(f"Error getting list: {e}")

    return None  # List not found

