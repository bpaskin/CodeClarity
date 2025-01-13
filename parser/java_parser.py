import javalang
from .parser import Parser

class JavaParser(Parser):
    def __init__(self, code_data):
        self.code_data = code_data
    def who_am_i(self):
        super().who_am_i()
        print("I will be used to parse java programs")
    
    def parse_functions(self):
        """Parses java functions from a given text."""
        super().parse_functions()
        tree = javalang.parse.parse(self.code_data)
        return tree


    def dump_info(self, tree):
        super().dump_info()
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            print(f"===========================")
            print(f"Function name: {node.name}")
            print(node.parameters)

    # Java unparse documentation: https://github.com/c2nes/javalang/issues/49    
    def return_function_text(self,tree):
        super().return_function_text()
        methods = {}
        for _, node in tree.filter(javalang.tree.MethodDeclaration):
            start, end = self.__get_start_end_for_node(tree,node)
            methods[node.name] = self.__get_string(self.code_data,start, end)     
        return methods
    
    '''
    The following are helper methods to unparse java code 
    '''
    def __get_start_end_for_node(self,tree,node_to_find):
        start = None
        end = None
        for path, node in tree:
            if start is not None and node_to_find not in path:
                end = node.position
                return start, end
            if start is None and node == node_to_find:
                start = node.position
        return start, end


    def __get_string(self,data,start, end):
        if start is None:
            return ""

        # positions are all offset by 1. e.g. first line -> lines[0], start.line = 1
        end_pos = None

        if end is not None:
            end_pos = end.line - 1

        lines = data.splitlines(True)
        string = "".join(lines[start.line:end_pos])
        string = lines[start.line - 1] + string

        # When the method is the last one, it will contain a additional brace
        if end is None:
            left = string.count("{")
            right = string.count("}")
            if right - left == 1:
                p = string.rfind("}")
                string = string[:p]

        return string