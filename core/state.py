"""
AEVA OS - Global Dynamic State Manager
Streamlit session_state integration with persistent context management
"""

import streamlit as st
import json
from typing import Any, Optional, Dict, List
from datetime import datetime
from pathlib import Path


class AEVAStateManager:
    """
    Global state manager for AEVA OS ecosystem.
    Handles persistent storage, token management, and cross-module communication.
    """

    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self._init_session_state()

    def _init_session_state(self):
        """Initialize Streamlit session state with default values."""
        if "aeva_initialized" not in st.session_state:
            st.session_state.aeva_initialized = True
            st.session_state.current_workspace = "chat"
            st.session_state.api_key = None
            st.session_state.api_key_configured = False
            st.session_state.selected_model = "meta/llama-3.3-70b-instruct"
            st.session_state.streaming_active = False
            st.session_state.abort_streaming = False
            st.session_state.chat_history = []
            st.session_state.novel_chapters = {}
            st.session_state.novel_active_chapter = None
            st.session_state.forge_datasets = []
            st.session_state.dev_tasks = []
            st.session_state.system_notifications = []
            st.session_state.command_palette_open = False
            st.session_state.theme_mode = "dark"
            st.session_state.quantum_orb_model_type = "reasoning"
            st.session_state.token_count = 0
            st.session_state.max_tokens = 2048
            st.session_state.context_memory = []
            st.session_state.memory_compressed = False
            # Streaming metrics
            st.session_state.streaming_start_time = None
            st.session_state.streaming_end_time = None
            st.session_state.total_session_tokens = 0
            st.session_state.streaming_speed_tokens_per_sec = 0.0
            st.session_state.studio_token_usage = {
                "chat": 0,
                "novel": 0,
                "forge": 0,
                "dev": 0,
            }

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a state value."""
        return st.session_state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a state value."""
        st.session_state[key] = value

    def update(self, **kwargs) -> None:
        """Update multiple state values."""
        for key, value in kwargs.items():
            st.session_state[key] = value

    def configure_api_key(self, api_key: str) -> None:
        """
        Securely store API key in session state (proxied storage).
        In production, use secure localStorage and environment variables.
        """
        self.set("api_key", api_key)
        self.set("api_key_configured", True)

    def get_api_key(self) -> Optional[str]:
        """Retrieve the stored API key safely."""
        return self.get("api_key", None)

    def clear_api_key(self) -> None:
        """Clear stored API key from memory."""
        self.set("api_key", None)
        self.set("api_key_configured", False)

    def switch_workspace(self, workspace: str) -> None:
        """Switch to a different workspace (chat, novel, forge, dev)."""
        valid_workspaces = ["chat", "novel", "forge", "dev"]
        if workspace in valid_workspaces:
            self.set("current_workspace", workspace)
        else:
            raise ValueError(f"Invalid workspace: {workspace}")

    def get_current_workspace(self) -> str:
        """Get the currently active workspace."""
        return self.get("current_workspace", "chat")

    def add_to_chat_history(self, role: str, content: str, model: str = None) -> None:
        """Add a message to chat history."""
        message = {
            "role": role,
            "content": content,
            "model": model or self.get("selected_model"),
            "timestamp": datetime.now().isoformat(),
        }
        history = self.get("chat_history", [])
        history.append(message)
        self.set("chat_history", history)

    def get_chat_history(self) -> List[Dict]:
        """Retrieve full chat history."""
        return self.get("chat_history", [])

    def clear_chat_history(self) -> None:
        """Clear entire chat history."""
        self.set("chat_history", [])
        self.set("context_memory", [])
        self.set("memory_compressed", False)

    def set_streaming_state(self, active: bool) -> None:
        """Set streaming state."""
        self.set("streaming_active", active)

    def is_streaming(self) -> bool:
        """Check if streaming is active."""
        return self.get("streaming_active", False)

    def request_abort_streaming(self) -> None:
        """Request to abort ongoing streaming."""
        self.set("abort_streaming", True)

    def get_abort_flag(self) -> bool:
        """Check if abort was requested."""
        return self.get("abort_streaming", False)

    def clear_abort_flag(self) -> None:
        """Clear the abort flag."""
        self.set("abort_streaming", False)

    def set_quantum_orb_model_type(self, model_type: str) -> None:
        """
        Set quantum orb animation based on model type.
        Types: reasoning, lightweight, coding, vision
        """
        self.set("quantum_orb_model_type", model_type)

    def get_quantum_orb_model_type(self) -> str:
        """Get current quantum orb model type."""
        return self.get("quantum_orb_model_type", "reasoning")

    def update_token_count(self, tokens: int) -> None:
        """Update current token count."""
        self.set("token_count", tokens)

    def get_token_count(self) -> int:
        """Get current token count."""
        return self.get("token_count", 0)

    def add_novel_chapter(self, chapter_id: str, title: str, content: str = "") -> None:
        """Add a new chapter to novel project."""
        chapters = self.get("novel_chapters", {})
        chapters[chapter_id] = {
            "title": title,
            "content": content,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        self.set("novel_chapters", chapters)

    def update_novel_chapter(self, chapter_id: str, content: str) -> None:
        """Update chapter content."""
        chapters = self.get("novel_chapters", {})
        if chapter_id in chapters:
            chapters[chapter_id]["content"] = content
            chapters[chapter_id]["updated_at"] = datetime.now().isoformat()
            self.set("novel_chapters", chapters)

    def get_novel_chapters(self) -> Dict:
        """Get all novel chapters."""
        return self.get("novel_chapters", {})

    def set_active_novel_chapter(self, chapter_id: str) -> None:
        """Set the active chapter for editing."""
        self.set("novel_active_chapter", chapter_id)

    def get_active_novel_chapter(self) -> Optional[str]:
        """Get the currently active novel chapter ID."""
        return self.get("novel_active_chapter", None)

    def add_forge_dataset(self, dataset_name: str, data_type: str) -> None:
        """Add a dataset to Quantum Forge."""
        datasets = self.get("forge_datasets", [])
        datasets.append({
            "name": dataset_name,
            "type": data_type,
            "uploaded_at": datetime.now().isoformat(),
            "status": "processing",
        })
        self.set("forge_datasets", datasets)

    def get_forge_datasets(self) -> List[Dict]:
        """Get all Quantum Forge datasets."""
        return self.get("forge_datasets", [])

    def add_dev_task(self, task_id: str, task_name: str, status: str = "pending") -> None:
        """Add a task to Dev Studio."""
        tasks = self.get("dev_tasks", [])
        tasks.append({
            "id": task_id,
            "name": task_name,
            "status": status,
            "created_at": datetime.now().isoformat(),
        })
        self.set("dev_tasks", tasks)

    def update_dev_task_status(self, task_id: str, status: str) -> None:
        """Update a dev task status."""
        tasks = self.get("dev_tasks", [])
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = status
                break
        self.set("dev_tasks", tasks)

    def get_dev_tasks(self) -> List[Dict]:
        """Get all dev tasks."""
        return self.get("dev_tasks", [])

    def add_notification(
        self,
        message: str,
        notification_type: str = "info",
        duration: int = 3000,
    ) -> None:
        """
        Add a system notification.
        Types: info, warning, error, success
        """
        notifications = self.get("system_notifications", [])
        notification = {
            "message": message,
            "type": notification_type,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "id": len(notifications),
        }
        notifications.append(notification)
        self.set("system_notifications", notifications)

    def get_notifications(self) -> List[Dict]:
        """Get all pending notifications."""
        return self.get("system_notifications", [])

    def clear_notifications(self) -> None:
        """Clear all notifications."""
        self.set("system_notifications", [])

    def open_command_palette(self) -> None:
        """Open command palette."""
        self.set("command_palette_open", True)

    def close_command_palette(self) -> None:
        """Close command palette."""
        self.set("command_palette_open", False)

    def is_command_palette_open(self) -> bool:
        """Check if command palette is open."""
        return self.get("command_palette_open", False)

    def set_selected_model(self, model: str) -> None:
        """Set the currently selected AI model."""
        self.set("selected_model", model)
        # Update quantum orb animation based on model characteristics
        if "reasoning" in model.lower():
            self.set_quantum_orb_model_type("reasoning")
        elif "coding" in model.lower() or "code" in model.lower():
            self.set_quantum_orb_model_type("coding")
        elif "vision" in model.lower():
            self.set_quantum_orb_model_type("vision")
        else:
            self.set_quantum_orb_model_type("lightweight")

    def get_selected_model(self) -> str:
        """Get the currently selected model."""
        return self.get("selected_model", "meta/llama-3.3-70b-instruct")

    def add_to_context_memory(self, summary: str) -> None:
        """Add a context summary to memory."""
        memory = self.get("context_memory", [])
        memory.append({
            "summary": summary,
            "timestamp": datetime.now().isoformat(),
        })
        self.set("context_memory", memory)

    def get_context_memory(self) -> List[Dict]:
        """Get context memory."""
        return self.get("context_memory", [])

    def mark_memory_compressed(self) -> None:
        """Mark that context has been compressed."""
        self.set("memory_compressed", True)

    def is_memory_compressed(self) -> bool:
        """Check if context memory has been compressed."""
        return self.get("memory_compressed", False)

    def start_streaming_session(self) -> None:
        """Mark the start of a streaming session."""
        import time
        self.set("streaming_start_time", time.time())
        self.set("streaming_end_time", None)

    def end_streaming_session(self) -> None:
        """Mark the end of a streaming session and calculate metrics."""
        import time
        self.set("streaming_end_time", time.time())
        
        start_time = self.get("streaming_start_time")
        end_time = self.get("streaming_end_time")
        token_count = self.get_token_count()
        
        if start_time and end_time and token_count > 0:
            duration = end_time - start_time
            speed = token_count / duration if duration > 0 else 0
            self.set("streaming_speed_tokens_per_sec", speed)
            
            # Update total session tokens
            total = self.get("total_session_tokens", 0)
            self.set("total_session_tokens", total + token_count)

    def get_streaming_metrics(self) -> Dict[str, Any]:
        """Get comprehensive streaming metrics."""
        return {
            "current_tokens": self.get_token_count(),
            "total_session_tokens": self.get("total_session_tokens", 0),
            "streaming_speed": self.get("streaming_speed_tokens_per_sec", 0.0),
            "is_streaming": self.is_streaming(),
            "start_time": self.get("streaming_start_time"),
            "end_time": self.get("streaming_end_time"),
        }

    def add_studio_tokens(self, studio: str, tokens: int) -> None:
        """Add tokens to a specific studio's usage tracking."""
        studio_usage = self.get("studio_token_usage", {})
        current = studio_usage.get(studio, 0)
        studio_usage[studio] = current + tokens
        self.set("studio_token_usage", studio_usage)

    def get_studio_tokens(self, studio: str) -> int:
        """Get total tokens used in a specific studio."""
        studio_usage = self.get("studio_token_usage", {})
        return studio_usage.get(studio, 0)

    def get_all_studio_tokens(self) -> Dict[str, int]:
        """Get token usage for all studios."""
        return self.get("studio_token_usage", {
            "chat": 0,
            "novel": 0,
            "forge": 0,
            "dev": 0,
        })

    def save_state_to_disk(self, filename: str = "aeva_state.json") -> None:
        """
        Save critical session state to disk for recovery.
        Excludes API keys and sensitive data.
        """
        safe_state = {
            "chat_history": self.get("chat_history"),
            "novel_chapters": self.get("novel_chapters"),
            "context_memory": self.get("context_memory"),
            "dev_tasks": self.get("dev_tasks"),
            "timestamp": datetime.now().isoformat(),
        }
        file_path = self.data_dir / filename
        with open(file_path, "w") as f:
            json.dump(safe_state, f, indent=2)

    def load_state_from_disk(self, filename: str = "aeva_state.json") -> bool:
        """
        Load previously saved state from disk.
        Returns True if successful, False if file not found.
        """
        file_path = self.data_dir / filename
        if not file_path.exists():
            return False

        try:
            with open(file_path, "r") as f:
                saved_state = json.load(f)

            self.set("chat_history", saved_state.get("chat_history", []))
            self.set("novel_chapters", saved_state.get("novel_chapters", {}))
            self.set("context_memory", saved_state.get("context_memory", []))
            self.set("dev_tasks", saved_state.get("dev_tasks", []))
            return True
        except Exception as e:
            print(f"Error loading state from disk: {e}")
            return False

    def reset_to_defaults(self) -> None:
        """Reset all state to default values."""
        self._init_session_state()

    def get_full_state(self) -> Dict[str, Any]:
        """Get entire session state (for debugging/auditing)."""
        return dict(st.session_state)


# Global instance
aeva_state = None


def get_state_manager() -> AEVAStateManager:
    """Get or create the global state manager."""
    global aeva_state
    if aeva_state is None:
        aeva_state = AEVAStateManager()
    return aeva_state
