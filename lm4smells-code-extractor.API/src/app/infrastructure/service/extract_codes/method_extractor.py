import ast 
from infrastructure.service.abstractions.code_extractor import CodeExtractor

class MethodExtractor(CodeExtractor):
    def visit_FunctionDef(self, node):

        self.items.append({
            "method_name": node.name,
            "lineno": node.lineno,
            "code": ast.unparse(node)
        })
        self.generic_visit(node)
