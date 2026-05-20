"""
AEVA OS - AI Provider Abstraction Layer
Modular provider integration with NVIDIA Build API endpoint
Intelligent Dynamic Model Router with studio-specific routing
Secure token streaming, cancellation support, and error recovery
"""

import os
import json
import asyncio
import aiohttp
import requests
from typing import Optional, AsyncIterator, Dict, List, Any, Iterator
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import streamlit as st
from core.state import get_state_manager


class StudioType(Enum):
    """Enum for AEVA OS studio types."""
    CHAT = "chat"
    NOVEL = "novel"
    FORGE = "forge"
    DEV = "dev"


class ModelCategory(Enum):
    """AI Model categories."""
    REASONING = "reasoning"
    CHAT = "chat"
    CODING = "coding"
    VISION = "vision"


@dataclass
class AIProviderConfig:
    """Configuration for AI providers."""

    api_endpoint: str
    api_key: str
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0


# ─────────────────────────────────────────────────────────────────────────
# COMPREHENSIVE MODEL REGISTRY
# ─────────────────────────────────────────────────────────────────────────

MODEL_CATALOG = {
    ModelCategory.REASONING: {
        "models": [
            "qwen/qwen3-next-80b-a3b-thinking",
            "moonshotai/kimi-k2-instruct"
        ],
        "provider_logo": "🧠",
        "description": "Deep reasoning with extended thinking",
        "context_window": 128000,
        "quantum_orb_mode": "pulse_titanium_slow",
        "optimal_studios": ["chat"],
    },
    ModelCategory.CHAT: {
        "models": [
            "nvidia/llama2-70b",
            "meta/llama-3.3-70b-instruct",
            "google/gemma-3-27b-it",
            "mistralai/mistral-nemotron"
        ],
        "provider_logo": "💬",
        "description": "High-quality conversational models",
        "context_window": 32000,
        "quantum_orb_mode": "pulse_neon_fluid",
        "optimal_studios": ["chat", "novel"],
    },
    ModelCategory.CODING: {
        "models": [
            "qwen/qwen3-coder-480b-a3b-instruct",
            "qwen/qwen2.5-coder-32b-instruct"
        ],
        "provider_logo": "⚡",
        "description": "Code-specialized reasoning and generation",
        "context_window": 200000,
        "quantum_orb_mode": "waveform_electric",
        "optimal_studios": ["forge", "dev"],
    },
    ModelCategory.VISION: {
        "models": [
            "nvidia/nemotron-nano-12b-v2-vl",
            "meta/llama-3.2-11b-vision-instruct"
        ],
        "provider_logo": "👁️",
        "description": "Multimodal vision and language understanding",
        "context_window": 4096,
        "quantum_orb_mode": "rotate_ring_vision",
        "optimal_studios": ["chat", "forge"],
    },
}

# Studio-to-Model-Category routing map
STUDIO_MODEL_ROUTES = {
    StudioType.CHAT.value: [ModelCategory.REASONING, ModelCategory.CHAT, ModelCategory.VISION],
    StudioType.NOVEL.value: [ModelCategory.CHAT, ModelCategory.REASONING],
    StudioType.FORGE.value: [ModelCategory.CODING, ModelCategory.VISION],
    StudioType.DEV.value: [ModelCategory.CODING],
}

STUDIO_DISPLAY_NAMES = {
    StudioType.CHAT.value: "Chat",
    StudioType.NOVEL.value: "Novel Studio",
    StudioType.FORGE.value: "Quantum Forge",
    StudioType.DEV.value: "Dev Studio",
}


def _resolve_studio_models(studio: str) -> List[str]:
    """Return ordered model list for a studio based on configured category routes."""
    models: List[str] = []
    categories = STUDIO_MODEL_ROUTES.get(studio, STUDIO_MODEL_ROUTES[StudioType.CHAT.value])
    for category in categories:
        category_config = MODEL_CATALOG.get(category, {})
        for model in category_config.get("models", []):
            if model not in models:
                models.append(model)
    return models


