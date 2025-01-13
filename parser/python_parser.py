import ast
from .parser import Parser
class PythonParser(Parser):
    def __init__(self, code_data):
        self.code_data = code_data
    def who_am_i(self):
        super().who_am_i()
#        print("I will be used to parse python programs")
    
    def parse_functions(self):
        """Parses Python functions from a given text."""
        super().parse_functions()
        tree = ast.parse(self.code_data)
        return tree

    def dump_info(self, tree):
        super().dump_info()

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                print(f"===========================")
                print(f"Function name: {node.name}")
                print(f"Arguments: {ast.dump(node.args)}")           

    def return_function_text(self, tree):
        super().return_function_text()
        functions = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name]=ast.unparse(node)
        return functions