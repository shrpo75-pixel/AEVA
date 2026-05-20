"""
AEVA OS - Main Entry Point
Secure configuration loading, boot sequence animation, and workspace orchestration
"""

import streamlit as st
import time
import os
from pathlib import Path
from dotenv import load_dotenv
from core.state import get_state_manager
from utils.ui_components import (
    inject_css,
    UIComponents,
    get_color_value,
)
from ai.provider import ProviderFactory, AIProviderAbstraction

# ─────────────────────────────────────────────────────────────────────────
# LOAD ENVIRONMENT VARIABLES
# ─────────────────────────────────────────────────────────────────────────

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────
# STREAMLIT PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AEVA OS - Premium AI Operating System",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────
# INITIALIZE AEVA STATE & CSS
# ─────────────────────────────────────────────────────────────────────────

state = get_state_manager()
inject_css()

# ─────────────────────────────────────────────────────────────────────────
# BOOT SEQUENCE
# ─────────────────────────────────────────────────────────────────────────


def show_boot_sequence():
    """Display boot sequence animation on first load."""
    if not state.get("boot_sequence_shown", False):
        placeholder = st.empty()

        with placeholder.container():
            UIComponents.render_boot_sequence()
            time.sleep(2.5)

        state.set("boot_sequence_shown", True)
        placeholder.empty()


# ─────────────────────────────────────────────────────────────────────────
# API KEY CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────


def setup_api_configuration():
    """Setup and validate API credentials securely."""
    # Check for environment variable first (production mode)
    env_api_key = os.getenv("NVIDIA_API_KEY")
    
    if env_api_key and not state.get_api_key():
        # Auto-configure from environment
        state.configure_api_key(env_api_key)
        state.add_notification(
            "✓ API key loaded from environment - Premium mode unlocked!",
            "success",
        )
        return True
    
    # Manual configuration fallback (development mode)
    if not state.get_api_key():
        st.warning(
            "🔐 **AEVA Configuration Required**\n\n"
            "Please provide your NVIDIA API key to get started.",
            icon="⚠️",
        )

        with st.form("api_config_form"):
            api_key_input = st.text_input(
                "NVIDIA API Key",
                type="password",
                help="Get your API key from https://integrate.api.nvidia.com",
            )
            model_options = AIProviderAbstraction.get_all_nvidia_models()
            selected_index = 0
            if state.get_selected_model() in model_options:
                selected_index = model_options.index(state.get_selected_model())
            model_select = st.selectbox(
                "Select Model",
                model_options,
                index=selected_index,
                help="Choose your preferred AI model",
            )

            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("✓ Configure", use_container_width=True)
            with col2:
                st.form_submit_button("✗ Cancel", use_container_width=True)

            if submitted and api_key_input:
                state.configure_api_key(api_key_input)
                state.set_selected_model(model_select)

                try:
                    provider = ProviderFactory.create("nvidia")
                    if provider.validate_api_key():
                        state.add_notification(
                            "✓ API key validated successfully!",
                            "success",
                        )
                        st.success("✓ Configuration complete! Restarting...")
                        st.rerun()
                    else:
                        state.add_notification(
                            "✗ API key validation failed. Check your key.",
                            "error",
                        )
                except Exception as e:
                    state.add_notification(
                        f"✗ Configuration error: {str(e)}", "error"
                    )

        return False
    return True


# ─────────────────────────────────────────────────────────────────────────
# MAIN LAYOUT & WORKSPACE ROUTING
# ─────────────────────────────────────────────────────────────────────────


