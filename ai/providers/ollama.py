"""Local Ollama backend, used when no cloud key is configured."""

import json
import urllib.error
import urllib.request

from core.config import CONFIG

from .base_provider import BaseProvider, ProviderError, Reply, ToolCall

TIMEOUT_SECONDS = 60


class OllamaProvider(BaseProvider):

    name = "ollama"

    def __init__(self, host=None, model=None):
        self.host = (host or CONFIG.ollama_host).rstrip("/")
        self.model = model or CONFIG.ollama_model

    # =====================================================

    def is_available(self):
        try:
            with urllib.request.urlopen(f"{self.host}/api/tags", timeout=2):
                return True
        except (urllib.error.URLError, OSError):
            return False

    # =====================================================

    def complete(self, prompt, system=None, history=(), tools=()):

        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        for role, text in history:
            messages.append({"role": role, "content": text})

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        if tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
                for tool in tools
            ]

        return self._parse(self._post("/api/chat", payload))

    # =====================================================

    def _post(self, path, payload):

        request = urllib.request.Request(
            f"{self.host}{path}",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                return json.loads(response.read())
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as error:
            raise ProviderError(f"Ollama request failed: {error}") from error

    # =====================================================

    def _parse(self, response):

        message = response.get("message", {})

        calls = []

        for call in message.get("tool_calls", []):

            function = call.get("function", {})
            arguments = function.get("arguments", {})

            # Some models return the argument object as a JSON string.
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}

            calls.append(
                ToolCall(
                    name=function.get("name", ""),
                    arguments=arguments,
                )
            )

        return Reply(
            text=message.get("content", ""),
            tool_calls=tuple(calls),
        )