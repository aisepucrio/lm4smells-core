from typing import List
from domain.entities.dl_classification import DLClassification
from infrastructure.config.db_connection import DatabaseConnection
import json


class DLClassificationRepository:
    def __init__(self) -> None:
        self.db_connection = DatabaseConnection()

    def save_all(self, classification: DLClassification) -> None:
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO dl_codes (
                        id, file_name, classification, model_used,
                        element_name, element_type, confidence_score, metrics, raw_code
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(classification.id),
                        classification.file_name,
                        classification.classification,
                        classification.model_used,
                        classification.element_name,
                        classification.element_type,
                        classification.confidence_score,
                        json.dumps(classification.metrics) if classification.metrics else None,
                        classification.raw_code,
                    ),
                )
                connection.commit()
                print(f"[INFO] DL Classification saved successfully: {classification.id}")
        except Exception as e:
            print(f"[ERROR] Failed saving DL classification: {e}")


    def get_all(self) -> List[dict]:
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    SELECT id, file_name, classification, model_used,
                           element_name, element_type, confidence_score,
                           metrics, raw_code, created_at FROM dl_codes
                    ORDER BY created_at DESC
                    """
                )
                rows = cursor.fetchall()

                results = []
                for row in rows:
                    result = {
                        "id": row[0],
                        "file_name": row[1],
                        "classification": row[2],
                        "model_used": row[3],
                        "element_name": row[4],
                        "element_type": row[5],
                        "confidence_score": row[6],
                        "metrics": json.loads(row[7]) if row[7] else None,
                        "raw_code": row[8],
                        "created_at": row[9],
                    }
                    results.append(result)

                return results
        except Exception as e:
            print(f"[ERROR] Failed retrieving DL classifications: {e}")
            return []

    def get_by_file_name(self, file_name: str) -> List[dict]:
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    SELECT id, file_name, classification, model_used,
                           element_name, element_type, confidence_score,
                           metrics, raw_code, created_at FROM dl_codes
                    WHERE file_name = ?
                    ORDER BY created_at DESC
                    """,
                    (file_name,),
                )
                rows = cursor.fetchall()

                results = []
                for row in rows:
                    result = {
                        "id": row[0],
                        "file_name": row[1],
                        "classification": row[2],
                        "model_used": row[3],
                        "element_name": row[4],
                        "element_type": row[5],
                        "confidence_score": row[6],
                        "metrics": json.loads(row[7]) if row[7] else None,
                        "raw_code": row[8],
                        "created_at": row[9],
                    }
                    results.append(result)

                return results
        except Exception as e:
            print(f"[ERROR] Failed retrieving DL classifications by file_name: {e}")
            return []
