# Quick Start Guide - Local Development & Deployment

## 🚀 Run Locally Before Deploying

Before deploying to Vercel and Render, test everything locally to ensure it works correctly.

---

## Part 1: Setup Local Environment

### 1.1 Clone & Setup Project

```bash
# Clone repository
git clone https://github.com/CosmicMagnetar/GenAI_Project.git
cd GenAI_Project

# Create .env file
cp .env.example .env

# Edit .env with your values
nano .env  # or use your editor

# Required values:
# OPENROUTER_API_KEY=sk-or-v1-...
# VITE_API_URL=http://localhost:8000/api
```

### 1.2 Install Python & Node.js

```bash
# Check Python version (3.8+)
python --version

# Check Node.js version (18+)
node --version
npm --version
```

---

## Part 2: Run Backend Locally

### 2.1 Install Backend Dependencies

```bash
cd End_sem/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Run FastAPI Backend

```bash
# From End_sem/backend/ directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 2.3 Test Backend Health

In another terminal:

```bash
# Health check
curl http://localhost:8000/api/health

# Expected response:
# {"status":"healthy","service":"EV-Charging-Backend","version":"2.0.0"}
```

**FastAPI Documentation Available at:**
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Part 3: Run Frontend Locally

### 3.1 Install Frontend Dependencies

```bash
cd End_sem/frontend

# Verify index.html exists (CRITICAL for Vite)
ls -la index.html  # Should show the file exists

# Install Node dependencies
npm install
```

**⚠️ IMPORTANT:** If `index.html` is missing, see [VERCEL_BUILD_FIX.md](../VERCEL_BUILD_FIX.md)

### 3.2 Run Vite Dev Server

```bash
# Start development server
npm run dev
```

**Expected output:**
```
  VITE v5.4.21  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### 3.3 Open in Browser

Open browser and navigate to:
```
http://localhost:5173
```

You should see the EV Charging Dashboard landing page.

---

## Part 4: Test Full Integration

### 4.1 Make API Call from Frontend

1. Open browser → http://localhost:5173
2. Open DevTools (F12) → **Console** tab
3. Test API connectivity:

```javascript
// In browser console
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(data => console.log(data))
```

**Expected output:**
```
{status: 'healthy', service: 'EV-Charging-Backend', version: '2.0.0'}
```

### 4.2 Test Data Endpoints

```bash
# Get sample data
curl http://localhost:8000/api/data/sample

# Check upload status
curl http://localhost:8000/api/upload/status

# Make prediction
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"hour": 14, "day_of_week": 3, "temperature": 28.5}'
```

### 4.3 Test Frontend Pages

Navigate through pages and verify each works:
- ✅ Landing page loads
- ✅ Dashboard displays data
- ✅ Prediction page works
- ✅ Batch processing page accessible
- ✅ Agent Planner page functional

---

## Part 5: Build Frontend for Production

### 5.1 Create Production Build

```bash
cd End_sem/frontend

# Build optimized production bundle
npm run build

# Expected output:
# ✓ built in 5.23s
# dist/index.html                     0.46 kB │ gzip:  0.28 kB
# dist/assets/index-xxxxx.js       150.23 kB │ gzip: 45.32 kB
```

### 5.2 Test Production Build Locally

```bash
# Preview production build
npm run preview

# Open http://localhost:4173
```

---

## Part 6: Deploy to Vercel (Frontend)

### 6.1 Install Vercel CLI

```bash
npm install -g vercel
vercel login
```

### 6.2 Deploy Frontend

```bash
cd End_sem/frontend
vercel --prod
```

**Follow prompts:**
- Project name: `genai-ev-frontend`
- Framework: `Vite`
- Build: `npm run build`
- Install: `npm install`
- Output: `dist`

### 6.3 Set Environment Variables on Vercel

After deployment, update environment:

```bash
vercel env add VITE_API_URL
# Enter: https://genai-ev-backend.onrender.com/api

