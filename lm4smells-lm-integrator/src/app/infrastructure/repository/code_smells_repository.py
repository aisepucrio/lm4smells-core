import sqlite3
import json
from typing import Dict, Optional
from infrastructure.config.db_connection import DatabaseConnection
from domain.entities.code_smell import CodeSmell
from infrastructure.repository.icode_smell_repository import ICodeSmellsRepository

class CodeSmellsRepository(ICodeSmellsRepository):
    def __init__(self):
        self.db_connection = DatabaseConnection() 

    def persist_lm_result(self, code_smell: CodeSmell):
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO code_smells_v1 (smell_type, explanation, file_name, model, programming_language, class_name,
                              method_name, analyse_type, code, prompt_type, prompt, is_composite_prompt, code_metric)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (code_smell.smell_type, code_smell.explanation, code_smell.file_name, code_smell.model, 
                      code_smell.programming_language, code_smell.class_name, code_smell.method_name, code_smell.analyse_type, 
                      code_smell.code, code_smell.prompt_type, code_smell.prompt, code_smell.is_composite_prompt, json.dumps(code_smell.code_metric)))

                connection.commit()
                print(f"[INFO] Answer saved successfully: {code_smell.file_name}")
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to save result to database: {e}")

