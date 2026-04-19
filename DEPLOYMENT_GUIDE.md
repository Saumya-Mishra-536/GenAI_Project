# Deployment Guide: Vercel (Frontend) + Render (Backend)

## Overview

This guide covers deploying the **EV Charging Demand Prediction System** to production:
- **Frontend**: React 19 + Vite → **Vercel**
- **Backend**: FastAPI + Streamlit → **Render**

---

## Part 1: Frontend Deployment on Vercel

### 1.1 Prerequisites

- [ ] GitHub account with repository access
- [ ] Vercel account (free tier sufficient) - [vercel.com](https://vercel.com)
- [ ] Repository pushed to GitHub

### 1.2 Prepare Frontend for Deployment

#### Step 1: Update Frontend Configuration

**File:** `End_sem/frontend/vite.config.js` (already configured)

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false,
  }
})
```

#### Step 2: Environment Variables

Create a `.env.production` file in `End_sem/frontend/`:

```bash
VITE_API_URL=https://your-backend-url.onrender.com/api
```

**⚠️ Important:** Replace `your-backend-url.onrender.com` with your actual Render backend URL (we'll create this in Part 2).

#### Step 3: Verify index.html Exists

**CRITICAL:** Vite requires an `index.html` file in the frontend root directory. This file should exist at `End_sem/frontend/index.html`.

```bash
# Verify the file exists
ls -la End_sem/frontend/index.html

# If it doesn't exist, it will be created automatically
# But you can also verify with:
cat End_sem/frontend/index.html | head -5
```

#### Step 4: Verify Build Locally

```bash
cd End_sem/frontend
npm install
npm run build
npm run preview
```

Expected output:
```
✓ built in 5.23s
vite v5.4.21 building for production...
dist/index.html                     0.46 kB │ gzip:  0.28 kB
dist/assets/index-xxxxx.js       150.23 kB │ gzip: 45.32 kB
```

**If you get an error like "Could not resolve entry module index.html":**
- See [VERCEL_BUILD_FIX.md](VERCEL_BUILD_FIX.md) for the solution

### 1.3 Deploy to Vercel

#### Method 1: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to frontend directory
cd End_sem/frontend

# Deploy
vercel --prod
```

Follow the prompts:
- **Project name:** `genai-ev-frontend`
- **Framework:** Select "Vite"
- **Build command:** `npm run build` (should auto-detect)
- **Output directory:** `dist` (should auto-detect)
- **Install command:** `npm install`

#### Method 2: Using Vercel Web Dashboard

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..." → "Project"**
3. Import your GitHub repository
4. Select the `End_sem/frontend` folder as root directory
5. Configure environment variables (see Step 4 below)
6. Click **Deploy**

### 1.4 Configure Environment Variables on Vercel

1. Go to **Project Settings** → **Environment Variables**
2. Add the following variables:

| Key | Value | Environment |
|-----|-------|-------------|
| `VITE_API_URL` | `https://your-backend-url.onrender.com/api` | Production |

3. Redeploy after adding environment variables

### 1.5 Verify Frontend Deployment

Once deployment completes:

1. Your frontend URL will be: `https://your-project.vercel.app`
2. Test the application:
   - Open `https://your-project.vercel.app`
   - You should see the Landing page
   - Navigation should work

**Troubleshooting Frontend:**
- Check browser console (F12) for API connection errors
- Verify `VITE_API_URL` is correctly set in Vercel environment variables
- Ensure backend is running (will complete in Part 2)

---

## Part 2: Backend Deployment on Render

### 2.1 Prerequisites

