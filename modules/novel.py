"""
AEVA OS - Novel Studio
3-panel workspace for interactive storytelling with persistent memory
"""

import streamlit as st
from datetime import datetime
from core.state import get_state_manager
from ai.provider import AIProviderAbstraction, ProviderFactory
from utils.ui_components import UIComponents, get_color_value


def render_plot_map_panel():
    """Render left panel: Interactive plot tree visualization and story structure."""
    st.markdown(
        """
        <div class="aeva-glass-panel-titanium" style="
            padding: var(--aeva-space-lg);
            height: 600px;
            overflow-y: auto;
            border: 1px solid rgba(69, 162, 158, 0.3);
            border-radius: var(--aeva-radius-lg);
        ">
            <div style="
                color: var(--aeva-accent-titanium);
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: var(--aeva-space-lg);
                letter-spacing: 1px;
            ">
                📍 PLOT MAP & TIMELINE
            </div>
        """,
        unsafe_allow_html=True,
    )

    state = get_state_manager()
    chapters = state.get_novel_chapters()

    if not chapters:
        st.markdown(
            """
            <div style="
                text-align: center;
                color: var(--aeva-text-secondary);
                padding: var(--aeva-space-2xl) var(--aeva-space-lg);
            ">
                <div style="font-size: 2rem; margin-bottom: var(--aeva-space-md);">📖</div>
                <p>No chapters yet. Create your first chapter to begin.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for chapter_id, chapter in chapters.items():
            is_active = chapter_id == state.get_active_novel_chapter()
            active_style = (
                "border: 2px solid var(--aeva-accent-titanium);"
                if is_active
                else "border: 1px solid rgba(69, 162, 158, 0.2);"
            )

            st.markdown(
                f"""
                <div class="aeva-glass-panel" style="
                    padding: var(--aeva-space-md);
                    margin: var(--aeva-space-sm) 0;
                    cursor: pointer;
                    {active_style}
                    transition: all var(--aeva-duration-fast) var(--aeva-easing-smooth);
                " onclick="document.querySelector('[data-chapter={chapter_id}]').click()">
                    <div style="color: var(--aeva-accent-titanium); font-weight: 600;">
                        {chapter.get('title', 'Untitled')}
                    </div>
                    <div style="
                        color: var(--aeva-text-secondary);
                        font-size: 0.8rem;
                        margin-top: var(--aeva-space-xs);
                    ">
                        {len(chapter.get('content', ''))} characters
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                f"✎ Edit",
                key=f"edit_ch_{chapter_id}",
                use_container_width=True,
            ):
                state.set_active_novel_chapter(chapter_id)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Add new chapter
    st.markdown("---")
    new_chapter_title = st.text_input(
        "New Chapter Title",
        placeholder="Chapter name...",
        label_visibility="collapsed",
    )

    if st.button("+ New Chapter", use_container_width=True):
        if new_chapter_title:
            chapter_id = f"ch_{datetime.now().timestamp()}"
            state.add_novel_chapter(chapter_id, new_chapter_title)
            state.set_active_novel_chapter(chapter_id)
            st.success(f"✓ Chapter created: {new_chapter_title}")
            st.rerun()
        else:
            st.warning("Please enter a chapter title.")


