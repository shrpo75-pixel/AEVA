"""
AEVA OS - Chat Subsystem
Immersive chat interface with Quantum Orb, token streaming, and responsive UI
"""

import streamlit as st
from typing import Iterator
from datetime import datetime
from core.state import get_state_manager
from ai.provider import ProviderFactory, AIProviderAbstraction
from utils.ui_components import UIComponents, get_color_value


def render_quantum_orb_component():
    """Render the animated AI Quantum Orb as cinematic focal point."""
    state = get_state_manager()
    model_type = state.get_quantum_orb_model_type()

    st.markdown(
        """
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: var(--aeva-space-lg);
            padding: var(--aeva-space-2xl) var(--aeva-space-lg);
            margin-bottom: var(--aeva-space-2xl);
        ">
        """,
        unsafe_allow_html=True,
    )

    # Quantum Orb
    UIComponents.render_quantum_orb(model_type=model_type, size=140)

    st.markdown(
        """
            <div style="
                text-align: center;
                color: var(--aeva-text-secondary);
                font-size: 0.9rem;
                letter-spacing: 1px;
            ">
                AI QUANTUM ORB • READY
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_message(role: str, content: str, model: str = None):
    """
    Render a single chat message in glass container with gradient fade-in.
    
    Args:
        role: "user" or "assistant"
        content: Message content
        model: Model used (for assistant messages)
    """
    if role == "user":
        glow_class = "aeva-glass-panel-titanium"
        alignment = "flex-end"
        bg_gradient = "rgba(69, 162, 158, 0.1)"
        text_color = "var(--aeva-accent-titanium)"
    else:
        glow_class = "aeva-glass-panel-neon"
        alignment = "flex-start"
        bg_gradient = "rgba(118, 185, 0, 0.1)"
        text_color = "var(--aeva-accent-neon)"

    html = f"""
    <div style="
        display: flex;
        justify-content: {alignment};
        margin: var(--aeva-space-lg) 0;
        animation: aeva-animate-slide-up 0.4s var(--aeva-easing-smooth);
    ">
        <div class="{glow_class}" style="
            max-width: 85%;
            padding: var(--aeva-space-lg);
            word-wrap: break-word;
            word-break: break-word;
            animation: aeva-animate-fade-in 0.5s var(--aeva-easing-smooth);
            line-height: var(--aeva-line-height-relaxed);
        ">
            <div style="
                color: var(--aeva-text-primary);
                margin-bottom: {'var(--aeva-space-sm)' if model else '0'};
            ">
                {content}
            </div>
            {f'<div style="color: {text_color}; font-size: 0.75rem; margin-top: var(--aeva-space-sm);">▸ {model}</div>' if model else ''}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_chat_input_system():
    """
    Render immersive chat input system with multi-line support,
    floating send button, and file upload capabilities.
    """
    st.markdown(
        """
        <div style="
            position: sticky;
            bottom: 0;
            background: linear-gradient(to top, rgba(11, 12, 16, 0.95), transparent);
            padding: var(--aeva-space-lg);
            padding-top: var(--aeva-space-2xl);
            margin-top: auto;
        ">
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 0.08], gap="small")

    with col1:
        user_input = st.text_area(
            "Message",
            placeholder="Type your message... (Shift+Enter for new line)",
            height=80,
            label_visibility="collapsed",
            key="chat_input",
        )

    with col2:
        send_button_html = """
        <div style="
            display: flex;
            flex-direction: column;
            gap: var(--aeva-space-sm);
            height: 100%;
            justify-content: flex-end;
        ">
            <button class="aeva-glass-panel-neon aeva-touch-target" style="
                width: 44px;
                height: 44px;
                border: none;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 1.2rem;
                color: var(--aeva-accent-neon);
                box-shadow: 0 0 16px rgba(118, 185, 0, 0.6);
                transition: all var(--aeva-duration-fast) var(--aeva-easing-smooth);
            " 
            onmouseover="this.style.boxShadow='0 0 24px rgba(118, 185, 0, 0.8)'"
            onmouseout="this.style.boxShadow='0 0 16px rgba(118, 185, 0, 0.6)'"
            title="Send message">
                ▶
            </button>
        </div>
        """
        st.markdown(send_button_html, unsafe_allow_html=True)

    # File Upload & Voice Input (Placeholder)
    col1, col2, col3 = st.columns(3, gap="small")

    with col1:
        uploaded_file = st.file_uploader(
            "Upload image or PDF",
            type=["png", "jpg", "jpeg", "pdf"],
            label_visibility="collapsed",
        )

    with col2:
        st.button(
            "🎤 Voice Input",
            key="voice_btn",
            help="Voice input coming soon",
            use_container_width=True,
        )

    with col3:
        st.button(
            "📎 Attach Files",
            key="attach_btn",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    return user_input, uploaded_file


def stream_response(messages: list, provider):
    """Stream AI response token by token with metrics tracking and HUD display."""
    state = get_state_manager()
    
    # Start streaming session metrics
    state.start_streaming_session()
    state.set_streaming_state(True)
    
    # Create placeholder for streaming response
    response_placeholder = st.empty()
    full_response = ""

    try:
        for token in provider.chat_completion_stream(
            messages,
            temperature=0.7,
            max_tokens=2048,
        ):
            if state.get_abort_flag():
                break

            full_response += token
            
            # Update display with streaming content
            with response_placeholder.container():
                render_chat_message("assistant", full_response, state.get_selected_model())
            
            # Display streaming HUD with metrics
            metrics = state.get_streaming_metrics()
            UIComponents.render_streaming_hud(
                tokens_current=metrics['current_tokens'],
                tokens_speed=metrics['streaming_speed'],
                model_name=state.get_selected_model(),
                studio_name="Chat",
            )

        # End streaming session and calculate metrics
        state.end_streaming_session()
        state.set_streaming_state(False)
        
        # Track tokens for this studio
        token_count = state.get_token_count()
        state.add_studio_tokens("chat", token_count)
        
        # Final message storage
        state.add_to_chat_history("assistant", full_response, state.get_selected_model())
        
        # Show completion notification
        speed = state.get_streaming_metrics()['streaming_speed']
        state.add_notification(
            f"✓ Response streamed ({token_count} tokens at {speed:.2f} tok/sec)",
            "success",
        )
        return full_response

    except Exception as e:
        state.end_streaming_session()
        state.set_streaming_state(False)
        state.add_notification(f"Error during streaming: {str(e)}", "error")
        response_placeholder.error(f"Error: {str(e)}")
        return None


def render_chat_workspace():
    """Render the complete Chat workspace."""
    state = get_state_manager()

    # Header
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: var(--aeva-space-2xl) var(--aeva-space-lg);
            border-bottom: 1px solid rgba(118, 185, 0, 0.1);
            margin-bottom: var(--aeva-space-xl);
        ">
            <h1 style="
                color: var(--aeva-accent-neon);
                font-size: 2.5rem;
                letter-spacing: 2px;
                margin-bottom: var(--aeva-space-md);
            ">
                ✦ QUANTUM DIALOG ✦
            </h1>
            <p style="
                color: var(--aeva-text-secondary);
                font-size: 0.95rem;
            ">
                Immersive AI conversation with streaming intelligence
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quantum Orb (Cinematic Focal Point)
    render_quantum_orb_component()

    # Model badge
    current_model = state.get_selected_model()
    st.markdown(
        f"""
        <div class="aeva-glass-panel-neon" style="
            padding: var(--aeva-space-sm) var(--aeva-space-md);
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: var(--aeva-space-xl);
            border-radius: var(--aeva-radius-xl);
            font-size: 0.95rem;
        ">
            <span style="color: var(--aeva-accent-neon);">MODEL</span>
            <strong style="color: var(--aeva-text-primary);">{current_model}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Chat History Display
    st.markdown(
        """
        <div style="
            min-height: 300px;
            margin-bottom: var(--aeva-space-2xl);
            animation: aeva-animate-fade-in 0.6s var(--aeva-easing-smooth);
        ">
        """,
        unsafe_allow_html=True,
    )

    chat_history = state.get_chat_history()
    if chat_history:
        for msg in chat_history:
            render_chat_message(
                msg["role"],
                msg["content"],
                msg.get("model"),
            )
    else:
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: var(--aeva-space-3xl) var(--aeva-space-lg);
                color: var(--aeva-text-secondary);
            ">
                <div style="font-size: 3rem; margin-bottom: var(--aeva-space-lg);">⬡</div>
                <p>Start a conversation with the Quantum Orb above...</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Input System
    user_input, uploaded_file = render_chat_input_system()

    # Handle message sending
    if user_input.strip():
        # Add user message to history
        state.add_to_chat_history("user", user_input)

        # Prepare messages for API
        messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in state.get_chat_history()
        ]

        try:
            # Initialize provider
            provider = ProviderFactory.create("nvidia")

            # Stream response
            stream_response(messages, provider)
            st.rerun()

        except Exception as e:
            state.add_notification(f"Failed to get response: {str(e)}", "error")
            st.error(f"Error: {str(e)}")

    # Sidebar Quick Actions
    with st.sidebar:
        st.markdown("---")
        st.subheader("💬 Chat Controls", divider="gray")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear History", use_container_width=True):
                state.clear_chat_history()
                st.success("History cleared!")
                st.rerun()

        with col2:
            if st.button("💾 Save Chat", use_container_width=True):
                state.save_state_to_disk("chat_backup.json")
                st.success("Chat saved!")

        st.markdown("---")

        # Model Selection
        models = AIProviderAbstraction.get_available_models_for_studio("chat")
        selected_index = 0
        if state.get_selected_model() in models:
            selected_index = models.index(state.get_selected_model())

        selected_model = st.selectbox(
            "Select Model",
            models,
            index=selected_index,
        )

        if selected_model != state.get_selected_model():
            state.set_selected_model(selected_model)
            st.rerun()

        # Temperature Control
        temperature = st.slider(
            "Temperature (Creativity)",
            0.0,
            2.0,
            0.7,
            step=0.1,
            help="Higher = more creative, Lower = more focused",
        )

        # Token Info
        st.write(f"**Tokens Used:** {state.get_token_count()}")

        # Abort Button (when streaming)
        if state.is_streaming():
            if st.button("⏹️ Stop Generation", use_container_width=True):
                state.request_abort_streaming()
                st.warning("Stopping generation...")
