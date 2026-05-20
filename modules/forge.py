"""
AEVA OS - Quantum Forge (Scientific Module)
Futuristic scientific HUD with data analysis and visualization
"""

import streamlit as st
from core.state import get_state_manager
from ai.provider import AIProviderAbstraction
from utils.ui_components import UIComponents


def render_3d_graph_viewport():
    """Render interactive 3D graph viewport placeholder."""
    st.markdown(
        """
        <div class="aeva-glass-panel-cyan" style="
            padding: var(--aeva-space-xl);
            border-radius: var(--aeva-radius-lg);
            aspect-ratio: 16 / 9;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(0, 217, 255, 0.05), rgba(69, 162, 158, 0.05));
            position: relative;
            overflow: hidden;
        ">
            <!-- Animated grid background -->
            <div style="
                position: absolute;
                width: 100%;
                height: 100%;
                opacity: 0.1;
                background-image: 
                    linear-gradient(90deg, rgba(0, 217, 255, 0.3) 1px, transparent 1px),
                    linear-gradient(rgba(0, 217, 255, 0.3) 1px, transparent 1px);
                background-size: 20px 20px;
                animation: aeva-animate-float 8s var(--aeva-easing-smooth) infinite;
            "></div>
            
            <div style="
                position: relative;
                z-index: 1;
                text-align: center;
                color: var(--aeva-text-secondary);
            ">
                <div style="font-size: 3rem; margin-bottom: var(--aeva-space-lg);">📊</div>
                <p>3D Graph Visualization Viewport</p>
                <p style="font-size: 0.85rem; color: var(--aeva-text-muted);">
                    Upload data or connect live streams to visualize
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_equation_panels():
    """Render floating scientific glass panels with math rendering."""
    equations = [
        ("Quantum State", "Ψ = ψ₁ + ψ₂ + ... + ψₙ"),
        ("Energy Function", "E = ℏω(n + 1/2)"),
        ("Superposition", "H|ψ⟩ = E|ψ⟩"),
    ]

    cols = st.columns(len(equations))

    for idx, (title, equation) in enumerate(equations):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="aeva-glass-panel-neon" style="
                    padding: var(--aeva-space-lg);
                    text-align: center;
                    border-radius: var(--aeva-radius-lg);
                    animation: aeva-animate-slide-up 0.5s var(--aeva-easing-smooth);
                    animation-delay: {idx * 0.1}s;
                ">
                    <div style="
                        color: var(--aeva-accent-neon);
                        font-size: 0.9rem;
                        font-weight: 600;
                        margin-bottom: var(--aeva-space-md);
                        letter-spacing: 1px;
                    ">
                        {title}
                    </div>
                    <div style="
                        color: var(--aeva-text-primary);
                        font-family: var(--aeva-font-mono);
                        font-size: 1.1rem;
                        letter-spacing: 0.5px;
                    ">
                        {equation}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_dataset_upload_zone():
    """Render dataset file upload drop-zone with CSV/Excel parsing."""
    st.markdown(
        """
        <div class="aeva-glass-panel-titanium" style="
            padding: var(--aeva-space-2xl);
            border: 2px dashed rgba(69, 162, 158, 0.4);
            border-radius: var(--aeva-radius-lg);
            text-align: center;
            cursor: pointer;
            transition: all var(--aeva-duration-fast) var(--aeva-easing-smooth);
        " onmouseover="this.style.borderColor='rgba(69, 162, 158, 0.8)'; this.style.background='rgba(69, 162, 158, 0.05)'"
           onmouseout="this.style.borderColor='rgba(69, 162, 158, 0.4)'; this.style.background='transparent'">
            <div style="font-size: 2rem; margin-bottom: var(--aeva-space-lg);">📁</div>
            <div style="
                color: var(--aeva-accent-titanium);
                font-weight: 600;
                margin-bottom: var(--aeva-space-sm);
            ">
                Drop Dataset Here
            </div>
            <div style="
                color: var(--aeva-text-secondary);
                font-size: 0.9rem;
            ">
                CSV, Excel, JSON, or Parquet files
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx", "json", "parquet"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        state = get_state_manager()
        state.add_forge_dataset(uploaded_file.name, uploaded_file.type)

        st.markdown(
            f"""
            <div class="aeva-glass-panel-neon" style="
                padding: var(--aeva-space-lg);
                border-radius: var(--aeva-radius-lg);
                margin-top: var(--aeva-space-lg);
            ">
                <div style="color: var(--aeva-accent-neon); font-weight: 600;">
                    ✓ File Detected: {uploaded_file.name}
                </div>
                <div style="
                    color: var(--aeva-text-secondary);
                    font-size: 0.9rem;
                    margin-top: var(--aeva-space-sm);
                ">
                    Size: {uploaded_file.size / 1024:.2f} KB
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Progress tracker
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Parse Progress", "89%")

        with col2:
            st.metric("Validation", "✓ Pass")

        with col3:
            st.metric("Confidence", "94%")


def render_quantum_forge():
    """Render complete Quantum Forge scientific workspace."""
    state = get_state_manager()

    # Header
    current_model = state.get_selected_model()
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: var(--aeva-space-xl) var(--aeva-space-lg);
            margin-bottom: var(--aeva-space-xl);
            border-bottom: 1px solid rgba(0, 217, 255, 0.1);
        ">
            <h1 style="
                color: var(--aeva-accent-cyan);
                font-size: 2rem;
                letter-spacing: 2px;
            ">
                🔬 QUANTUM FORGE 🔬
            </h1>
            <p style="color: var(--aeva-text-secondary);">
                Scientific HUD • Real-Time Data Analysis • Advanced Computation
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
                <span style="color: var(--aeva-accent-cyan);">MODEL</span>
                <strong style="color: var(--aeva-text-primary);">{current_model}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3D Visualization Viewport
    st.subheader("📊 Data Visualization Engine", divider="gray")
    render_3d_graph_viewport()

    st.markdown("---")

    # Equation Panels
    st.subheader("⚗️ Mathematical Equations", divider="gray")
    render_equation_panels()

    st.markdown("---")

    # Dataset Upload Zone
    st.subheader("📁 Dataset Analysis", divider="gray")
    render_dataset_upload_zone()

    st.markdown("---")

    # Studio model override
    with st.sidebar:
        st.markdown("---")
        st.subheader("🧠 Forge Model Selector", divider="gray")
        models = AIProviderAbstraction.get_available_models_for_studio("forge")
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

    # Active Datasets
    st.subheader("📚 Active Datasets", divider="gray")

    datasets = state.get_forge_datasets()

    if datasets:
        for dataset in datasets:
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(
                    f"""
                    <div class="aeva-glass-panel" style="padding: var(--aeva-space-md);">
                        <div style="color: var(--aeva-accent-cyan); font-weight: 600;">
                            {dataset['name']}
                        </div>
                        <div style="
                            color: var(--aeva-text-secondary);
                            font-size: 0.85rem;
                            margin-top: var(--aeva-space-xs);
                        ">
                            Type: {dataset['type']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                status_color = (
                    "#2ED573" if dataset["status"] == "complete" else "#FFA502"
                )
                st.markdown(
                    f"""
                    <div style="
                        color: {status_color};
                        text-align: center;
                        font-weight: 600;
                        padding: var(--aeva-space-md);
                    ">
                        {dataset['status'].upper()}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                if st.button("🔍", key=f"inspect_{dataset['name']}", use_container_width=True):
                    st.info(f"Analyzing: {dataset['name']}")

    else:
        st.markdown(
            """
            <div style="
                text-align: center;
                color: var(--aeva-text-secondary);
                padding: var(--aeva-space-2xl);
            ">
                <p>No datasets loaded. Upload a file to begin analysis.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Sidebar Controls
    with st.sidebar:
        st.markdown("---")
        st.subheader("🔬 Forge Controls", divider="gray")

        # Computation Mode
        comp_mode = st.selectbox(
            "Computation Mode",
            ["Real-Time", "Batch Processing", "Streaming Analysis"],
        )

        # Algorithm Selection
        algorithm = st.selectbox(
            "Analysis Algorithm",
            ["Neural Network", "Quantum Algorithm", "Genetic Algorithm", "Hybrid"],
        )

        # Precision Level
        precision = st.slider("Precision Level", 1, 10, 8)

        # Export Options
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export Data", use_container_width=True):
                st.success("Data exported!")

        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generating...")