def render_focus_writing_mode():
    """Render center panel: Ultra-clean distraction-free writing editor."""
    state = get_state_manager()
    active_chapter_id = state.get_active_novel_chapter()

    st.markdown(
        """
        <div class="aeva-glass-panel-neon" style="
            padding: var(--aeva-space-lg);
            border: 1px solid rgba(118, 185, 0, 0.2);
            border-radius: var(--aeva-radius-lg);
            min-height: 600px;
        ">
            <div style="
                color: var(--aeva-accent-neon);
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: var(--aeva-space-lg);
                letter-spacing: 1px;
            ">
                ✎ FOCUS WRITING MODE
            </div>
        """,
        unsafe_allow_html=True,
    )

    if not active_chapter_id:
        st.markdown(
            """
            <div style="
                text-align: center;
                color: var(--aeva-text-secondary);
                padding: var(--aeva-space-2xl);
            ">
                <p>Select a chapter from the Plot Map to begin writing.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        chapters = state.get_novel_chapters()
        current_chapter = chapters.get(active_chapter_id, {})

        # Chapter header
        st.markdown(
            f"""
            <div style="
                color: var(--aeva-text-primary);
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: var(--aeva-space-lg);
            ">
                {current_chapter.get('title', 'Untitled Chapter')}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Writing editor
        chapter_content = st.text_area(
            "Chapter Content",
            value=current_chapter.get("content", ""),
            height=400,
            label_visibility="collapsed",
            key=f"editor_{active_chapter_id}",
            placeholder="Start writing your chapter here...",
        )

        # Auto-save
        if chapter_content != current_chapter.get("content", ""):
            state.update_novel_chapter(active_chapter_id, chapter_content)

        # Stats
        char_count = len(chapter_content)
        word_count = len(chapter_content.split())

        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: space-between;
                color: var(--aeva-text-secondary);
                font-size: 0.85rem;
                margin-top: var(--aeva-space-lg);
                padding-top: var(--aeva-space-lg);
                border-top: 1px solid rgba(118, 185, 0, 0.1);
            ">
                <div>📝 {word_count} words</div>
                <div>📏 {char_count} characters</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_prompt_core_control():
    """
    Render right panel: Highlight-to-rewrite tools, tone presets,
    and holographic book cover generation.
    """
    st.markdown(
        """
        <div class="aeva-glass-panel-cyan" style="
            padding: var(--aeva-space-lg);
            border: 1px solid rgba(0, 217, 255, 0.2);
            border-radius: var(--aeva-radius-lg);
            min-height: 600px;
        ">
            <div style="
                color: var(--aeva-accent-cyan);
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: var(--aeva-space-lg);
                letter-spacing: 1px;
            ">
                ✨ PROMPT CORE CONTROL
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Narrative Tone Presets
    st.subheader("🎭 Narrative Tone", divider=False)

    tone_options = {
        "Noir": "Dark, cynical, atmospheric storytelling",
        "Cyberpunk": "Futuristic, high-tech, gritty",
        "Gothic": "Dark, mysterious, romantic horror",
        "Cosmic": "Epic, otherworldly, vast scale",
        "Noir Cyberpunk": "Blend of 1940s noir with 2150s tech",
    }

    selected_tone = st.radio(
        "Select Tone",
        list(tone_options.keys()),
        help="Change the narrative tone of your chapter",
        label_visibility="collapsed",
    )

    st.caption(tone_options[selected_tone])

    # Text Transformation Controls
    st.markdown("---")
    st.subheader("🔄 Text Transformations", divider=False)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✏️ Rewrite", use_container_width=True):
            st.info("Highlight text and click 'Rewrite' to transform it.")

    with col2:
        if st.button("🎨 Enhance", use_container_width=True):
            st.info("Enhance writing with more vivid descriptions.")

    # Book Cover Generator
    st.markdown("---")
    st.subheader("📚 Holographic Book Cover", divider=False)

    st.markdown(
        """
        <div class="aeva-glass-panel-neon" style="
            padding: var(--aeva-space-xl);
            text-align: center;
            border-radius: var(--aeva-radius-lg);
            background: linear-gradient(135deg, rgba(118, 185, 0, 0.1), rgba(69, 162, 158, 0.1));
            min-height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        ">
            <div style="font-size: 4rem; margin-bottom: var(--aeva-space-lg);">📖</div>
            <div style="color: var(--aeva-text-secondary); margin-bottom: var(--aeva-space-lg);">
                AI-Generated Cover Preview
            </div>
            <button class="aeva-glass-panel-neon aeva-touch-target" style="
                padding: var(--aeva-space-lg) var(--aeva-space-xl);
                border: none;
                cursor: pointer;
                color: var(--aeva-accent-neon);
                font-weight: 600;
                border-radius: var(--aeva-radius-lg);
            ">
                🎨 Generate Cover
            </button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def render_novel_workspace():
    """Main Novel Studio workspace with 3-panel layout."""
    state = get_state_manager()

    # Header
    current_model = state.get_selected_model()
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: var(--aeva-space-xl) var(--aeva-space-lg);
            margin-bottom: var(--aeva-space-xl);
            border-bottom: 1px solid rgba(69, 162, 158, 0.1);
        ">
            <h1 style="
                color: var(--aeva-accent-titanium);
                font-size: 2rem;
                letter-spacing: 2px;
            ">
                📖 AEVA NOVEL STUDIO 📖
            </h1>
            <p style="color: var(--aeva-text-secondary); margin-top: var(--aeva-space-md);">
                Immersive creative workspace for storytelling
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
                <span style="color: var(--aeva-accent-titanium);">MODEL</span>
                <strong style="color: var(--aeva-text-primary);">{current_model}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Check device type and render layout accordingly
    is_mobile = st.session_state.get("device_width", 1200) < 800

    if is_mobile:
        # Mobile: Swipeable tabs
        tab1, tab2, tab3 = st.tabs(["📍 Plot Map", "✎ Writing", "✨ Control"])

        with tab1:
            render_plot_map_panel()

        with tab2:
            render_focus_writing_mode()

        with tab3:
            render_prompt_core_control()

    else:
        # Desktop: 3-panel split layout
        col1, col2, col3 = st.columns([1, 1.5, 1], gap="medium")

        with col1:
            render_plot_map_panel()

        with col2:
            render_focus_writing_mode()

        with col3:
            render_prompt_core_control()

    # Studio model override in sidebar
    with st.sidebar:
        st.markdown("---")
        st.subheader("🧠 Novel Model Selector", divider="gray")
        models = AIProviderAbstraction.get_available_models_for_studio("novel")
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

    # Auto-save indicator
    st.markdown(
        """
        <div style="
            position: fixed;
            bottom: var(--aeva-space-safe-bottom);
            right: var(--aeva-space-safe-right);
            font-size: 0.8rem;
            color: var(--aeva-text-secondary);
            padding: var(--aeva-space-md);
        ">
            ✓ Auto-saving...
        </div>
        """,
        unsafe_allow_html=True,
    )
