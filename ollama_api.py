import requests
import json


class OllamaAPI:
    def __init__(self, url_ollama):
        self.url_ollama = url_ollama
        self.responses = []

    def generate_response(self, question, context):
        """Generate response from Ollama API"""
        data = {
            "model": "llama3.1",  # Replace with your Ollama model name
            "prompt": f"Context: {context}\nQuestion: {question}\nAnswer:"
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url_ollama, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Response received, generating full answer...")
            self.parse_response(response.text)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def parse_response(self, response_text):
        """Parse the responses from Ollama"""
        response_text = response_text.strip()
        json_objects = response_text.splitlines()
        for json_str in json_objects:
            try:
                response_data = json.loads(json_str)
                response = response_data.get("response", "")
                self.responses.append(response)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")

    def get_full_response(self):
        """Return the full concatenated response"""
        return ''.join(self.responses)
