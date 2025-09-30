import requests
import json

QUANTIZE_LIST = [
    "q2_K",
    "q3_K_L",
    "q3_K_M",
    "q3_K_S",
    "q4_0",
    "q4_1",
    "q4_K_M",
    "q4_K_S",
    "q5_0",
    "q5_1",
    "q5_K_M",
    "q5_K_S",
    "q6_K",
    "q8_0",
]


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
        data = {"model": model, "stream": False}
        requests.post(self.base_url + "/api/pull", data=json.dumps(data))
        return model

    def push_model(self, model: str) -> str:
        data = {"model": model, "stream": False}
        requests.post(self.base_url + "/api/push", data=json.dumps(data))
        return model

    def delete_model(self, model: str):
        data = {"model": model}
        result = requests.delete(self.base_url + "/api/delete", data=json.dumps(data))
        if result.status_code != 200:
            raise Exception("Failed to delete the model.")
        return model

    def get_process(self) -> list[str]:
        result = requests.get(self.base_url + "/api/ps")
        return [m["name"] for m in result.json()["models"]]

    def generate(self, model: str, prompt: str, keep_alive: None | int = None) -> str:
        data = {"model": model, "prompt": prompt, "stream": False}
        if keep_alive is not None:
            data["keep_alive"] = keep_alive
        result = requests.post(self.base_url + "/api/generate", data=json.dumps(data))
        return result.json()["response"]

    def create_model(self, model_name: str, from_name: str, system_prompt: str, quantize: None | str = None):
        data = {"model": model_name, "from": from_name, "system": system_prompt}
        if quantize is not None:
            if quantize not in QUANTIZE_LIST:
                raise Exception(f"Unsupported quantize type. Supported types are {QUANTIZE_LIST}")
            data["quantize"] = quantize
        result = requests.post(
            self.base_url + "/api/create",
            data=json.dumps(data),
        )
        return result.json()["response"]

    def is_blob_exist(self, digest: str) -> bool:
        result = requests.head(
            self.base_url + "/api/blobs/" + digest,
        )
        return result.status_code == 200

    def show_model(self, model: str) -> dict:
        data = {"model": model}
        result = requests.post(self.base_url + "/api/show", data=json.dumps(data))
        return result.json()

    def copy_model(self, src: str, dest: str) -> None:
        data = {"source": src, "destination": dest}
        requests.post(self.base_url + "/api/copy", data=json.dumps(data))
