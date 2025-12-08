from infrastructure.config.db_connection import DatabaseConnection
from typing import List

class ScheduleStatusRepository():
    def __init__(self) -> None:
        self.db_connection = DatabaseConnection()

    def update_schedule_status(self, task_id: str, status: str):
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE tasks SET status = 'completed' WHERE task_id = %s
                """, (task_id,))
                connection.commit()
        except Exception as e:
            print(f"[ERROR] Failed saving schedule status: {e}")
            raise e