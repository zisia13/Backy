import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("pictures.db")
        self.cursor = self.connection.cursor()

        self.table_name = "hashes"
        self.column_name = "file_hash"

        #! create table if it not exists
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {self.column_name} TEXT NOT NULL
            )
            """
        )
        
    def save(self, val: str) -> None:
        self.cursor.execute(
            f"INSERT INTO {self.table_name} ({self.column_name}) VALUES (?)",
            (val,)
        )
        self.connection.commit()
    
    def delete(self, val: str) -> None: ... #todo implement in other projects
        # dont forget: self.connection.commit()
        
    def check(self, val: str) -> bool:
        """
        Returns true if the value exists else false
        """
        self.cursor.execute(f"SELECT 1 FROM {self.table_name} WHERE {self.column_name}=?", (val,))
        return self.cursor.fetchone() != None

    def close(self) -> None:
        self.connection.close()


if __name__ == "__main__":

    db = Database()
    db.save("Alina ist doof")
    print(db.check("Alina ist doof"))
    db.close()
