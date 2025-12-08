from typing import List
from domain.entities.smell_occurrence import SmellOccurrence
from domain.entities.ml_classification import MLClassification
from domain.entities.dl_classification import DLClassification
from domain.entities.lm_codes import LMCode
from infrastructure.config.db_connection import DatabaseConnection
from dataclasses import asdict
import json

class SmellRepository():
    def __init__(self) -> None:
        self.db_connection = DatabaseConnection()

    def save_all(self, smells: SmellOccurrence) -> None:
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO ast_codes (
                        id, smell_type, description, location, metrics, 
                        definition_author, threshold_used, detected_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(smells.id),
                    str(smells.smell_type),
                    smells.description,
                    json.dumps(asdict(smells.location)),
                    json.dumps(asdict(smells.metrics)),
                    smells.definition_author,
                    smells.threshold_used,
                    smells.detected_at
                ))
                connection.commit()
                print(f"[INFO] Answer saved successfully: {smells.id}")
        except Exception as e:
            print(f"[ERROR] Failed saving smells: {e}")

    def get_ast_codes_by_id(self, id: str) -> List[SmellOccurrence]:
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT id, smell_type, description, 
                                    location, metrics, definition_author, threshold_used, 
                                    detected_at, created_at 
                                    FROM ast_codes WHERE id = %s""", (id,))
                rows = cursor.fetchall()

                return [SmellOccurrence(
                    id=row["id"],
                    smell_type=row["smell_type"],
                    description=row["description"],
                    location=json.loads(row["location"]),
                    metrics=json.loads(row["metrics"]),
                    definition_author=row["definition_author"],
                    threshold_used=row["threshold_used"],
                    detected_at=row["detected_at"],
                    created_at=row["created_at"]
                ) for row in rows]

        except Exception as e:
            print(f"[ERROR] Failed retrieving smells: {e}")
            return []

    def get_ml_codes_by_id(self, id: str) -> List[MLClassification]:
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT id, file_name, classification, model_used, 
                                    element_name, element_type, confidence_score, 
                                    metrics, created_at 
                                    FROM ml_codes WHERE id = %s""", (id,))
                rows = cursor.fetchall()

                return [MLClassification(
                    id=row["id"],
                    file_name=row["file_name"],
                    classification=row["classification"],
                    model_used=row["model_used"],
                    element_name=row["element_name"],
                    element_type=row["element_type"],
                    confidence_score=row["confidence_score"],
                    metrics=json.loads(row["metrics"]) if row["metrics"] else None,
                    created_at=row["created_at"]
                ) for row in rows]
        except Exception as e:
            print(f"[ERROR] Failed retrieving codes: {e}")
            return []

    def get_dl_codes_by_id(self, id: str) -> List[DLClassification]:
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT id, file_name, classification, model_used, 
                                    element_name, element_type, confidence_score, 
                                    metrics, raw_code, created_at 
                                    FROM dl_codes WHERE id = %s""", (id,))
                rows = cursor.fetchall()

                return [DLClassification(
                    id=row["id"],
                    file_name=row["file_name"],
                    classification=row["classification"],
                    model_used=row["model_used"],
                    element_name=row["element_name"],
                    element_type=row["element_type"],
                    confidence_score=row["confidence_score"],
                    metrics=json.loads(row["metrics"]) if row["metrics"] else None,
                    raw_code=row["raw_code"],
                    created_at=row["created_at"]
                ) for row in rows]
        except Exception as e:
            print(f"[ERROR] Failed retrieving codes: {e}")
            return []

    def get_lm_codes_by_id(self, id: str) -> List[LMCode]:
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT task_id, smell_type, explanation, file_name, model, programming_language,
                                    class_name, method_name, analyse_type, code, prompt_type, prompt,
                                    is_composite_prompt, code_metric, created_at
                                    FROM code_smells_v1 WHERE task_id = %s""", (id,))

                rows = cursor.fetchall()

                return [LMCode(
                    id=row["task_id"],
                    smell_type=row["smell_type"],
                    explanation=row["explanation"],
                    file_name=row["file_name"],
                    model=row["model"],
                    programming_language=row["programming_language"],
                    class_name=row["class_name"],
                    method_name=row["method_name"],
                    analyse_type=row["analyse_type"],
                    code=row["code"],
                    prompt_type=row["prompt_type"],
                    prompt=row["prompt"],
                    is_composite_prompt=bool(row["is_composite_prompt"]),
                    code_metric=row["code_metric"],
                    created_at=row["created_at"],
                ) for row in rows]

        except Exception as e:
            print(f"[ERROR] Failed retrieving codes: {e}")
            return []

