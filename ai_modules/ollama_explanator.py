from .explanator import Explanator
from ollama import generate, Client
from fileio.settings import Settings

# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-8b-code-instruct
'''
This code defines a class called Ollama which inherits from the Explanator class. The __init__ method initializes the class with a model_name and code_data. The who_am_i and greet methods are inherited from the Explanator class and simply call their respective methods. The generate_explanation method generates an explanation for the provided code_data using the generate function from the model_name.
'''
class Ollama(Explanator):
    def __init__(self):
        settings = Settings()
        ollama_settings = settings.read_sections("settings.config", "ollama")
        ollama_model = settings.getSettingValue(ollama_settings, "model_name")
        ollama_host = settings.getSettingValue(ollama_settings, "host")

        self.model_name = ollama_model
        self.host = ollama_host
        self.client = Client( host='http://' + self.host )

    def who_am_i(self):
        super().who_am_i()

    def greet(self):
        super().greet()
    
    def generate_explanation(self, code_data):
        super().generate_explanation(code_data)
        explanation_request = f"""You are an expert software developer. In a sentence or two, explain what does the code do.

        {code_data}
        """

        response = self.client.generate(self.model_name, explanation_request)
        # print(response['response'])
        return response['response']
    
    def generate_summary_from_explanations(self,method_explanations):
        # Expecting explanations array with format ["explanation_1","explanation_2"]
        super().generate_summary_from_explanations()
        explanations_string = ""	
        for method_explanation in method_explanations:	
            explanations_string += method_explanation['method_explanation']

        summary_request = f"""You are an expert software developer. You have already generated explanations of individual functions in a file. Now given the explanations, clearly and succintly summarize the purpose of the file.

        [INPUT]
        {explanations_string}
        [SUMMARY]
        """

        response = self.client.generate(self.model_name, summary_request)
        # print(response['response'])
        return response['response']
    
    def answer_user_query(self,question,references):	

        reference_string = ""	
        for reference in references:	
            reference_string += f"\n{reference['_source']['method_explanation']}\n"	

        query_request = f"""You are an experienced programmer. Please answer the following question to the best of your ability. Only answer based on the references. If an answer can not be derived from the references, say "I am not sure!". 	
        [Question]	
        {question}	
        [Reference]	
        {reference_string}	
        [Answer]	
        """	

        response = self.client.generate(self.model_name, query_request)	
        # print(response['response'])	
        return response['response']
    
    def handle_general_requst(self,request):
        response = self.client.generate(self.model_name, request)	
        return response['response']