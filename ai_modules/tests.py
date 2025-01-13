from wxai import WxAI
from ollama_explanator import Ollama

CODE_DATA = """
name = "Brian"
print(name)
"""

# MODEL_NAME = "mistralai/mixtral-8x7b-instruct-v01"
# API_KEY = "EXAMPLE_API_KEY"
# PROJECT_ID = "EXAMPLE_PROJECT_ID"
# wxai_child = WxAI(MODEL_NAME, CODE_DATA, API_KEY, PROJECT_ID)
# wxai_child.greet()
# wxai_child.generate_explanation()

MODEL_NAME = "llama3.1"
ollama_child = Ollama(MODEL_NAME, CODE_DATA)
ollama_child.greet()
ollama_child.generate_explanation()