def render_main_layout():
    """Render main AEVA OS layout with workspace routing."""
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(
            """
            <div style="
                padding: var(--aeva-space-lg) 0;
                border-bottom: 1px solid rgba(118, 185, 0, 0.1);
                margin-bottom: var(--aeva-space-xl);
            ">
                <div style="
                    color: var(--aeva-accent-neon);
                    font-size: 1.5rem;
                    font-weight: bold;
                    letter-spacing: 2px;
                ">
                    ⬡ AEVA OS
                </div>
                <div style="
                    color: var(--aeva-text-secondary);
                    font-size: 0.75rem;
                    letter-spacing: 1px;
                    margin-top: 0.5rem;
                ">
                    v1.0 ALPHA • MOBILE-FIRST
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        workspace_select = st.radio(
            "Select Workspace",
            ["💬 Chat", "📖 Novel Studio", "🔬 Quantum Forge", "📊 Dev Studio"],
            help="Switch between different AEVA OS workspaces",
        )

        # Map display names to workspace keys
        workspace_map = {
            "💬 Chat": "chat",
            "📖 Novel Studio": "novel",
            "🔬 Quantum Forge": "forge",
            "📊 Dev Studio": "dev",
        }

        selected_workspace = workspace_map.get(workspace_select, "chat")
        previous_workspace = state.get_current_workspace()
        if selected_workspace != previous_workspace:
            state.switch_workspace(selected_workspace)
            default_model = AIProviderAbstraction.get_default_model_for_studio(selected_workspace)
            state.set_selected_model(default_model)

        # Settings Section
        st.markdown("---")
        st.subheader("⚙️ Settings", divider="gray")

        # Model Override for Current Studio
        with st.expander("🧠 Model Selection", expanded=False):
            current_studio = state.get_current_workspace()
            available_models = AIProviderAbstraction.get_available_models_for_studio(current_studio)
            current_model = state.get_selected_model()
            
            selected_index = 0
            if current_model in available_models:
                selected_index = available_models.index(current_model)
            
            new_model = st.selectbox(
                "Select AI Model",
                available_models,
                index=selected_index,
                help=f"Available models for {current_studio} studio",
            )
            
            if new_model != current_model:
                state.set_selected_model(new_model)
                st.success(f"✓ Model switched to {new_model}")
                st.rerun()

        with st.expander("🔑 API Configuration", expanded=False):
            if st.button("Reset API Key", use_container_width=True):
                state.clear_api_key()
                st.success("API key cleared. Please reconfigure.")
                st.rerun()

            if st.button("Validate API Connection", use_container_width=True):
                try:
                    provider = ProviderFactory.create("nvidia")
                    if provider.validate_api_key():
                        st.success("✓ API connection valid!")
                    else:
                        st.error("✗ API connection failed.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        with st.expander("📊 System Stats & Metrics", expanded=False):
            # Basic stats
            stats = {
                "Current Workspace": state.get_current_workspace().upper(),
                "Active Model": state.get_selected_model().split("/")[-1],
                "Chat Messages": len(state.get_chat_history()),
                "Novel Chapters": len(state.get_novel_chapters()),
                "Dev Tasks": len(state.get_dev_tasks()),
            }
            for stat_name, stat_value in stats.items():
                st.write(f"**{stat_name}:** `{stat_value}`")
            
            st.markdown("---")
            
            # Streaming metrics
            metrics = state.get_streaming_metrics()
            st.write(f"**Current Tokens:** `{metrics['current_tokens']}`")
            st.write(f"**Session Total:** `{metrics['total_session_tokens']}`")
            st.write(f"**Streaming Speed:** `{metrics['streaming_speed']:.2f} tokens/sec`")
            
            st.markdown("---")
            
            # Studio token usage
            studio_tokens = state.get_all_studio_tokens()
            st.write("**Studio Token Usage:**")
            for studio, tokens in studio_tokens.items():
                st.write(f"  • {studio.title()}: `{tokens}` tokens")
            
            memory_state = "✓ Compressed" if state.is_memory_compressed() else "Standard"
            st.write(f"**Memory State:** `{memory_state}`")

        with st.expander("💾 Data Management", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save State", use_container_width=True):
                    state.save_state_to_disk()
                    st.success("State saved!")
            with col2:
                if st.button("Load State", use_container_width=True):
                    if state.load_state_from_disk():
                        st.success("State loaded!")
                    else:
                        st.warning("No saved state found.")

        # Notifications Display
        notifications = state.get_notifications()
        if notifications:
            st.markdown("---")
            st.subheader("🔔 Notifications", divider="gray")
            for notif in notifications:
                icon_map = {
                    "error": "❌",
                    "warning": "⚠️",
                    "success": "✅",
                    "info": "ℹ️",
                }
                icon = icon_map.get(notif["type"], "•")
                st.write(f"{icon} {notif['message']}")
            if st.button("Clear Notifications", use_container_width=True):
                state.clear_notifications()
                st.rerun()

    # Main Content Area - Workspace Routing
    current_workspace = state.get_current_workspace()

    if current_workspace == "chat":
        from modules.chat import render_chat_workspace

        render_chat_workspace()

    elif current_workspace == "novel":
        from modules.novel import render_novel_workspace

        render_novel_workspace()

    elif current_workspace == "forge":
        from modules.forge import render_quantum_forge

        render_quantum_forge()

    elif current_workspace == "dev":
        from modules.dev import render_dev_studio

        render_dev_studio()


# ─────────────────────────────────────────────────────────────────────────
# COMMAND PALETTE
# ─────────────────────────────────────────────────────────────────────────


def render_command_palette():
    """Render floating command palette for quick actions."""
    if state.is_command_palette_open():
        with st.container():
            st.markdown(
                """
                <div class="aeva-glass-panel-neon" style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 90%;
                    max-width: 600px;
                    z-index: 100;
                    padding: var(--aeva-space-2xl);
                    animation: aeva-animate-scale-pop;
                ">
                    <div style="color: var(--aeva-accent-neon); margin-bottom: var(--aeva-space-lg);">
                        ⌘ COMMAND PALETTE
                    </div>
                    <input type="text" placeholder="Search commands, workspaces, actions..." 
                        style="
                            width: 100%;
                            padding: var(--aeva-space-lg);
                            background: rgba(31, 40, 51, 0.8);
                            border: 1px solid rgba(118, 185, 0, 0.3);
                            color: var(--aeva-text-primary);
                            border-radius: var(--aeva-radius-lg);
                            font-family: var(--aeva-font-family);
                        "
                    />
                </div>
                """,
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────────────


def main():
    """Main application entry point."""

    # Show boot sequence on first run
    show_boot_sequence()

    # Setup API if not configured
    if not setup_api_configuration():
        return

    # Render main layout
    render_main_layout()

    # Render command palette if active
    render_command_palette()

    # Keyboard shortcuts (handled via custom JS in production)
    # Ctrl+K or Cmd+K: Open command palette
    # Ctrl+Q or Cmd+Q: Quick workspace switcher


if __name__ == "__main__":
    main()
