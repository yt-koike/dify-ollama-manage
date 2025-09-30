from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.ollama import OllamaManager


class PullModel(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ollama = OllamaManager(self.runtime.credentials.get("base_url"))
        model = tool_parameters.get("model")
        ollama.pull_model(model)
        yield self.create_text_message("Pulled " + model)
