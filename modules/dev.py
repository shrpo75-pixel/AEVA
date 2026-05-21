"""
AEVA OS - Dev Studio (Dashboard Module)
Real-time system monitoring, git diff viewer, and deployment controls
"""

import streamlit as st
from datetime import datetime, timedelta
import random
from core.state import get_state_manager
from ai.provider import AIProviderAbstraction, ProviderFactory


def render_model_badge():
    """Render the selected model badge for Dev Studio."""
    state = get_state_manager()
    current_model = state.get_selected_model()
    st.markdown(
        f"""
        <div class="aeva-glass-panel-neon" style="
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: var(--aeva-space-lg);
            padding: var(--aeva-space-sm) var(--aeva-space-md);
            border-radius: var(--aeva-radius-xl);
            font-size: 0.9rem;
        ">
            <span style="color: var(--aeva-accent-cyan);">MODEL</span>
            <strong style="color: var(--aeva-text-primary);">{current_model}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics_cards():
    """Render compact metrics cards in glass containers."""
    metrics = [
        ("CPU Usage", "68%", "var(--aeva-accent-neon)"),
        ("Memory", "4.2 GB / 16 GB", "var(--aeva-accent-titanium)"),
        ("Network I/O", "125 Mbps", "var(--aeva-accent-cyan)"),
        ("API Health", "✓ 99.8%", "var(--aeva-accent-neon)"),
    ]

    cols = st.columns(len(metrics))

    for idx, (title, value, color) in enumerate(metrics):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="aeva-glass-panel-neon" style="
                    padding: var(--aeva-space-lg);
                    border-radius: var(--aeva-radius-lg);
                    text-align: center;
                    animation: aeva-animate-slide-up 0.4s var(--aeva-easing-smooth);
                    animation-delay: {idx * 0.1}s;
                ">
                    <div style="
                        color: var(--aeva-text-secondary);
                        font-size: 0.85rem;
                        letter-spacing: 1px;
                        margin-bottom: var(--aeva-space-sm);
                    ">
                        {title}
                    </div>
                    <div style="
                        color: {color};
                        font-size: 1.4rem;
                        font-weight: bold;
                    ">
                        {value}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def escape_html(text: str) -> str:
    """Escape HTML tags in code snippets so they render as text rather than markup."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_git_diff_viewer():
    """Render git diff-style code viewer in glassmorphism blocks."""
    st.markdown(
        """
        <div style="
            color: var(--aeva-accent-cyan);
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: var(--aeva-space-lg);
            letter-spacing: 1px;
        ">
            📝 RECENT CHANGES
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mock git diff
    diff_content = """
    --- app.py (old)
    +++ app.py (new)
    @@ -45,7 +45,11 @@
     def render_main_layout():
         \"\"\"Render main AEVA OS layout.\"\"\"
    -    st.write("Loading...")
    +    st.markdown(\"<div>Improved Layout</div>\")
    +    
    +    # Better state management
    +    state = get_state_manager()
    +    render_workspace_selector()
    
     def handle_streaming():
         \"\"\"Stream AI responses.\"\"\"
    """

    lines = diff_content.strip().split("\n")

    st.markdown(
        """
        <div class="aeva-glass-panel-titanium" style="
            padding: var(--aeva-space-lg);
            border-radius: var(--aeva-radius-lg);
            font-family: var(--aeva-font-mono);
            font-size: 0.85rem;
            max-height: 400px;
            overflow-y: auto;
            line-height: var(--aeva-line-height-tight);
        ">
        """,
        unsafe_allow_html=True,
    )

    for line in lines:
        if line.startswith("+") and not line.startswith("+++"):
            color = "var(--aeva-accent-neon)"
            bg = "rgba(46, 213, 115, 0.1)"
        elif line.startswith("-") and not line.startswith("---"):
            color = "var(--aeva-danger)"
            bg = "rgba(255, 71, 87, 0.1)"
        elif line.startswith("@@"):
            color = "var(--aeva-text-secondary)"
            bg = "transparent"
        else:
            color = "var(--aeva-text-primary)"
            bg = "transparent"

        safe_line = escape_html(line)

        st.markdown(
            f"""
            <div style="
                color: {color};
                background: {bg};
                padding: 4px 8px;
                border-radius: 2px;
                white-space: pre-wrap;
                word-break: break-word;
            ">
                {safe_line}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_task_timeline():
    """Render AI task orchestration timeline tracker."""
    state = get_state_manager()

    st.markdown(
        """
        <div style="
            color: var(--aeva-accent-titanium);
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: var(--aeva-space-lg);
            letter-spacing: 1px;
        ">
            ⏱️ ORCHESTRATION TIMELINE
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sample tasks
    sample_tasks = [
        {
            "id": "task_001",
            "name": "Model Inference",
            "status": "completed",
            "progress": 100,
            "duration": "2.3s",
        },
        {
            "id": "task_002",
            "name": "Data Processing",
            "status": "in_progress",
            "progress": 65,
            "duration": "~4.1s",
        },
        {
            "id": "task_003",
            "name": "Cache Synchronization",
            "status": "pending",
            "progress": 0,
            "duration": "-",
        },
        {
            "id": "task_004",
            "name": "Deployment Staging",
            "status": "pending",
            "progress": 0,
            "duration": "-",
        },
    ]

    for task in sample_tasks:
        status_colors = {
            "completed": "#2ED573",
            "in_progress": "#FFA502",
            "pending": "#546E7A",
        }

        status_color = status_colors.get(task["status"], "#546E7A")

        st.markdown(
            f"""
            <div class="aeva-glass-panel" style="
                padding: var(--aeva-space-lg);
                margin-bottom: var(--aeva-space-md);
                border-left: 3px solid {status_color};
                border-radius: var(--aeva-radius-lg);
            ">
                <div style="display: flex; justify-content: space-between; margin-bottom: var(--aeva-space-sm);">
                    <div style="color: var(--aeva-text-primary); font-weight: 600;">
                        {task['name']}
                    </div>
                    <div style="color: {status_color}; font-weight: 600; font-size: 0.9rem;">
                        {task['status'].upper()}
                    </div>
                </div>
                
                <!-- Progress bar -->
                <div style="
                    width: 100%;
                    height: 4px;
                    background: rgba(118, 185, 0, 0.1);
                    border-radius: 2px;
                    overflow: hidden;
                    margin-bottom: var(--aeva-space-sm);
                ">
                    <div style="
                        width: {task['progress']}%;
                        height: 100%;
                        background: linear-gradient(90deg, var(--aeva-accent-neon), var(--aeva-accent-cyan));
                        transition: width 0.3s var(--aeva-easing-smooth);
                    "></div>
                </div>
                
                <div style="
                    color: var(--aeva-text-secondary);
                    font-size: 0.85rem;
                    display: flex;
                    justify-content: space-between;
                ">
                    <span>{task['progress']}% Complete</span>
                    <span>⏱️ {task['duration']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Store or update tasks in state
    if not state.get_dev_tasks():
        for task in sample_tasks:
            state.add_dev_task(task["id"], task["name"], task["status"])


def render_deployment_controls():
    """Render floating deployment action controls with CTA button."""
    st.markdown(
        """
        <div style="margin-top: var(--aeva-space-2xl); padding-top: var(--aeva-space-2xl); border-top: 1px solid rgba(118, 185, 0, 0.1);">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            color: var(--aeva-accent-neon);
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: var(--aeva-space-lg);
            letter-spacing: 1px;
        ">
            🚀 DEPLOYMENT CONTROL
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Deployment Status
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="aeva-glass-panel-cyan" style="
                padding: var(--aeva-space-lg);
                text-align: center;
                border-radius: var(--aeva-radius-lg);
            ">
                <div style="color: var(--aeva-text-secondary); font-size: 0.9rem;">
                    Build Status
                </div>
                <div style="
                    color: var(--aeva-accent-cyan);
                    font-weight: bold;
                    font-size: 1.2rem;
                    margin-top: var(--aeva-space-sm);
                ">
                    ✓ PASS
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="aeva-glass-panel-titanium" style="
                padding: var(--aeva-space-lg);
                text-align: center;
                border-radius: var(--aeva-radius-lg);
            ">
                <div style="color: var(--aeva-text-secondary); font-size: 0.9rem;">
                    Tests Passed
                </div>
                <div style="
                    color: var(--aeva-accent-titanium);
                    font-weight: bold;
                    font-size: 1.2rem;
                    margin-top: var(--aeva-space-sm);
                ">
                    27/27
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="aeva-glass-panel-neon" style="
                padding: var(--aeva-space-lg);
                text-align: center;
                border-radius: var(--aeva-radius-lg);
            ">
                <div style="color: var(--aeva-text-secondary); font-size: 0.9rem;">
                    Coverage
                </div>
                <div style="
                    color: var(--aeva-accent-neon);
                    font-weight: bold;
                    font-size: 1.2rem;
                    margin-top: var(--aeva-space-sm);
                ">
                    94%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Main Deployment CTA Button
    st.markdown(
        """
        <div style="
            display: flex;
            gap: var(--aeva-space-lg);
            margin-top: var(--aeva-space-xl);
        ">
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button(
            "✓ APPROVE & DEPLOY TO STAGING",
            key="deploy_btn",
            use_container_width=True,
        ):
            state = get_state_manager()
            state.add_notification(
                "Deployment initiated. Staging environment updating...",
                "info",
            )
            st.success(
                "✓ Deployment pipeline started!\n\nMonitoring staging environment..."
            )

    with col2:
        if st.button(
            "Preview",
            key="preview_btn",
            use_container_width=True,
        ):
            st.info("Preview environment: staging-001.aeva.dev")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_dev_studio():
    """Render complete Dev Studio dashboard."""
    state = get_state_manager()

    # Header
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: var(--aeva-space-xl) var(--aeva-space-lg);
            margin-bottom: var(--aeva-space-xl);
            border-bottom: 1px solid rgba(118, 185, 0, 0.1);
        ">
            <h1 style="
                color: var(--aeva-accent-neon);
                font-size: 2rem;
                letter-spacing: 2px;
            ">
                📊 DEV STUDIO 📊
            </h1>
            <p style="color: var(--aeva-text-secondary);">
                System Monitoring • Deployment Control • Real-Time Analytics
            </p>
            <div class="aeva-glass-panel-neon" style="
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                margin-top: var(--aeva-space-md);
                padding: var(--aeva-space-sm) var(--aeva-space-md);
                border-radius: var(--aeva-radius-xl);
                font-size: 0.9rem;
            ">
                <span style="color: var(--aeva-accent-neon);">MODEL</span>
                <strong style="color: var(--aeva-text-primary);">{state.get_selected_model()}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # System Metrics
    st.subheader("📈 System Metrics", divider="gray")
    render_metrics_cards()

    st.markdown("---")

    # Two-column layout
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.subheader("📝 Code Changes", divider="gray")
        render_git_diff_viewer()

    with col2:
        st.subheader("⏱️ Task Timeline", divider="gray")
        render_task_timeline()

    st.markdown("---")

    # Deployment
    render_deployment_controls()

    # Sidebar
    with st.sidebar:
        st.markdown("---")
        st.subheader("📊 Studio Controls", divider="gray")

        # Monitoring Mode
        monitor_mode = st.selectbox(
            "Monitoring Mode",
            ["Real-Time", "Historical", "Predictive"],
        )

        # Environment Select
        environment = st.selectbox(
            "Environment",
            ["Development", "Staging", "Production"],
        )

        # Log Level
        log_level = st.select_slider(
            "Log Level",
            options=["DEBUG", "INFO", "WARNING", "ERROR"],
            value="INFO",
        )

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export Logs", use_container_width=True):
                st.success("Logs exported!")

        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()

        # Model Selector
        st.markdown("---")
        st.subheader("🧠 Dev Model Selector", divider="gray")
        models = AIProviderAbstraction.get_available_models_for_studio("dev")
        selected_index = 0
        if state.get_selected_model() in models:
            selected_index = models.index(state.get_selected_model())

        selected_model = st.selectbox(
            "Model Override",
            models,
            index=selected_index,
        )
        if selected_model != state.get_selected_model():
            state.set_selected_model(selected_model)
            st.experimental_rerun()

        # Deployment History
        st.markdown("---")
        st.subheader("📜 Deployment History", divider="gray")

        history = [
            ("v1.2.4", "2 hours ago", "✓ Success"),
            ("v1.2.3", "1 day ago", "✓ Success"),
            ("v1.2.2", "3 days ago", "✗ Rollback"),
        ]

        for version, time, status in history:
            status_color = "color: var(--aeva-accent-neon);" if "Success" in status else "color: var(--aeva-danger);"
            st.markdown(
                f"""
                <div style="
                    padding: var(--aeva-space-md);
                    border-left: 3px solid;
                    {status_color}
                    margin-bottom: var(--aeva-space-sm);
                ">
                    <div style="font-weight: 600;">{version}</div>
                    <div style="font-size: 0.85rem; color: var(--aeva-text-secondary);">
                        {time} • {status}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
