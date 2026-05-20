# 🚀 AEVA OS - Installation & Launch Commands

## 📋 Quick Reference

### **Minimum Installation** (30 seconds)

```bash
# 1. Install core packages
pip install streamlit requests aiohttp pandas

# 2. Configure API key
export NVIDIA_API_KEY="your_api_key_here"

# 3. Launch
streamlit run app.py --server.port 8501
```

---

## 🔧 Full Installation (Production-Ready)

### **Step 1: Clone Repository**

```bash
cd /workspaces/AEVA
```

### **Step 2: Create Virtual Environment** (Recommended)

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### **Step 3: Install All Dependencies**

**Option A: Using requirements.txt (Recommended)**

```bash
pip install -r requirements.txt
```

**Option B: Manual Installation**

```bash
pip install \
  streamlit==1.28.1 \
  streamlit-option-menu==0.3.6 \
  requests==2.31.0 \
  aiohttp==3.9.0 \
  pandas==2.1.1 \
  numpy==1.24.3 \
  pyarrow==13.0.0 \
  python-dotenv==1.0.0 \
  plotly==5.17.0 \
  scikit-learn==1.3.1
```

### **Step 4: Configure Environment**

```bash
# Copy example config
cp .env.example .env

# Edit and add your NVIDIA API key
# Option 1: nano (macOS/Linux)
nano .env

# Option 2: Edit file directly
# Add line: NVIDIA_API_KEY=your_api_key_here

# Option 3: Export as environment variable
export NVIDIA_API_KEY="nvapi_xxxxxxxxxxxxxxxxxxxxxxxx"
```

### **Step 5: Launch the Application**

```bash
# Standard launch
streamlit run app.py

# Or with explicit port (default: 8501)
streamlit run app.py --server.port 8501

# With custom configuration
streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --logger.level info
```

**Access Application:** `http://localhost:8501`

---

## 🐳 Docker Setup

### **Option 1: Docker Run**

```bash
# Build image
docker build -t aeva-os .

# Run container
docker run -p 8501:8501 \
  -e NVIDIA_API_KEY="your_key_here" \
  -v $(pwd)/data:/app/data \
  aeva-os

# Access at http://localhost:8501
```

### **Option 2: Docker Compose** (Recommended)

```bash
# 1. Create .env file with API key
echo 'NVIDIA_API_KEY=your_key_here' > .env

# 2. Start container
docker-compose up -d

# 3. View logs
docker-compose logs -f aeva-os

# 4. Stop container
docker-compose down
```

---

## ☁️ Cloud Deployment Commands

### **Streamlit Cloud**

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to https://share.streamlit.io
# 3. New app → Select repo/branch
# 4. Advanced settings → Add environment variable
# 5. Deploy!
```

### **Heroku**

```bash
# Login to Heroku
heroku login

# Create app
heroku create aeva-os

# Set API key
heroku config:set NVIDIA_API_KEY="your_key_here"

# Create Procfile
echo 'web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0' > Procfile

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### **AWS EC2**

```bash
# SSH into instance
ssh -i key.pem ec2-user@instance-ip

# Install dependencies
sudo yum install python3 python3-pip git -y
git clone https://github.com/aeva-os/aeva-os.git
cd AEVA
pip3 install -r requirements.txt

# Set API key
export NVIDIA_API_KEY="your_key_here"

# Run in background
nohup streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 > app.log 2>&1 &

# Access at http://instance-ip:8501
```

### **Google Cloud Run**

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy aeva-os \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --set-env-vars NVIDIA_API_KEY=your_key_here \
  --allow-unauthenticated
```

---

## 📊 Package Installation Summary

### **Complete Installation Command** (One-liner)

```bash
pip install streamlit==1.28.1 streamlit-option-menu==0.3.6 \
  requests==2.31.0 aiohttp==3.9.0 openai==1.0.0 \
  pandas==2.1.1 numpy==1.24.3 pyarrow==13.0.0 \
  streamlit-lottie==0.0.5 python-dotenv==1.0.0 \
  plotly==5.17.0 scikit-learn==1.3.1
