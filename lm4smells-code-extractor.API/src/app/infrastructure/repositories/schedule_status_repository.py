from infrastructure.config.db_connection import DatabaseConnection
from typing import List

class ScheduleStatusRepository():
    def __init__(self) -> None:
        self.db_connection = DatabaseConnection()

    def get_schedule_status(self, task_id: List[str]):
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT status, task_type, task_id FROM tasks WHERE task_id = ANY(%s)""", (task_id,))
                rows = cursor.fetchall()

                return rows if rows else []
        except Exception as e:
            print(f"[ERROR] Failed retrieving schedule status: {e}")
            return "ERROR"
    

    def save_schedule_status(self, task_id: str, status: str, task_type: str):
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO tasks (task_id, status, task_type) 
                    VALUES (%s, %s, %s)
                    ON CONFLICT (task_id) 
                    DO UPDATE SET status = EXCLUDED.status
                """, (task_id, status, task_type))
                connection.commit()
        except Exception as e:
            print(f"[ERROR] Failed saving schedule status: {e}")
            raise e