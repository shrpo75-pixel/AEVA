# ⬡ AEVA OS - Premium Futuristic AI Operating System

**A mobile-first, cloud-native AI operating system with native support for NVIDIA's Build API.**

![AEVA OS](assets/banner.png)

## 🎯 Overview

AEVA OS is a next-generation AI operating system designed with:

- **Mobile-First Architecture**: Responsive design from 320px phones to 4K desktops
- **Film Noir + NVIDIA Cyberpunk Design**: Deep carbon (#0B0C10) with neon green accents (#76B900) and titanium highlights (#45A29E)
- **Glassmorphism UI**: GPU-optimized blur effects, smooth animations, and modern aesthetics
- **Modular Workspaces**: Chat, Novel Studio, Quantum Forge, Dev Studio
- **Token Streaming**: Real-time AI response generation with abort capabilities
- **Secure Configuration**: Session-based API key management with localStorage proxying

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- Streamlit 1.28+
- NVIDIA API Key (get it from [integrate.api.nvidia.com](https://integrate.api.nvidia.com))

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/aeva-os/aeva-os.git
cd AEVA

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your NVIDIA API Key
nano .env
```

### 3. Launch the Application

```bash
# Run the Streamlit server on port 8501
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Or with custom configuration
streamlit run app.py \
  --logger.level=info \
  --client.showErrorDetails=true \
  --server.runOnSave=true
```

The application will be available at `http://localhost:8501`

## 📁 Project Structure

```
AEVA/
├── app.py                          # Main entry point with boot sequence
├── core/
│   ├── tokens.css                 # Design system tokens & animations
│   └── state.py                   # Global state manager (Streamlit session_state)
├── ai/
│   └── provider.py                # NVIDIA API provider abstraction
├── modules/
│   ├── chat.py                    # Chat workspace with Quantum Orb
│   ├── novel.py                   # Novel Studio (3-panel editor)
│   ├── forge.py                   # Quantum Forge (Scientific HUD)
│   └── dev.py                     # Dev Studio (Deployment Dashboard)
├── utils/
│   └── ui_components.py           # Reusable UI components
├── data/                          # Persistent state storage
├── assets/                        # Media & branding
└── requirements.txt               # Python dependencies
```

## 🎨 Design System

### Color Palette

| Role | Color | Usage |
|------|-------|-------|
| **Background** | #0B0C10 (Carbon) | Deep base layer |
| **Panels** | #1F2833 (Glass Dark) | Glassmorphism containers |
| **Primary Accent** | #76B900 (Neon Green) | Interactive elements, CTAs |
| **Secondary Accent** | #45A29E (Titanium) | Status, highlights |
| **Tertiary Accent** | #00D9FF (Cyan) | Data visualization |
| **Text Primary** | #ECEFF1 | Main content |
| **Text Secondary** | #90A4AE | Supporting text |

### Animation Presets

- **Fade In**: 300ms smooth fade
- **Slide Up**: 300ms entrance from bottom
- **Scale Pop**: 150ms bounce entrance
- **Pulse Glow**: Adaptive 2-3s glow effect
- **Rotate Ring**: 3s continuous rotation
- **Shimmer**: 2s gradient shimmer

### Glassmorphism Effects

- `backdrop-filter: blur(12-24px)`
- `background: rgba(31, 40, 51, 0.08-0.16)`
- `border: 1px solid rgba(118, 185, 0, 0.1-0.3)`
- Neon/Titanium glow shadows (0-32px)

## 🔧 Core Modules

### 1. **App Entry Point** (`app.py`)

- Boot sequence animation (2.5s)
- API key configuration & validation
- Workspace routing
- Sidebar navigation
- Command palette (Ctrl+K / Cmd+K)

### 2. **State Management** (`core/state.py`)

Global state manager with session persistence:

```python
state = get_state_manager()

# API Management
state.configure_api_key(api_key)
state.get_api_key()

# Chat History
state.add_to_chat_history("user", "Hello")
state.get_chat_history()

# Workspace Control
state.switch_workspace("chat")

# Token Tracking
state.update_token_count(245)

# Notifications
state.add_notification("Success!", "success")
```

### 3. **AI Provider** (`ai/provider.py`)

NVIDIA Build API integration with streaming support:

```python
from ai.provider import ProviderFactory

# Create provider
provider = ProviderFactory.create("nvidia", use_env=True)

# Non-streaming completion
response = provider.chat_completion(
    messages=[{"role": "user", "content": "Hello"}],
    model="nvidia/llama2-70b",
    max_tokens=2048
)

# Token-by-token streaming
for token in provider.chat_completion_stream(messages):
    print(token, end="", flush=True)

# Request abort
provider.request_abort()
```

### 4. **Chat Workspace** (`modules/chat.py`)

Features:
- **Quantum Orb**: Animated focal point with model-aware pulse rates
  - Reasoning models → Slow titanium pulse
  - Lightweight models → Fast neon pulse
  - Coding models → Electric waveform
  - Vision models → Rotating rings
- **Immersive Chat UI**: Glass containers, smooth fade-ins
- **Multi-line Input**: Responsive text area with send button
- **File Upload**: Image & PDF support with previews
- **Voice Input**: Placeholder for future implementation

### 5. **Novel Studio** (`modules/novel.py`)

3-panel adaptive workspace:

**Desktop Layout:**
- **Left Panel (Plot Map)**: Chapter tree, timeline, character maps
- **Center Panel (Focus Writing)**: Distraction-free editor
- **Right Panel (Prompt Core)**: Rewrite tools, tone presets, cover generation

**Mobile Layout:** Swipeable tabs with gesture-based switching

### 6. **Quantum Forge** (`modules/forge.py`)

Scientific HUD features:
- 3D Graph Viewport (animated grid background)
- Mathematical Equation Panels (with LaTeX rendering)
- Dataset Upload Drop-zone (CSV/Excel/JSON/Parquet)
- Real-time Analysis Metrics
- Confidence Indicators & Progress Trackers

### 7. **Dev Studio** (`modules/dev.py`)

Deployment dashboard with:
- System Metrics Cards (CPU, Memory, Network, Health)
- Git Diff Viewer (green additions, red removals)
- Task Orchestration Timeline (real-time status)
- Deployment Controls with prominent "Approve & Deploy" CTA

## 🎯 Advanced Features

### Command Palette Engine

```
Keyboard Shortcuts:
- Ctrl+K / Cmd+K: Open command palette
- Ctrl+Q / Cmd+Q: Quick workspace switcher
```

### Notification Framework

```python
state.add_notification(
    "Operation completed",
    notification_type="success",  # "info", "warning", "error", "success"
    duration=3000
)
```

### Memory Compression

Background worker that summarizes long chat histories:

```python
if state.should_compress_memory():
    state.mark_memory_compressed()
    # Auto-summarization happens asynchronously
```

### Persistent State Management

```python
# Save to disk
state.save_state_to_disk("chat_backup.json")

# Load from disk
state.load_state_from_disk("chat_backup.json")
```

## 📊 Performance Optimization

All animations are GPU-accelerated:

```css
.aeva-gpu-accel {
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 1000px;
}
```

Features:
- ✓ 60fps animations on mobile GPUs
- ✓ No layout shifts during streaming
- ✓ Hardware-accelerated blur effects
- ✓ Keyboard overlap prevention on mobile

## 🔐 Security

### API Key Management

- Keys stored in Streamlit `session_state` (in-memory)
- Never logged to console
- Cleared on logout
- Environment variable fallback
- Validation endpoint check

### Data Privacy

- All state can be saved/loaded
- Sensitive data excluded from exports
- Local processing, no telemetry
- GDPR-compliant

## 🌐 Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.port", "8501", \
     "--server.address", "0.0.0.0"]
```

### Cloud Platforms

**Streamlit Cloud:**
```bash
git push  # Automatic deployment
```

**Heroku:**
```bash
git push heroku main
```

**AWS EC2/ECS, GCP Cloud Run, Azure App Service:** Standard Python deployment

## 📦 Installation Commands

### For Gitpod/Codespace:

```bash
# Install packages
pip install streamlit==1.28.1 requests==2.31.0 aiohttp==3.9.0 \
  pandas==2.1.1 numpy==1.24.3 python-dotenv==1.0.0

# Launch server on port 8501
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 📚 API Documentation

### NVIDIA Build API Endpoint

**Base URL:** `https://integrate.api.nvidia.com/v1/chat/completions`

**Available Models:**
- `nvidia/llama2-70b` - Reasoning
- `nvidia/llama2-13b` - Balanced
- `nvidia/llama2-7b` - Lightweight
- `nvidia/mistral-7b` - Code
- `nvidia/mixtral-8x7b` - Hybrid

**Request Example:**

```bash
curl -X POST https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/llama2-70b",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.7,
    "max_tokens": 2048,
    "stream": true
  }'
```

## 🛠️ Troubleshooting

### API Key Not Working

```bash
# Validate key
python -c "
from ai.provider import AIProviderAbstraction
from core.state import get_state_manager
state = get_state_manager()
state.configure_api_key('your_key')
provider = AIProviderAbstraction.from_session_state()
print('Valid!' if provider.validate_api_key() else 'Invalid!')
"
```

### Streamlit Caching Issues

```bash
streamlit cache clear
streamlit run app.py
```

### Port Already in Use

```bash
streamlit run app.py --server.port 8502
```

## 📈 Roadmap

- [ ] Voice input/output
- [ ] Vision model integration
- [ ] Advanced 3D visualization
- [ ] Collaborative editing
- [ ] Multi-user sessions
- [ ] Plugin system
- [ ] Mobile native apps
- [ ] Offline mode

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **Design Inspiration:** Film Noir + NVIDIA Cyberpunk aesthetic
- **Technology:** Streamlit, NVIDIA Build API, Python
- **Community:** Open-source contributors

## 📞 Support

- **Documentation**: `/docs`
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@aeva.dev

---

**Built with ⬡ for the future of AI**

*AEVA OS v1.0 ALPHA - Mobile-First, Cloud-Native, Enterprise-Ready*