```

### **Package Breakdown**

| Category | Package | Version | Purpose |
|----------|---------|---------|---------|
| **Core** | streamlit | 1.28.1 | Web framework |
| | requests | 2.31.0 | HTTP requests |
| | aiohttp | 3.9.0 | Async HTTP |
| **Data** | pandas | 2.1.1 | Data processing |
| | numpy | 1.24.3 | Numerical computing |
| | pyarrow | 13.0.0 | Data serialization |
| **UI** | streamlit-option-menu | 0.3.6 | Menu component |
| | streamlit-lottie | 0.0.5 | Animations |
| **Config** | python-dotenv | 1.0.0 | Environment vars |
| **ML** | scikit-learn | 1.3.1 | ML algorithms |
| **Viz** | plotly | 5.17.0 | Interactive charts |

---

## 🔍 Verification Commands

### **Verify Installation**

```bash
# Check Streamlit version
streamlit --version

# Test imports
python -c "
import streamlit as st
import requests
import pandas as pd
import numpy as np
print('✓ Core packages installed')
"

# Verify project structure
ls -la app.py core/ ai/ modules/ utils/ requirements.txt

# Test API key
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('NVIDIA_API_KEY')
if api_key:
    print(f'✓ API key configured: {api_key[:20]}...')
else:
    print('⚠ API key not found')
"
```

### **Run Smoke Test**

```bash
# Start with debug logging
streamlit run app.py --logger.level debug

# Watch for startup messages:
# ✓ Cache type: In-memory
# ✓ Caching is on
# ✓ Running on local URL: http://localhost:8501
```

---

## 🚀 Launch Scenarios

### **Development (Hot Reload)**

```bash
streamlit run app.py \
  --client.showErrorDetails=true \
  --server.runOnSave=true \
  --logger.level=debug
```

### **Production (Optimized)**

```bash
streamlit run app.py \
  --server.headless=true \
  --logger.level=warning \
  --client.showErrorDetails=false \
  --server.port=8501 \
  --server.address=0.0.0.0
```

### **Performance Testing**

```bash
# With memory/CPU monitoring (macOS/Linux)
time streamlit run app.py

# With verbose output
streamlit run app.py --logger.level=debug
```

---

## 🆘 Common Issues & Fixes

### **Port Already in Use**

```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
lsof -ti:8501 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8501   # Windows
```

### **Module Not Found**

```bash
# Reinstall specific package
pip install --upgrade streamlit

# Or reinstall all
pip install -r requirements.txt --force-reinstall
```

### **API Key Issues**

```bash
# Verify key is loaded
python -c "import os; print(os.getenv('NVIDIA_API_KEY'))"

# Test API connectivity
curl -X POST https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/llama2-7b","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

---

## 📦 Requirements File Format

The `requirements.txt` specifies exact versions for reproducibility:

```
streamlit==1.28.1
requests==2.31.0
aiohttp==3.9.0
pandas==2.1.1
numpy==1.24.3
```

**To update all packages to latest:**

```bash
pip list --outdated
pip install --upgrade -r requirements.txt
```

---

## ✅ Final Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created & activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with `NVIDIA_API_KEY`
- [ ] API key validated
- [ ] Port 8501 available
- [ ] Project structure verified
- [ ] Streamlit configured
- [ ] Application launched

---

## 🎯 Next Steps After Installation

1. **Initial Boot**: App will show loading animation (~2.5s)
2. **API Configuration**: Enter NVIDIA API key on first run
3. **Select Model**: Choose preferred AI model
4. **Explore Workspaces**:
   - 💬 Chat: Interactive AI conversations
   - 📖 Novel Studio: Creative writing workspace
   - 🔬 Quantum Forge: Scientific data analysis
   - 📊 Dev Studio: Deployment monitoring

---

## 📞 Support

- **Docs**: https://aeva.dev/docs
- **Issues**: https://github.com/aeva-os/issues
- **Setup Help**: https://aeva.dev/setup

---

**Ready? Run:**

```bash
pip install -r requirements.txt && \
export NVIDIA_API_KEY="your_key_here" && \
streamlit run app.py --server.port 8501
```

**⬡ AEVA OS Launching...**