vercel redeploy --prod
```

---

## Part 7: Deploy to Render (Backend)

### 7.1 Prepare Repository

```bash
# Ensure all files committed
git add -A
git commit -m "Ready for Render deployment"
git push origin main
```

### 7.2 Create Render Service

1. Go to [render.com/dashboard](https://dashboard.render.com)
2. Click **New → Web Service**
3. Connect GitHub repository
4. Configure:

| Setting | Value |
|---------|-------|
| Name | `genai-ev-backend` |
| Build Command | `pip install -r End_sem/backend/requirements.txt` |
| Start Command | `cd End_sem/backend && uvicorn main:app --host 0.0.0.0 --port 8000` |

### 7.3 Add Environment Variables

Set in Render dashboard:

```
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=nvidia/nemotron-3-super-120b-a12b:free
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
PYTHONUNBUFFERED=1
```

### 7.4 Deploy

Click **Create Web Service** and wait for deployment.

Your backend URL will be: `https://genai-ev-backend.onrender.com`

---

## Part 8: Final Integration & Testing

### 8.1 Connect Frontend to Production Backend

1. Go to Vercel dashboard
2. **Settings → Environment Variables**
3. Update:
   ```
   VITE_API_URL=https://genai-ev-backend.onrender.com/api
   ```
4. Trigger redeploy

### 8.2 Test End-to-End

```bash
# Test backend health
curl https://genai-ev-backend.onrender.com/api/health

# Test frontend loads
# Visit https://your-frontend.vercel.app
```

### 8.3 Verify Features

- [ ] Frontend loads
- [ ] Navigation works
- [ ] API calls successful
- [ ] Dashboard displays data
- [ ] Predictions generate correctly
- [ ] Agent planner responds

---

## Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.8+

# Check all dependencies installed
pip list | grep -E "fastapi|uvicorn"

# Try with verbose logging
uvicorn main:app --reload --log-level=debug
```

### Frontend shows blank page

1. Open DevTools (F12)
2. Check **Console** tab for errors
3. Verify API URL in **Network** tab
4. Check `VITE_API_URL` environment variable

### API calls fail with CORS error

**Add your URL to CORS allowed origins in `main.py`:**

```python
allow_origins=[
    "https://your-frontend.vercel.app",  # Add your Vercel URL
    "http://localhost:5173",
]
```

### Models fail to load on Render

- Ensure all model files are in repository
- Check Render logs for import errors
- Verify required Python packages in `requirements.txt`

---

## Local Development Workflow

### Terminal 1: Backend
```bash
cd End_sem/backend
source venv/bin/activate
uvicorn main:app --reload
```

### Terminal 2: Frontend
```bash
cd End_sem/frontend
npm run dev
```

### Terminal 3: Testing
```bash
# Run your tests or curl commands here
```

---

## Environment Variables Reference

### Development (.env)
```bash
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=nvidia/nemotron-3-super-120b-a12b:free
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
VITE_API_URL=http://localhost:8000/api
```

### Production (Vercel)
```bash
VITE_API_URL=https://genai-ev-backend.onrender.com/api
```

### Production (Render)
```bash
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=nvidia/nemotron-3-super-120b-a12b:free
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
PYTHONUNBUFFERED=1
```

---

## Useful Commands Summary

### Frontend Commands
```bash
npm install              # Install dependencies
npm run dev             # Start dev server
npm run build           # Build for production
npm run preview         # Test production build
npm run lint            # Check code quality
```

### Backend Commands
```bash
pip install -r requirements.txt  # Install dependencies
uvicorn main:app --reload         # Start dev server
python -m pytest                  # Run tests
pip freeze > requirements.txt      # Update dependencies
```

### Git Commands
```bash
git status              # Check changes
git add -A              # Stage all changes
git commit -m "message" # Commit changes
git push origin main    # Push to GitHub
```

---

## Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Vite Docs**: https://vitejs.dev
- **React Docs**: https://react.dev

---

**Document Version:** 1.0  
**Last Updated:** April 2026  
**Ready for Production:** ✅
