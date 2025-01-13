from .database import Database
from elasticsearch import Elasticsearch, RequestError
from sentence_transformers import SentenceTransformer
from fileio.settings import Settings

from ai_modules.ollama_explanator import Ollama

class Elasticsearch_db(Database): 

    def  __init__(self):
        settings = Settings()
        es_settings = settings.read_sections("settings.config", "elastic")
        es_url = settings.getSettingValue(es_settings, "url")
        es_username = settings.getSettingValue(es_settings, "username")
        es_password = settings.getSettingValue(es_settings, "password")
        es_certificate = settings.getSettingValue(es_settings, "certificate")
        es_index = settings.getSettingValue(es_settings, "index")
        embedding_model = settings.getSettingValue(es_settings, "embedding_model")

        self.client =  Elasticsearch(
            es_url,
            ca_certs=es_certificate,
            basic_auth=(es_username, es_password),
        )
        self.index = es_index
        self.embedding_model = SentenceTransformer(embedding_model)

    def logon(self, url, username, password, certificate):
        self.client = Elasticsearch(
            url,
            ca_certs=certificate,
            basic_auth=(username, password)
        )       

    def write_record(self, data,filename):
        operations = []
        for document in data:
            operations.append({'index': {'_index': self.index}})
            operations.append({
                **document,
                'my_vector':self.embedding_model.encode(document['method_explanation']),
                'program':filename
            })
        return self.client.bulk(operations=operations)

    def read_record(self, data):
        return self.client.search(
            index=self.index,
            query={
                "match": {
                    data
                }
            }
        )

    def search_records(self, prompt):
        # First we decide whether to use vector search or database query
        ai = Ollama()
        decide_prompt = f"""Answer with either 0 or 1. You should 0 if the answer is (`vector_search`) and return 1 if the answer is (`database_query`. If you are not sure, return 0. Only responde with the number. * `database_query`: The question is likely to be answered via a database query. The question may refer to a property in the mapping in the database. * `vector_search`: The question is likely to be answered via a vector search. The question is general, and the answer may require drawing logical steps or drawing relations.

        [Example 1]
        [input]: How many functions are in the database?
        [output]: 1
        [Example 2]
        [input]: Explain the relationship between program A and program B.
        [output]: 0
        [Example 3]
        [input]: are there functions related to setting up SSL connections?
        [output]: 0
        [Example 4]
        [input]: what functions do you have?
        [output]: 1
        """

        decide_result = ai.handle_general_requst(decide_prompt)

        while True:
            match decide_result:
                case '0':
                    query_vector = self.embedding_model.encode(prompt)

                    response = self.client.search(
                        knn={
                            "field": "my_vector",
                            "query_vector": query_vector,
                            "num_candidates": 50,
                            "k": 10,
                        },
                        index=self.index,
                        source=["method_explanation", "method_text", "program"],
                        size=5,
                        min_score=0.6,
                    )
                    break
                case '1':
                    # Use llm to translate natural language to elastic search query strings. then execute the elastic search query
                    mapping = {
                        "mappings": {
                            "properties": {
                                "my_vector": {
                                    "type": "dense_vector",
                                    "dims": 384,
                                    "index": True,
                                    "similarity": "cosine",
                                },
                                "method_text": {"type": "text"},
                                "method_explanation": {"type": "text"},
                                "program":{"type": "text"},
                            }
                        }
                    }
                    llm_prompt = f'''Given the mapping delimited by triple backticks ```{mapping}``` translate the text delimited by triple quotes in a valid Elasticsearch DSL query """{prompt}""". Give me only the json code part of the answer. Compress the json output removing spaces.
                    
                    [Example 1]
                    [input]: Show all the methods from the program named Hello
                    [output]: {{"query":{{"match_phrase":{{"program":"Hello"}}}}}}
                    [Example 2]
                    [input]: show me all the programs.
                    [output]: {{"query":{{"match_all":{{}}}}}}
                    '''

                    es_query = ai.handle_general_requst(llm_prompt)

                    # es_query = es_query.replace("```json\n?|```", ''), known issue for model trained with Markddown
                    es_query = es_query.replace("```json", '').replace("```", '')

                    response = self.client.search(
                        index=self.index,
                        body=es_query
                    )

                    if len(response["hits"]["hits"]) ==0:
                        # perform vector search
                        decide_result='0'
                    else:
                        break        
                case '_':
                    break

       
        return response["hits"]["hits"]

    def delete_record(self, id):
        return self.client.delete(
            index=self.index, doc_type="_doc", id=id
        )

    def create_table(self):
        try :
            mapping = {
                "mappings": {
                    "properties": {
                        "my_vector": {
                            "type": "dense_vector",
                            "dims": 384,
                            "index": True,
                            "similarity": "cosine",
                        },
                        "method_text": {"type": "text"},
                        "method_explanation": {"type": "text"},
                        "program":{"type": "text"},
                    }
                }
            }
            resp = self.client.indices.create(
                index=self.index,
                body=mapping
            )

        # Index already exists
        except RequestError as e:
            pass