import sqlite3
from infrastructure.config.settings import settings

class DatabaseConnection:
    def __init__(self, db_path = settings.db_path):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()

                cursor.execute("""
                                CREATE TABLE IF NOT EXISTS code_smells_v1 (
                                smell_type TEXT NOT NULL DEFAULT 'nd', 
                                explanation TEXT NOT NULL DEFAULT 'nd',
                                file_name TEXT NOT NULL,
                                model TEXT NOT NULL,
                                programming_language TEXT NOT NULL,
                                class_name TEXT,
                                method_name TEXT,
                                analyse_type TEXT NOT NULL DEFAULT 'nd',
                                code TEXT NOT NULL,
                                prompt_type TEXT NOT NULL DEFAULT 'nd',
                                prompt TEXT NOT NULL,
                                is_composite_prompt BOOLEAN NOT NULL,
                                code_metric TEXT NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                PRIMARY KEY (file_name, model, prompt, is_composite_prompt)
                            )
                        """)
                
                connection.commit()
                print("[INFO] Database successfully initialized.")
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to initialize the database: {e}")
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)