import sqlite3

class Database:
    def __init__(self, db_path: str = "pictures.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        #! table name
        self.table_name = "data"

        #! column names
        self.hash_column_name = "file_hash"
        self.filename_column_name = "file_name"

        #! create table if it not exists
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {self.hash_column_name} TEXT,
                {self.filename_column_name} TEXT
            )
            """
        )
        
    def save(self, column_name: str, val: str) -> None:
        self.cursor.execute(
            f"INSERT INTO {self.table_name} ({column_name}) VALUES (?)",
            (val,)
        )
        self.connection.commit()
    
    def delete(self, column_name: str, val: str) -> None: ... #todo implement in other projects
        # dont forget: self.connection.commit()
        
    def check(self, column_name: str, val: str) -> bool:
        """
        Returns true if the value exists else false
        """
        self.cursor.execute(f"SELECT 1 FROM {self.table_name} WHERE {column_name}=?", (val,))
        return self.cursor.fetchone() != None

    def close(self) -> None:
        self.connection.close()


if __name__ == "__main__":

    db = Database()
    db.save("Alina ist doof")
    print(db.check("Alina ist doof"))
    db.close()
