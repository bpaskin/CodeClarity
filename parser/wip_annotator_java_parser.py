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

        lex = None
        methods = {}
        codelines = self.code_data.split('\n')
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            startpos, endpos, startline, endline = self.get_method_start_end(tree,method_node)
            method_text, startline, endline, lex = self.get_method_text(codelines,startpos, endpos, startline, endline, lex)
            methods[method_node.name] = method_text
        return methods
    
    '''
    The following are helper methods to unparse java code 
    '''
    def get_method_start_end(self,tree,method_node):
        startpos  = None
        endpos    = None
        startline = None
        endline   = None
        for path, node in tree:
            if startpos is not None and method_node not in path:
                endpos = node.position
                endline = node.position.line if node.position is not None else None
                break
            if startpos is None and node == method_node:
                startpos = node.position
                startline = node.position.line if node.position is not None else None
        return startpos, endpos, startline, endline


    def get_method_text(self,codelines,startpos, endpos, startline, endline, last_endline_index):
        if startpos is None:
            return "", None, None, None
        else:
            startline_index = startline - 1 
            endline_index = endline - 1 if endpos is not None else None 

            # 1. check for and fetch annotations
            if last_endline_index is not None:
                for line in codelines[(last_endline_index + 1):(startline_index)]:
                    if "@" in line: 
                        startline_index = startline_index - 1
            meth_text = "<ST>".join(codelines[startline_index:endline_index])
            meth_text = meth_text[:meth_text.rfind("}") + 1] 

            # 2. remove trailing rbrace for last methods & any external content/comments
            # if endpos is None and 
            if not abs(meth_text.count("}") - meth_text.count("{")) == 0:
                # imbalanced braces
                brace_diff = abs(meth_text.count("}") - meth_text.count("{"))

                for _ in range(brace_diff):
                    meth_text  = meth_text[:meth_text.rfind("}")]    
                    meth_text  = meth_text[:meth_text.rfind("}") + 1]     

            meth_lines = meth_text.split("<ST>")  
            meth_text  = "".join(meth_lines)                   
            last_endline_index = startline_index + (len(meth_lines) - 1) 

            return meth_text, (startline_index + 1), (last_endline_index + 1), last_endline_index