import ast
from infrastructure.service.abstractions.code_extractor import CodeExtractor

class ClassExtractor(CodeExtractor):
    def visit_ClassDef(self, node):
        
        self.items.append({
            "class_name": node.name,
            "lineno": node.lineno,
            "code": ast.unparse(node)
        })
        self.generic_visit(node)
