"""
AEVA OS - UI Components Library
Reusable components for glassmorphism design system
"""

import streamlit as st
from typing import Optional, Callable, List, Dict, Any
import base64


class UIComponents:
    """Collection of AEVA OS UI components."""

    @staticmethod
    def render_glass_panel(
        content: Callable,
        title: Optional[str] = None,
        glow_type: str = "neon",
        padding: str = "lg",
    ) -> None:
        """
        Render a glassmorphism panel with optional glow effect.

        Args:
            content: Callable that renders the panel content
            title: Optional panel title
            glow_type: "neon" or "titanium"
            padding: "sm", "md", "lg", "xl"
        """
        glow_class = f"aeva-glow-{glow_type}-md"
        padding_map = {"sm": "var(--aeva-space-md)", "md": "var(--aeva-space-lg)",
                       "lg": "var(--aeva-space-xl)", "xl": "var(--aeva-space-2xl)"}
        padding_val = padding_map.get(padding, padding_map["lg"])

        css = f"""
        <div class="aeva-glass-panel-{glow_type}" style="
            padding: {padding_val};
            margin: var(--aeva-space-lg) 0;
            animation: aeva-animate-fade-in;
        ">
            {f'<h3 style="color: var(--aeva-accent-{glow_type}); margin-bottom: var(--aeva-space-md);">{title}</h3>' if title else ''}
        </div>
        """
        st.markdown(css, unsafe_allow_html=True)
        content()

    @staticmethod
    def render_quantum_orb(
        model_type: str = "reasoning",
        size: int = 120,
        container_width: str = "100%",
    ) -> None:
        """
        Render animated AI Quantum Orb with reactive pulse based on model type.

        Args:
            model_type: "reasoning", "lightweight", "coding", "vision"
            size: Orb diameter in pixels
            container_width: Container width
        """
        animation_map = {
            "reasoning": "aeva-animate-pulse-titanium-slow",
            "lightweight": "aeva-animate-pulse-neon-fast",
            "coding": "aeva-animate-waveform",
            "vision": "aeva-animate-rotate-ring",
        }

        color_map = {
            "reasoning": "#45A29E",
            "lightweight": "#76B900",
            "coding": "#00D9FF",
            "vision": "#9D4EDD",
        }

        animation = animation_map.get(model_type, animation_map["reasoning"])
        color = color_map.get(model_type, color_map["reasoning"])

        html = f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            width: {container_width};
            margin: var(--aeva-space-2xl) 0;
        ">
            <div style="
                position: relative;
                width: {size}px;
                height: {size}px;
            ">
                <!-- Outer glow layer -->
                <div style="
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    border-radius: 50%;
                    background: radial-gradient(circle at 30% 30%, rgba({int(int(color[1:3], 16)*0.7)}, {int(int(color[3:5], 16)*0.7)}, {int(int(color[5:7], 16)*0.7)}, 0.3), transparent);
                    box-shadow: 0 0 {size}px rgba({int(int(color[1:3], 16))}, {int(int(color[3:5], 16))}, {int(int(color[5:7], 16))}, 0.4);
                    animation: {animation} infinite;
                "></div>
                
                <!-- Core orb -->
                <div style="
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    border-radius: 50%;
                    background: radial-gradient(circle at 35% 35%, {color}, rgba({int(int(color[1:3], 16))}, {int(int(color[3:5], 16))}, {int(int(color[5:7], 16))}, 0.5));
                    box-shadow: inset -2px -2px 4px rgba(0, 0, 0, 0.5), inset 2px 2px 4px rgba(255, 255, 255, 0.1);
                    filter: drop-shadow(0 0 {size // 2}px {color});
                "></div>
                
                <!-- Shine overlay -->
                <div style="
                    position: absolute;
                    width: 40%;
                    height: 40%;
                    top: 15%;
                    left: 15%;
                    border-radius: 50%;
                    background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.6), transparent);
                    opacity: 0.7;
                "></div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    @staticmethod
    def render_boot_sequence() -> None:
        """Render animated boot sequence loading screen."""
        html = """
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            width: 100vw;
            background: linear-gradient(135deg, #0B0C10 0%, #16213E 100%);
            gap: 2rem;
            padding: var(--aeva-space-safe-top) var(--aeva-space-safe-left);
        ">
            <!-- AEVA Logo / Title -->
            <div class="aeva-animate-fade-in" style="
                font-size: 3rem;
                font-weight: bold;
                letter-spacing: 4px;
                color: var(--aeva-accent-neon);
                text-shadow: 0 0 20px var(--aeva-accent-neon);
                margin-bottom: 1rem;
            ">
                AEVA OS
            </div>
            
            <!-- Boot scan line -->
            <div class="aeva-boot-scan" style="
                width: 80%;
                max-width: 400px;
                height: 3px;
                background: linear-gradient(90deg, transparent, var(--aeva-accent-neon), transparent);
                box-shadow: 0 0 10px var(--aeva-accent-neon);
                margin: 1rem 0;
            "></div>
            
            <!-- Loading dots -->
            <div style="
                display: flex;
                gap: 0.5rem;
                margin-top: 2rem;
            ">
                <div class="aeva-animate-pulse-neon-fast" style="
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    background: var(--aeva-accent-neon);
                    box-shadow: 0 0 10px var(--aeva-accent-neon);
                    animation-delay: 0s;
                "></div>
                <div class="aeva-animate-pulse-neon-fast" style="
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    background: var(--aeva-accent-neon);
                    box-shadow: 0 0 10px var(--aeva-accent-neon);
                    animation-delay: 0.2s;
                "></div>
                <div class="aeva-animate-pulse-neon-fast" style="
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    background: var(--aeva-accent-neon);
                    box-shadow: 0 0 10px var(--aeva-accent-neon);
                    animation-delay: 0.4s;
                "></div>
            </div>
            
            <!-- Boot status text -->
            <div class="aeva-boot-flicker" style="
                color: var(--aeva-text-secondary);
                font-size: 0.9rem;
                letter-spacing: 2px;
                margin-top: 2rem;
            ">
                INITIALIZING CORE SYSTEMS...
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    @staticmethod
    def render_animated_sidebar() -> None:
        """Render animated glass sidebar for layout controls."""
        html = """
        <div style="
            position: fixed;
            left: 0;
            top: 0;
            width: 256px;
            height: 100vh;
            background: rgba(11, 12, 16, 0.95);
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(118, 185, 0, 0.1);
            padding: var(--aeva-space-safe-top) var(--aeva-space-lg);
            z-index: 100;
            overflow-y: auto;
            animation: aeva-animate-slide-up 0.5s var(--aeva-easing-smooth);
        ">
            <!-- Sidebar Header -->
            <div style="
                padding-bottom: var(--aeva-space-xl);
                border-bottom: 1px solid rgba(69, 162, 158, 0.1);
                margin-bottom: var(--aeva-space-xl);
            ">
                <div style="
                    color: var(--aeva-accent-neon);
                    font-size: 1.2rem;
                    font-weight: bold;
                    letter-spacing: 2px;
                ">
                    ⬡ AEVA
                </div>
                <div style="
                    color: var(--aeva-text-secondary);
                    font-size: 0.75rem;
                    letter-spacing: 1px;
                    margin-top: 0.25rem;
                ">
                    CONTROL CENTER
                </div>
            </div>
            
            <!-- Navigation Items -->
            <div style="display: flex; flex-direction: column; gap: var(--aeva-space-md);">
                <div class="aeva-glass-panel" style="
                    padding: var(--aeva-space-md);
                    cursor: pointer;
                    transition: all var(--aeva-duration-fast) var(--aeva-easing-smooth);
                ">
                    <div style="color: var(--aeva-accent-neon); font-weight: 500;">💬 Chat</div>
                </div>
                <div class="aeva-glass-panel" style="
                    padding: var(--aeva-space-md);
                    cursor: pointer;
                    transition: all var(--aeva-duration-fast) var(--aeva-easing-smooth);
                ">
                    <div style="color: var(--aeva-accent-titanium); font-weight: 500;">📖 Novel Studio</div>
                </div>
                <div class="aeva-glass-panel" style="
                    padding: var(--aeva-space-md);
                    cursor: pointer;
                    transition: all var(--aeva-duration-fast) var(--aeva-easing-smooth);
                ">
                    <div style="color: var(--aeva-accent-cyan); font-weight: 500;">🔬 Quantum Forge</div>
                </div>
                <div class="aeva-glass-panel" style="
                    padding: var(--aeva-space-md);
                    cursor: pointer;
                    transition: all var(--aeva-duration-fast) var(--aeva-easing-smooth);
                ">
                    <div style="color: var(--aeva-accent-purple); font-weight: 500;">📊 Dev Studio</div>
                </div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    @staticmethod
    def render_toast_notification(
        message: str,
        notification_type: str = "info",
        duration: int = 3000,
    ) -> None:
        """
        Render floating glass toast notification.

        Args:
            message: Notification message
            notification_type: "info", "success", "warning", "error"
            duration: Display duration in milliseconds
        """
        color_map = {
            "info": "#00D9FF",
            "success": "#2ED573",
            "warning": "#FFA502",
            "error": "#FF4757",
        }

        color = color_map.get(notification_type, color_map["info"])

        html = f"""
        <div class="aeva-glass-panel-neon" style="
            position: fixed;
            bottom: var(--aeva-space-safe-bottom);
            right: var(--aeva-space-safe-right);
            max-width: 400px;
            padding: var(--aeva-space-lg);
            margin: var(--aeva-space-lg);
            z-index: 50;
            animation: aeva-animate-slide-up 0.3s var(--aeva-easing-bounce);
            border-left: 3px solid {color};
        ">
            <div style="color: var(--aeva-text-primary); font-size: 0.95rem;">
                {message}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    @staticmethod
    def render_glass_button(
        label: str,
        onclick: Optional[str] = None,
        button_type: str = "primary",
        size: str = "md",
        full_width: bool = False,
    ) -> None:
        """Render a glass-styled button."""
        size_map = {
            "sm": "var(--aeva-space-md) var(--aeva-space-lg)",
            "md": "var(--aeva-space-lg) var(--aeva-space-xl)",
            "lg": "var(--aeva-space-lg) var(--aeva-space-2xl)",
        }
        padding = size_map.get(size, size_map["md"])
        width_style = "width: 100%;" if full_width else ""

        html = f"""
        <button class="aeva-glass-panel-neon aeva-touch-target" style="
            {width_style}
            padding: {padding};
            border: none;
            cursor: pointer;
            color: var(--aeva-accent-neon);
            font-weight: 600;
            font-size: 0.95rem;
            transition: all var(--aeva-duration-fast) var(--aeva-easing-smooth);
            letter-spacing: 1px;
        " onclick="{onclick}">
            {label}
        </button>
        """
        st.markdown(html, unsafe_allow_html=True)

    @staticmethod
    def render_streaming_hud(
        tokens_current: int,
        tokens_speed: float,
        model_name: str,
        studio_name: str,
    ) -> None:
        """
        Render real-time streaming HUD with neon indicators.
        
        Args:
            tokens_current: Current token count
            tokens_speed: Tokens per second streaming speed
            model_name: Active model name
            studio_name: Current studio name
        """
        html = f"""
        <div class="aeva-glass-panel-neon" style="
            position: fixed;
            top: var(--aeva-space-safe-top);
            right: var(--aeva-space-safe-right);
            width: 320px;
            padding: var(--aeva-space-lg);
            margin: var(--aeva-space-lg);
            z-index: 40;
            animation: aeva-animate-fade-in 0.4s var(--aeva-easing-smooth);
            border: 1px solid rgba(118, 185, 0, 0.5);
            backdrop-filter: blur(10px);
        ">
            <div style="
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: var(--aeva-space-md);
            ">
                <!-- Tokens Indicator -->
                <div style="
                    padding: var(--aeva-space-md);
                    background: rgba(118, 185, 0, 0.1);
                    border-radius: var(--aeva-radius-md);
                    border-left: 3px solid var(--aeva-accent-neon);
                ">
                    <div style="
                        color: var(--aeva-text-secondary);
                        font-size: 0.75rem;
                        letter-spacing: 1px;
                        margin-bottom: 4px;
                    ">
                        TOKENS
                    </div>
                    <div style="
                        color: var(--aeva-accent-neon);
                        font-size: 1.4rem;
                        font-weight: bold;
                    ">
                        {tokens_current}
                    </div>
                </div>
                
                <!-- Speed Indicator -->
                <div style="
                    padding: var(--aeva-space-md);
                    background: rgba(0, 217, 255, 0.1);
                    border-radius: var(--aeva-radius-md);
                    border-left: 3px solid var(--aeva-accent-cyan);
                ">
                    <div style="
                        color: var(--aeva-text-secondary);
                        font-size: 0.75rem;
                        letter-spacing: 1px;
                        margin-bottom: 4px;
                    ">
                        SPEED
                    </div>
                    <div style="
                        color: var(--aeva-accent-cyan);
                        font-size: 1.2rem;
                        font-weight: bold;
                    ">
                        {tokens_speed:.1f}t/s
                    </div>
                </div>
                
                <!-- Model Badge -->
                <div style="
                    grid-column: 1 / -1;
                    padding: var(--aeva-space-sm);
                    background: rgba(69, 162, 158, 0.1);
                    border-radius: var(--aeva-radius-md);
                    border: 1px solid rgba(69, 162, 158, 0.3);
                    text-align: center;
                ">
                    <div style="
                        color: var(--aeva-text-secondary);
                        font-size: 0.7rem;
                        letter-spacing: 1px;
                        margin-bottom: 2px;
                    ">
                        {studio_name.upper()} • {model_name.split('/')[-1]}
                    </div>
                </div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)


def inject_css() -> None:
    """Inject design system CSS into Streamlit app."""
    with open("core/tokens.css", "r") as f:
        css_content = f.read()

    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def get_color_value(color_name: str) -> str:
    """Get color value from design system."""
    colors = {
        "carbon": "#0B0C10",
        "dark": "#16213E",
        "glass": "#1F2833",
        "neon": "#76B900",
        "titanium": "#45A29E",
        "cyan": "#00D9FF",
        "purple": "#9D4EDD",
        "text": "#ECEFF1",
        "text-secondary": "#90A4AE",
        "danger": "#FF4757",
        "warning": "#FFA502",
        "success": "#2ED573",
    }
    return colors.get(color_name, "#ECEFF1")