- [ ] Render account (free tier) - [render.com](https://render.com)
- [ ] GitHub repository with backend code
- [ ] OpenRouter API key - [openrouter.ai](https://openrouter.ai)

### 2.2 Prepare Backend for Deployment

#### Step 1: Create Render-Specific Configuration

Create `End_sem/backend/render.yaml`:

```yaml
services:
  - type: web
    name: genai-ev-backend
    runtime: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port 8000"
    healthCheckPath: /api/health
    envVars:
      - key: PYTHON_VERSION
        value: 3.10
      - key: PORT
        value: 8000
```

#### Step 2: Update Backend Entry Point

Create `End_sem/backend/main.py` (if not exists):

```python
"""
FastAPI Entry Point for Render Deployment
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys

# Import your existing FastAPI app
# Adjust this based on your actual backend structure
try:
    # If streamlit_app.py contains the FastAPI app, create a separate main.py
    # For now, we'll create a minimal FastAPI app that wraps your logic
    
    app = FastAPI(title="EV Charging Backend", version="1.0.0")
    
    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health Check
    @app.get("/api/health")
    async def health_check():
        return {"status": "healthy", "service": "EV-Charging-Backend"}
    
    # Import and include your API routes
    # from routes import predict_router, batch_router, agent_router
    # app.include_router(predict_router, prefix="/api")
    # app.include_router(batch_router, prefix="/api")
    # app.include_router(agent_router, prefix="/api")
    
except Exception as e:
    print(f"Error initializing FastAPI app: {e}")
    raise

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

#### Step 3: Update Requirements.txt

Ensure `End_sem/backend/requirements.txt` includes Uvicorn:

```
fastapi
uvicorn[standard]
python-dotenv
pandas
numpy
openpyxl
scikit-learn
joblib
plotly
langchain
langchain-core
langchain-community
langchain-openai
langchain-huggingface
langchain-text-splitters
langgraph
sentence-transformers
faiss-cpu
python-multipart
pydantic
```

#### Step 4: Create .gitignore

Ensure sensitive files are not committed:

```
# Environment
.env
.env.local
.env.*.local

# Cache
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/

# Models
models/*.joblib
*.pkl

# Node
node_modules/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

### 2.3 Deploy to Render

#### Step 1: Create Web Service on Render

1. Go to [render.com/dashboard](https://dashboard.render.com)
2. Click **"New +" → "Web Service"**
3. Connect your GitHub repository
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `genai-ev-backend` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r End_sem/backend/requirements.txt` |
| **Start Command** | `cd End_sem/backend && uvicorn main:app --host 0.0.0.0 --port 8000` |
| **Instance Type** | `Starter` (free tier) |

#### Step 2: Add Environment Variables

In Render Dashboard → **Environment**:

| Key | Value |
|-----|-------|
| `OPENROUTER_API_KEY` | `sk-or-v1-...` (your OpenRouter API key) |
| `OPENROUTER_BASE_URL` | `https://openrouter.ai/api/v1` |
| `MODEL_NAME` | `nvidia/nemotron-3-super-120b-a12b:free` |
| `EMBEDDINGS_MODEL` | `all-MiniLM-L6-v2` |
| `PYTHONUNBUFFERED` | `1` |

**⚠️ Security:** Never commit API keys. Use Render's environment variable system.

#### Step 3: Deploy

1. Click **"Create Web Service"**
2. Render will automatically build and deploy
3. You'll receive a unique URL: `https://genai-ev-backend.onrender.com`

**Initial deployment may take 5-10 minutes.**

### 2.4 Verify Backend Deployment

#### Check Health Endpoint

```bash
curl https://genai-ev-backend.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "EV-Charging-Backend"
}
```

#### Monitor Logs

In Render Dashboard:
1. Click your service
2. Go to **Logs**
3. Watch for errors during startup

### 2.5 Configure CORS for Frontend

Update backend CORS settings to allow Vercel frontend:

In `End_sem/backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",  # Add Vercel URL
        "http://localhost:3000",              # Local development
        "http://localhost:5173",              # Local Vite dev
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

---

## Part 3: Connect Frontend to Backend

### 3.1 Update Frontend API URL

Once backend is deployed, update frontend:

1. **On Vercel Dashboard:**
   - Go to **Settings → Environment Variables**
   - Update `VITE_API_URL` to your Render backend URL:
     ```
     https://genai-ev-backend.onrender.com/api
     ```

2. **Trigger Redeployment:**
   - Vercel automatically redeploys when environment variables change
   - Or manually trigger from **Deployments** tab

### 3.2 Test End-to-End

1. Open your Vercel frontend URL
2. Navigate to any page that makes API calls
3. Open browser DevTools (F12) → **Network** tab
4. Verify API requests go to your Render backend
5. Check responses are successful (200 status codes)

---

## Part 4: Production Monitoring & Maintenance

### 4.1 Monitoring

**Vercel Monitoring:**
- Dashboard shows real-time metrics
- Check **Logs** for errors
- Set up alerts in **Integrations**

**Render Monitoring:**
- Dashboard shows resource usage
- Check **Logs** for backend errors
- Set up metrics in **Monitoring** tab

### 4.2 Scaling

**If Frontend Gets Heavy Traffic (Vercel):**
- Vercel auto-scales (no action needed on free tier)
- Monitor build times and bandwidth

**If Backend Gets Heavy Traffic (Render):**
- Upgrade from `Starter` to `Standard` instance
- Add Redis caching for model predictions
- Consider using PostgreSQL instead of joblib cache

### 4.3 Maintenance

**Weekly:**
- Check Render logs for errors
- Monitor API response times
- Test critical user flows

**Monthly:**
- Review analytics in Vercel and Render
- Check for dependency updates
- Review error reports

---

## Part 5: Troubleshooting

### Frontend Issues

| Issue | Solution |
|-------|----------|
| **CORS Error** | Update backend CORS allowed origins to include Vercel URL |
| **API calls fail** | Verify `VITE_API_URL` environment variable is set correctly |
| **Build fails on Vercel** | Check build output in Vercel logs; ensure `npm install` succeeds |
| **Blank page** | Open DevTools console; check for JavaScript errors |

### Backend Issues

| Issue | Solution |
|-------|----------|
| **Service won't start** | Check Python version, dependencies in logs |
| **Out of memory** | Render Starter has 512MB; consider upgrading instance |
| **API timeouts** | Optimize query performance, increase timeout in FastAPI |
| **FAISS initialization fails** | Precompute vector embeddings; include in repo or cache |

### Network Issues

| Issue | Solution |
|-------|----------|
| **Frontend can't reach backend** | Verify CORS headers in response |
| **Slow responses** | Check Render logs for performance bottlenecks |
| **Connection refused** | Ensure Render backend is running (check Health endpoint) |

---

## Part 6: Advanced Configuration

### 6.1 Custom Domain (Optional)

**Vercel:**
1. **Settings → Domains**
2. Add your custom domain
3. Update DNS records to point to Vercel

**Render:**
1. **Settings → Custom Domain**
2. Add your custom domain
3. Update DNS records

### 6.2 SSL/TLS

Both Vercel and Render provide **free HTTPS** automatically.

### 6.3 Database (If Upgrading)

For production-grade persistence:

**Option 1: Render PostgreSQL**
```bash
# Create PostgreSQL instance on Render
# Connect from backend using SQLAlchemy
```

**Option 2: MongoDB Atlas**
```bash
# Cloud MongoDB
# Store predictions, user preferences, logs
```

### 6.4 Caching Layer

**Redis on Render:**
1. Create Redis instance on Render
2. Cache model predictions for frequently queried timeframes
3. Reduces latency from minutes to milliseconds

---

## Summary Checklist

### Frontend (Vercel)
- [ ] Code pushed to GitHub
- [ ] `npm install` works locally
- [ ] `npm run build` produces `dist/` folder
- [ ] `.env.production` configured with backend URL
- [ ] Vercel project created and linked
- [ ] `VITE_API_URL` environment variable set
- [ ] Deploy succeeds without errors
- [ ] Vercel URL accessible and functional

### Backend (Render)
- [ ] Code pushed to GitHub
- [ ] `requirements.txt` complete and tested
- [ ] `main.py` configured as entry point
- [ ] Environment variables set in Render (API keys, URLs)
- [ ] Health check endpoint responds
- [ ] CORS configured for Vercel frontend URL
- [ ] Render deployment succeeds
- [ ] API endpoints respond with correct data

### Integration
- [ ] Frontend environment variable updated with backend URL
- [ ] Frontend API calls reach backend successfully
- [ ] Full user workflows function end-to-end
- [ ] Error handling works gracefully
- [ ] Monitoring/logging enabled on both platforms

---

## Useful Commands

### Frontend
```bash
# Local development
cd End_sem/frontend && npm run dev

# Production build
npm run build

# Test build
npm run preview

# Linting
npm run lint
```

### Backend
```bash
# Local development
cd End_sem/backend && uvicorn main:app --reload

# Production (Render)
uvicorn main:app --host 0.0.0.0 --port 8000

# Install dependencies
pip install -r requirements.txt
```

### Deployment URLs (After Deployment)
```
Frontend: https://your-project.vercel.app
Backend: https://genai-ev-backend.onrender.com
API Base: https://genai-ev-backend.onrender.com/api
```

---

## Support & Resources

- **Vercel Docs:** https://vercel.com/docs
- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Vite Docs:** https://vitejs.dev
- **React Docs:** https://react.dev

---

**Document Version:** 1.0  
**Last Updated:** April 2026  
**Status:** Ready for Production Deployment
