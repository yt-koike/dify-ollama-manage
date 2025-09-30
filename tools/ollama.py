import requests


class OllamaManager:
    # Reference: https://docs.ollama.com/api
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_models(self) -> list[str]:
        result = requests.get(self.base_url + "/api/tags")
        return [model["model"] for model in result.json()["models"]]

    def get_version(self) -> str:
        result = requests.get(self.base_url + "/api/version")
        return result.json()["version"]

    def pull_model(self, model: str) -> str:
        requests.post(self.base_url + "/api/pull", data='{"model": "' + model + '", "stream": false}')
        return model

    def delete_model(self, model: str):
        requests.delete(self.base_url + "/api/delete", data='{"model": "' + model + '"}')
        return model

    def get_process(self) -> list[str]:
        result = requests.get(self.base_url + "/api/ps")
        return [m["name"] for m in result.json()["models"]]

    def generate(self, model: str, prompt: str) -> str:
        result = requests.get(
            self.base_url + "/api/generate",
            data='{"model": "' + model + '", "prompt": "' + prompt + '", "stream": false}',
        )
        return result.json()["response"]
