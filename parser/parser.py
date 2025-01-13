from abc import ABC, abstractmethod
class Parser(ABC):
    @abstractmethod
    def who_am_i(self):
        print(f"Hello I am Peter Parser.")

    @abstractmethod
    def parse_functions(self):
        self.who_am_i()
#        print(f"Parsing through...\n\n{self.code_data}")

    @abstractmethod
    def dump_info(self):
        print("Dumping info:")

    # Assisted by WCA@IBM
    # Latest GenAI contribution: ibm/granite-8b-code-instruct
    @abstractmethod
    def return_function_text(self):
        """
        Returns a dictionary of function names and their corresponding bodies.

        Parameters:
        self (object): The instance of the class calling the function.

        Returns:
        dict: A dictionary containing function names as keys and their corresponding bodies as values.
        """
#        print("Return functions text")
        functions = {"exampleFunctionName":"exampleFunctionBody"}
        return functions
