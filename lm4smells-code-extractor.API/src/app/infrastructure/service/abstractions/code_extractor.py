import ast 
from typing import Dict, List
from infrastructure.service.metric_codes.radon_analyzer import RadonAnalyzer

class CodeExtractor(ast.NodeVisitor):
    def __init__(self):
        self.items = []
        self.metric_codes = RadonAnalyzer()
    
    def _get_code(self, file_content: str) -> List[str]:
        self.items = []
        tree = ast.parse(file_content)
        self.visit(tree)
        return self.items

    def extract(self, code_files: List[Dict]) -> List[Dict]:
        all_items = []

        for codes in code_files:
            programming_language = codes['programming_language']
            file_name = codes['file_name']
            code = codes['code']
            items = self._get_code(code)

            for item in items:
                metric_result = self.metric_codes.analyze(item['code'])

                all_items.append({
                    "file_name": file_name,
                    "programming_language": programming_language,
                    **item,
                    "code_metric": metric_result
                })

        return all_items

    