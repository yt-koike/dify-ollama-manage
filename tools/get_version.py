from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.ollama import OllamaManager


class GetVersion(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ollama = OllamaManager(self.runtime.credentials.get("base_url"))
        yield self.create_text_message(ollama.get_version())
