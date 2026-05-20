# 🚀 AEVA OS - Complete Setup Guide

## Quick Setup (5 minutes)

### 1️⃣ **Clone & Navigate**

```bash
cd /workspaces/AEVA
```

### 2️⃣ **Install Dependencies**

```bash
pip install streamlit==1.28.1 requests==2.31.0 aiohttp==3.9.0 \
  pandas==2.1.1 numpy==1.24.3 python-dotenv==1.0.0
```

Or use the full requirements:

```bash
pip install -r requirements.txt
```

### 3️⃣ **Get NVIDIA API Key**

1. Visit: https://integrate.api.nvidia.com
2. Sign up / Log in
3. Create API key
4. Copy the key

### 4️⃣ **Configure Environment**

```bash
cp .env.example .env
# Edit .env and add your NVIDIA_API_KEY
nano .env
```

### 5️⃣ **Launch Application**

```bash
streamlit run app.py --server.port 8501
```

✅ **Done!** Open browser to `http://localhost:8501`

---

## Detailed Installation Guide

### **Local Machine Setup**

#### Prerequisites

- Python 3.9+ ([Download](https://www.python.org/downloads/))
- pip or conda
- Git

#### Step-by-Step

```bash
# 1. Clone repository
git clone https://github.com/aeva-os/aeva-os.git
cd AEVA

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create .env file
cp .env.example .env

# 7. Edit .env with your API key
# macOS/Linux:
nano .env
# Windows:
notepad .env

# Add your NVIDIA API key:
# NVIDIA_API_KEY=nvapi_xxxxxxxxxxxxx

# 8. Run the app
streamlit run app.py
```

### **Gitpod/GitHub Codespaces Setup**

```bash
# In terminal, run all at once:
pip install streamlit requests aiohttp pandas numpy python-dotenv && \
cp .env.example .env && \
echo "NVIDIA_API_KEY=your_key_here" >> .env && \
streamlit run app.py --server.port 8501
```

### **Docker Setup**

```bash
# 1. Build image
docker build -t aeva-os .

# 2. Run container
docker run -p 8501:8501 \
  -e NVIDIA_API_KEY=your_key_here \
  aeva-os

# 3. Access at http://localhost:8501
```

### **Conda Setup**

```bash
# 1. Create conda environment
conda create -n aeva-os python=3.11

# 2. Activate environment
conda activate aeva-os

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run app
streamlit run app.py
```

---

## Cloud Deployment

### **Streamlit Cloud (Recommended)**

1. Push repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select repository, branch, main file: `app.py`
5. In "Advanced settings", add:
   ```
   NVIDIA_API_KEY = your_key_here
   ```
6. Deploy! 🚀

### **Heroku Deployment**

```bash
# 1. Create Heroku app
heroku create aeva-os

# 2. Add buildpacks
heroku buildpacks:add heroku/python

# 3. Set environment variable
heroku config:set NVIDIA_API_KEY=your_key_here

# 4. Create Procfile
echo "web: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0" > Procfile

# 5. Deploy
git push heroku main

# 6. View logs
heroku logs --tail
```

### **AWS EC2 Setup**

```bash
# 1. SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance.com

# 2. Install Python
sudo yum install python3 python3-pip -y

# 3. Clone repository
git clone https://github.com/aeva-os/aeva-os.git
cd AEVA

# 4. Install dependencies
pip3 install -r requirements.txt

# 5. Set API key
export NVIDIA_API_KEY=your_key_here

# 6. Run app (with nohup to keep running)
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > app.log 2>&1 &

# 7. Access via http://your-instance-public-ip:8501
```

### **Google Cloud Run**

```bash
# 1. Create Dockerfile (already included)
# 2. Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/aeva-os

# 3. Deploy to Cloud Run
gcloud run deploy aeva-os \
  --image gcr.io/YOUR_PROJECT_ID/aeva-os \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --set-env-vars NVIDIA_API_KEY=your_key_here

# 4. Access the service URL
```

### **Azure App Service**

```bash
# 1. Create resource group
az group create -n aeva-os -l eastus

# 2. Create app service plan
az appservice plan create -n aeva-os-plan -g aeva-os

# 3. Create web app
az webapp create -n aeva-os -g aeva-os -p aeva-os-plan \
  --runtime "PYTHON|3.11"

# 4. Set environment variables
az webapp config appsettings set -n aeva-os -g aeva-os \
  --settings NVIDIA_API_KEY=your_key_here

# 5. Deploy
git push azure main
```

---

## Verification & Testing

### **Test Installation**

```bash
# 1. Verify Python
python --version  # Should be 3.9+

# 2. Verify packages
pip list | grep -E "streamlit|requests|pandas"

# 3. Test imports
python -c "
import streamlit
import requests
import pandas
from core.state import get_state_manager
print('✓ All imports successful!')
"

# 4. Validate API key
python -c "
from ai.provider import AIProviderAbstraction
import os
api_key = os.getenv('NVIDIA_API_KEY')
if api_key:
    print(f'✓ API Key found: {api_key[:20]}...')
else:
    print('✗ API Key not set in environment')
"
```

### **Smoke Test**

```bash
# Run with debug mode
streamlit run app.py --logger.level=debug

# Check for errors in startup
# Should see:
# ✓ Cache type: In-memory
# ✓ Caching is on.
# ✓ Running on local URL:  http://localhost:8501
```

---

## Troubleshooting

### **Port Already in Use**

```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill process on port 8501
# macOS/Linux:
lsof -ti:8501 | xargs kill -9

# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### **API Key Issues**

```bash
# Verify key is set
echo $NVIDIA_API_KEY

# Test connectivity
curl -X POST https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/llama2-7b","messages":[{"role":"user","content":"test"}],"max_tokens":10}'

# Should return 200 OK
```

### **Module Import Errors**

```bash
# Verify project structure
ls -la app.py core/ ai/ modules/ utils/

# Reinstall dependencies
pip uninstall -y streamlit requests aiohttp pandas numpy
pip install streamlit==1.28.1 requests==2.31.0 aiohttp==3.9.0 pandas==2.1.1 numpy==1.24.3

# Clear cache
streamlit cache clear
```

### **Memory/Performance Issues**

```bash
# Increase allocated memory
STREAMLIT_MAX_UPLOAD_SIZE=5 \
STREAMLIT_CLIENT_MAX_MESSAGE_SIZE=10 \
streamlit run app.py

# Or edit ~/.streamlit/config.toml:
# [client]
# maxMessageSize = 10
# maxUploadSize = 5
```

---

## Configuration

### **Environment Variables**

```bash
# .env file
NVIDIA_API_KEY=nvapi_xxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxx  # Optional fallback
AEVA_DEBUG=true                    # Enable debug logging
AEVA_PORT=8501                     # Server port
MAX_TOKENS=2048                    # Max tokens per request
CACHE_DIR=./.streamlit/cache       # Cache location
LOG_LEVEL=INFO                     # Logging level
```

### **Streamlit Configuration**

Create `~/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#76B900"
backgroundColor = "#0B0C10"
secondaryBackgroundColor = "#1F2833"
textColor = "#ECEFF1"

[server]
port = 8501
headless = true
runOnSave = true

[logger]
level = "info"

[client]
toolbarMode = "minimal"
showErrorDetails = true
maxMessageSize = 10
```

---

## Performance Tuning

### **Optimization Checklist**

```bash
# 1. Use production flag
streamlit run app.py --logger.level=warning

# 2. Enable caching
STREAMLIT_CACHE_CONTROL="no-cache, no-store, must-revalidate" streamlit run app.py

# 3. Allocate resources
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=4

# 4. Async provider for better concurrency
# (Already implemented in ai/provider.py)

# 5. Monitor resources
# Linux:
watch -n 1 'ps aux | grep streamlit'
```

---

## Next Steps

1. **Explore Workspaces**: Chat → Novel Studio → Quantum Forge → Dev Studio
2. **Read Full Docs**: `README.md`
3. **Check Examples**: `/examples` directory
4. **Join Community**: GitHub Discussions
5. **Submit Issues**: GitHub Issues

---

## Support

- **Docs**: https://aeva.dev/docs
- **Issues**: https://github.com/aeva-os/issues
- **Discussions**: https://github.com/aeva-os/discussions
- **Email**: support@aeva.dev

---

**Ready to launch? Run:**

```bash
streamlit run app.py --server.port 8501
```

**Happy coding! ⬡**
