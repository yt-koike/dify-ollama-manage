from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.ollama import OllamaManager


class Generate(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ollama = OllamaManager(self.runtime.credentials.get("base_url"))
        model = tool_parameters.get("model")
        prompt = tool_parameters.get("prompt")
        keep_alive = tool_parameters.get("keep_alive")
        response = ollama.generate(model, prompt, keep_alive)
        yield self.create_text_message(response)
