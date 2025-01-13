from .explanator import Explanator
import requests
from fileio.settings import Settings

class WxAI(Explanator):
    def __init__(self):
        settings = Settings()
        wxai_settings = settings.read_sections("settings.config", "watsonx.ai")
        wxai_apikey = settings.getSettingValue(wxai_settings, "api_key")
        wxai_project = settings.getSettingValue(wxai_settings, "project_id")
        wxai_model = settings.getSettingValue(wxai_settings, "model_name")

        self.model_name = wxai_model
        self.api_key = wxai_apikey
        self.project_id = wxai_project

    def who_am_i(self):
        super().who_am_i()

    def greet(self):
        super().greet()
        print(f"API KEY: {self.api_key}")

    def retrieve_tokens(self):
        # Retrieve token for REST service
        d = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key,
        }
        token_response = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=d,
        )

        if token_response.status_code != 200:
            print(
                "error: bad token_response from access token service:"
                + token_response.text
            )
            return {
                "headers": {"Content-Type": "application/json; charset=utf-8"},
                "statusCode": token_response.status_code,
                "body": token_response.text,
            }
        token = token_response.json()["access_token"]
        return token
    
    # Assisted by WCA@IBM
    # Latest GenAI contribution: ibm/granite-8b-code-instruct
    """
    Generates an explanation for the provided code using IBM watsonx AI.

    Returns:
        str: The generated explanation.
    """
    def generate_explanation(self, code_data):
        super().generate_explanation(code_data)

        token = self.retrieve_tokens()

        url = (
            "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        )
        explanation_request = f"""You are an expert software developer. In a sentence or two, explain what does the code do.

        {code_data}
        """

        body = {
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 200,
                "repetition_penalty": 1,
            },
            "model_id": self.model_name,
            "project_id": self.project_id,
            "input": explanation_request,
            "moderations": {
                "hap": {
                    "input": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {"remove_entity_value": True},
                    },
                    "output": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {"remove_entity_value": True},
                    },
                },
                "pii": {
                    "input": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {"remove_entity_value": True},
                    },
                    "output": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {"remove_entity_value": True},
                    },
                },
            },
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()
       # print(data['results'][0]['generated_text'])
        return data['results'][0]['generated_text']

    def generate_summary_from_explanations(self,explanations):
        # Expecting explanations array with format ["explanation_1","explanation_2"]
        super().generate_summary_from_explanations()

        token = self.retrieve_tokens()

        url = (
            "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        )
        summary_request = f"""You are an expert software developer. You have already generated explanations of individual functions in a file. Now given the explanations, clearly and succintly summarize the purpose of the file. 

        [INPUT]
        {explanations}

        [SUMMARY]
        """

        body = {
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 200,
                "repetition_penalty": 1,
            },
            "model_id": self.model_name,
            "project_id": self.project_id,
            "input": summary_request,
            "moderations": {
                "hap": {
                    "input": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {"remove_entity_value": True},
                    },
                    "output": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {"remove_entity_value": True},
                    },
                },
                "pii": {
                    "input": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {"remove_entity_value": True},
                    },
                    "output": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {"remove_entity_value": True},
                    },
                },
            },
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()
       # print(data['results'][0]['generated_text'])
        return data['results'][0]['generated_text']
    
    def answer_user_query(self,question,references):	
        return
    
    def handle_general_requst(self):
        return super().handle_general_requst()