class AIProviderAbstraction:
    """
    Modular AI provider abstraction layer supporting multiple backends.
    Current focus: NVIDIA Build API endpoint integration.
    """

    # Supported providers
    NVIDIA_ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"
    OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"

    def __init__(self, config: AIProviderConfig, provider: str = "nvidia"):
        self.config = config
        self.provider = provider
        self.state = get_state_manager()
        self.abort_flag = False
        self.current_token_count = 0

    @staticmethod
    def from_env(provider: str = "nvidia") -> "AIProviderAbstraction":
        """Create provider from environment variables."""
        api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                f"API key not found. Set NVIDIA_API_KEY or OPENAI_API_KEY environment variable."
            )

        endpoint = (
            AIProviderAbstraction.NVIDIA_ENDPOINT
            if provider == "nvidia"
            else AIProviderAbstraction.OPENAI_ENDPOINT
        )

        config = AIProviderConfig(api_endpoint=endpoint, api_key=api_key)
        return AIProviderAbstraction(config, provider)

    @staticmethod
    def from_session_state(provider: str = "nvidia") -> "AIProviderAbstraction":
        """Create provider from Streamlit session state."""
        state = get_state_manager()
        api_key = state.get_api_key()

        if not api_key:
            raise ValueError(
                "API key not configured. Please configure it in settings."
            )

        endpoint = (
            AIProviderAbstraction.NVIDIA_ENDPOINT
            if provider == "nvidia"
            else AIProviderAbstraction.OPENAI_ENDPOINT
        )

        config = AIProviderConfig(api_endpoint=endpoint, api_key=api_key)
        return AIProviderAbstraction(config, provider)

    @staticmethod
    def get_default_model_for_studio(studio: str) -> str:
        """Return the default NVIDIA model ID for the requested studio."""
        models = _resolve_studio_models(studio)
        if models:
            return models[0]
        return MODEL_CATALOG[ModelCategory.CHAT]["models"][0]

    @staticmethod
    def get_available_models_for_studio(studio: str) -> List[str]:
        """Return the exact NVIDIA model option list for the requested studio."""
        return _resolve_studio_models(studio)

    @staticmethod
    def get_studio_display_name(studio: str) -> str:
        """Return the display name for the requested studio."""
        return STUDIO_DISPLAY_NAMES.get(studio, STUDIO_DISPLAY_NAMES[StudioType.CHAT.value])

    @staticmethod
    def get_all_nvidia_models() -> List[str]:
        """Return the unique set of all NVIDIA models used by AEVA OS."""
        models: List[str] = []
        for category_data in MODEL_CATALOG.values():
            for model in category_data.get("models", []):
                if model not in models:
                    models.append(model)
        return models

    def request_abort(self) -> None:
        """Request to abort ongoing streaming."""
        self.abort_flag = True
        self.state.request_abort_streaming()

    def is_abort_requested(self) -> bool:
        """Check if abort was requested."""
        return self.abort_flag or self.state.get_abort_flag()

    def clear_abort_flag(self) -> None:
        """Clear abort flag."""
        self.abort_flag = False
        self.state.clear_abort_flag()

    def _build_request_headers(self) -> Dict[str, str]:
        """Build request headers for API call."""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        if self.provider == "nvidia":
            headers["User-Agent"] = "AEVA-OS/1.0 (Mobile-First)"

        return headers

    def _build_request_body(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """Build request body for API call."""
        return {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            "top_p": 0.9,
        }

    def _parse_stream_response(self, line: str) -> Optional[str]:
        """Parse streaming response line to extract token."""
        if not line.startswith("data:"):
            return None

        data_str = line[5:].strip()

        if data_str == "[DONE]":
            return None

        try:
            data = json.loads(data_str)
            token = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
            return token
        except json.JSONDecodeError:
            return None

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """
        Non-streaming chat completion.
        Returns complete response as string.
        """
        model = model or self.state.get_selected_model()
        self.clear_abort_flag()

        headers = self._build_request_headers()
        body = self._build_request_body(
            messages, model, temperature, max_tokens, stream=False
        )

        try:
            response = requests.post(
                self.config.api_endpoint,
                headers=headers,
                json=body,
                timeout=self.config.timeout,
            )
            response.raise_for_status()

            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")

        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            self.state.add_notification(error_msg, "error")
            raise

    def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Iterator[str]:
        """
        Streaming chat completion with token-by-token response engine.
        Supports request cancellation via abort_flag.
        Yields individual tokens.
        """
        model = model or self.state.get_selected_model()
        self.clear_abort_flag()
        self.current_token_count = 0
        self.state.set_streaming_state(True)

        headers = self._build_request_headers()
        body = self._build_request_body(
            messages, model, temperature, max_tokens, stream=True
        )

        try:
            response = requests.post(
                self.config.api_endpoint,
                headers=headers,
                json=body,
                timeout=self.config.timeout,
                stream=True,
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if self.is_abort_requested():
                    break

                if not line:
                    continue

                token = self._parse_stream_response(line.decode("utf-8"))
                if token:
                    self.current_token_count += len(token.split())
                    self.state.update_token_count(self.current_token_count)
                    yield token

        except requests.exceptions.RequestException as e:
            error_msg = f"Streaming API request failed: {str(e)}"
            self.state.add_notification(error_msg, "error")
            raise
        finally:
            self.state.set_streaming_state(False)

    async def chat_completion_stream_async(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncIterator[str]:
        """
        Async streaming chat completion for concurrent operations.
        Useful for background processing and parallel requests.
        """
        model = model or self.state.get_selected_model()
        self.clear_abort_flag()
        self.current_token_count = 0
        self.state.set_streaming_state(True)

        headers = self._build_request_headers()
        body = self._build_request_body(
            messages, model, temperature, max_tokens, stream=True
        )

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.api_endpoint,
                    headers=headers,
                    json=body,
                    timeout=aiohttp.ClientTimeout(total=self.config.timeout),
                ) as response:
                    response.raise_for_status()

                    async for line in response.content:
                        if self.is_abort_requested():
                            break

                        if not line:
                            continue

                        token = self._parse_stream_response(line.decode("utf-8"))
                        if token:
                            self.current_token_count += len(token.split())
                            self.state.update_token_count(self.current_token_count)
                            yield token

        except aiohttp.ClientError as e:
            error_msg = f"Async streaming API request failed: {str(e)}"
            self.state.add_notification(error_msg, "error")
            raise
        finally:
            self.state.set_streaming_state(False)

    def validate_api_key(self) -> bool:
        """Validate API key by making a minimal API call."""
        headers = self._build_request_headers()
        body = self._build_request_body(
            [{"role": "user", "content": "ping"}],
            AIProviderAbstraction.get_default_model_for_studio("chat"),
            temperature=0.1,
            max_tokens=10,
        )

        try:
            response = requests.post(
                self.config.api_endpoint,
                headers=headers,
                json=body,
                timeout=5,
            )
            return response.status_code == 200
        except Exception:
            return False

    def get_available_models(self) -> List[str]:
        """Get list of available models for current provider."""
        if self.provider == "nvidia":
            return AIProviderAbstraction.get_all_nvidia_models()
        elif self.provider == "openai":
            return [
                "gpt-4-turbo",
                "gpt-4",
                "gpt-3.5-turbo",
            ]
        return []

    def estimate_tokens(self, text: str) -> int:
        """
        Rough estimation of tokens in text.
        Note: This is an approximation. Exact count requires API call.
        """
        words = len(text.split())
        return max(int(words * 1.3), 1)

    def get_token_count(self) -> int:
        """Get current token count from streaming."""
        return self.current_token_count


class ProviderFactory:
    """Factory for creating and managing AI providers."""

    _instances = {}

    @staticmethod
    def create(provider: str = "nvidia", use_env: bool = False) -> AIProviderAbstraction:
        """Create a new provider instance."""
        try:
            if use_env:
                return AIProviderAbstraction.from_env(provider)
            else:
                return AIProviderAbstraction.from_session_state(provider)
        except ValueError as e:
            st.error(f"Failed to initialize {provider} provider: {str(e)}")
            raise

    @staticmethod
    def get_cached(provider: str = "nvidia") -> Optional[AIProviderAbstraction]:
        """Get cached provider instance if available."""
        return ProviderFactory._instances.get(provider)

    @staticmethod
    def cache_instance(provider: str, instance: AIProviderAbstraction) -> None:
        """Cache a provider instance."""
        ProviderFactory._instances[provider] = instance

    @staticmethod
    def clear_cache() -> None:
        """Clear all cached instances."""
        ProviderFactory._instances.clear()
