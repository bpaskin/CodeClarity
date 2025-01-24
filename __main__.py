from fileio.settings import Settings
from fileio.file_handler import FileHandler
import os
from parser.python_parser import PythonParser
from parser.java_parser import JavaParser
from parser.cobol_parser import CobolParser
from ai_modules.ollama_explanator import Ollama
from ai_modules.wxai import WxAI
from database.elasticsearch_db import Elasticsearch_db
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import streamlit as st
import streamlit.components.v1 as components
import json

# app settings
settings = Settings()
upload_settings = settings.read_sections("settings.config", "files")
max_files = int(settings.getSettingValue(upload_settings, "max_files"))
file_location = settings.getSettingValue(upload_settings, "file_location")

general_settings = settings.read_sections("settings.config", "general")
ai_to_use = settings.getSettingValue(general_settings, "ai_to_use")
db_to_use = settings.getSettingValue(general_settings, "db_to_use")


if ai_to_use == "ollama":
    ai = Ollama()

if ai_to_use == "wxai":
    ai = WxAI()

if db_to_use == "elastic":
    db = Elasticsearch_db()
    db.create_table()

# accepted types
accepted_python = ['.py']
accepted_java = ['.java']
accepted_cobol = ['.cbl', '.cpy', '.CBL', '.CPY']

def get_methods(method):
    explanation = ai.generate_explanation(method)
    return {"method_text":method, "method_explanation":explanation}

st.set_page_config(
    page_title="Code Clarity",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Code Clarity")

tab1, tab2 = st.tabs(["Upload Files", "Chat"])

with tab1:
    files = st.file_uploader("Upload your code files", accept_multiple_files=True, type=[".py", ".java", ".cbl", ".cpy"])
    layout = dict()

    for file in files:
        contents = file.getvalue().decode("utf-8")

        # time to parse the file
        file_name, file_extension = os.path.splitext(file.name)

        if file_extension in accepted_python:
            code_parser = PythonParser(contents)

        if file_extension in accepted_java:
            code_parser = JavaParser(contents)

        if file_extension in accepted_cobol:
            code_parser = CobolParser(contents)

        st.divider()
        with st.spinner("Processing program " + file_name):

            methods = code_parser.parse_functions() 
            methods = code_parser.return_function_text(methods)

            methods_explanation = []

            with ThreadPoolExecutor(max_workers = 10) as executor:
                results = executor.map(get_methods, methods.values())
               
            for result in results:
                methods_explanation.append(result)

            # add summary of file
            summary = ai.generate_summary_from_explanations(methods_explanation)

            labelTitle = file_name + " summary"
            components.html(
                f"""
                <script>
                    var elems = window.parent.document.querySelectorAll('div[class*="stExpander"] p');
                    var elem = Array.from(elems).find(x => x.innerText == '{labelTitle}');
                    elem.style.fontSize = '30px'
                </script>
                """, height=0
            )

            with st.expander(labelTitle, expanded=True):
                st.write(summary)

            with st.expander("Program Code and Explanation for " + file_name):
                for item in methods_explanation:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.code(item['method_text'])
                    with col2:
                        st.write(item['method_explanation'])
            
            # write to db
            # document =  { file_name: [{"summary": summary, "methods": methods_explanation}] }
            db.write_record(methods_explanation,filename=file_name)


with tab2:
    prompt = st.chat_input("Ask your question")
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")
        result = db.search_records(prompt)
        if result:
            overall_answer = ai.answer_user_query(question=prompt,references=result)
            st.write(f"Answer: {overall_answer}")
            with st.expander("Referenced functions"):
                for item in result:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Program name: "+item['_source']['program'])
                        st.code(item['_source']['method_text'])
                    with col2:
                        st.write(item['_source']['method_explanation'])
        else:
            st.write(f"I am sorry. I can't find any relevant information.")