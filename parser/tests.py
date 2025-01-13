from python_parser import PythonParser
from java_parser import JavaParser

PYTHON_CODE_DATA = """
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y
"""

JAVA_CODE_DATA = """
// Assisted by WCA@IBM
// Latest GenAI contribution: ibm/granite-8b-code-instruct

public class Person {
    private String name;
    private String email;
    private String phone;

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone() {
        return this.phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }
}

"""

python_parser = PythonParser(PYTHON_CODE_DATA)
python_parser.who_am_i()
tree = python_parser.parse_functions()
python_parser.dump_info(tree)
functions = python_parser.return_function_text(tree)
# for function, function_body in functions.items():
#     # Do something, send to LLM for analysis
#     print(function, function_body)

# java_parser = JavaParser(JAVA_CODE_DATA)
# java_parser.who_am_i()
# tree = java_parser.parse_functions()
# java_parser.dump_info(tree)
# functions = java_parser.return_function_text(tree)
# # for function, function_body in functions.items():
# #     # Do something, send to LLM for analysis
# #     print(function, function_body)