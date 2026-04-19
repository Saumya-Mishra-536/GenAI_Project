# CORS Error Fix Guide

## 🔴 The Problem

You're seeing these errors in the browser console:

```
Access to XMLHttpRequest at 'https://genai-project-rtsb.onrender.com/data/sample' 
from origin 'https://gen-ai-project-invhf5ifm-cosmicmagnetars-projects.vercel.app' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header 
is present on the requested resource.
```

**What this means:**
- Your **frontend** is at: `https://gen-ai-project-invhf5ifm-cosmicmagnetars-projects.vercel.app`
- Your **backend** is at: `https://genai-project-rtsb.onrender.com`
- Frontend tries to call backend → Backend says "No, I don't know you" → Browser blocks it

---

## 🔍 Root Cause

Your backend's CORS configuration had a **hardcoded Vercel URL** that doesn't match your actual Vercel deployment URL:

```python
# BEFORE (❌ Wrong)
allow_origins=[
    "https://genai-ev-frontend.vercel.app",  # This is not your actual URL!
    "http://localhost:3000",
    ...
]
```

But your actual Vercel URL is:
```
https://gen-ai-project-invhf5ifm-cosmicmagnetars-projects.vercel.app
```

These don't match → CORS blocks the request.

---

## 🟢 The Solution

### Step 1: Update Backend with FRONTEND_URL Environment Variable ✅

I've already updated `End_sem/backend/main.py` to use environment variables:

```python
# NOW (✅ Fixed)
FRONTEND_URL = os.getenv("FRONTEND_URL", "").strip()
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8501",
]
if FRONTEND_URL:
    ALLOWED_ORIGINS.insert(0, FRONTEND_URL)
```

This is **dynamic** - it reads from the `FRONTEND_URL` environment variable.

### Step 2: Set FRONTEND_URL on Render ⚠️ YOU MUST DO THIS

Go to your Render backend dashboard:

1. **Navigate to:** https://dashboard.render.com
2. **Click:** Your GenAI project (genai-project-rtsb)
3. **Click:** "Environment" tab
4. **Click:** "Add Environment Variable"
5. **Add this:**
   ```
   Key:   FRONTEND_URL
   Value: https://gen-ai-project-invhf5ifm-cosmicmagnetars-projects.vercel.app
   ```
6. **Click:** "Save"
7. **Wait:** Render automatically redeploys (2-3 minutes)

### Step 3: Verify Backend Redeployed ✅

1. Go to https://dashboard.render.com
2. Click your project
3. Watch the "Deploys" section
4. Wait for green "Deploy successful" message

### Step 4: Test CORS is Fixed ✅

Open your frontend in browser:
1. Go to: https://gen-ai-project-invhf5ifm-cosmicmagnetars-projects.vercel.app
2. Open DevTools: F12 → Console
3. **The error should be gone!** ✅

If you see different errors, scroll down to the troubleshooting section.

---

## 📋 Complete Setup Steps

### For Render Backend Environment Variables

Set these on Render dashboard (Settings → Environment):

```
OPENROUTER_API_KEY=your_api_key_here
FRONTEND_URL=https://gen-ai-project-invhf5ifm-cosmicmagnetars-projects.vercel.app
```

**Important:** Use your actual Vercel URL, not the example above!

### For Vercel Frontend Environment Variables

Set these on Vercel dashboard (Settings → Environment Variables):

```
VITE_API_URL=https://genai-project-rtsb.onrender.com/api
```

**Important:** Use your actual Render backend URL!

---

## 🔧 Testing CORS Locally

Before deploying, test locally:

### 1. Backend with Dynamic CORS

```bash
cd End_sem/backend

# Set the environment variable
export FRONTEND_URL=http://localhost:3000

# Run backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend Dev Server

```bash
cd End_sem/frontend

# Set backend URL
export VITE_API_URL=http://localhost:8000/api

# Run dev server
npm run dev
```

### 3. Test API Call

In browser console:
```javascript
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(console.log)
```

Should see:
```json
{
  "status": "healthy",
  "service": "EV-Charging-Backend",
  "version": "2.0.0"
}
```

---

## 📊 CORS Configuration Summary

### What Changed

| Aspect | Before ❌ | After ✅ |
|--------|-----------|---------|
| Frontend URL | Hardcoded | Environment variable |
| Flexibility | Fixed URL only | Any deployment URL |
| Production Ready | No | Yes |
| Easy to Deploy | No | Yes |

### How It Works Now

```
Your Vercel Frontend
        ↓
Sets VITE_API_URL env var
        ↓
Calls API: /api/health
        ↓
Browser sends request to Render
        ↓
Render backend checks CORS
        ↓
Reads FRONTEND_URL env var
        ↓
Compares your URL to FRONTEND_URL
        ↓
✅ Match! Allows request
        ↓
Response sent back to frontend ✅
```

---

## 🚀 Quick Action Checklist

### RIGHT NOW (5 minutes)

```
[ ] 1. Go to https://dashboard.render.com
[ ] 2. Click your backend project
[ ] 3. Click "Environment" tab
[ ] 4. Click "Add Environment Variable"
[ ] 5. Add FRONTEND_URL = your Vercel URL
[ ] 6. Save and wait for redeploy
[ ] 7. Check Vercel dashboard for green status
[ ] 8. Reload frontend page (Ctrl+Shift+R)
[ ] 9. Check browser console (F12)
[ ] 10. Error should be gone! ✅
```

### Your URLs (for reference)

**Frontend (Vercel):**
```
https://gen-ai-project-invhf5ifm-cosmicmagnetars-projects.vercel.app
```

**Backend (Render):**
```
https://genai-project-rtsb.onrender.com
```

**Frontend should call:**
```
https://genai-project-rtsb.onrender.com/api/...
```

---

## 🧪 Testing Endpoints

Once CORS is fixed, these should work:

### Health Check
```bash
curl https://genai-project-rtsb.onrender.com/api/health
```

### Sample Data
```bash
curl https://genai-project-rtsb.onrender.com/api/data/sample
```

### Upload Status
```bash
curl https://genai-project-rtsb.onrender.com/api/upload/status
```

All should return JSON (not CORS error).

---

## ❌ Troubleshooting

### Still Getting CORS Error After 10 Minutes?

1. **Clear Render Cache**
   - Go to Render dashboard
   - Click "Manual Deploy" → "Clear Build Cache and Deploy"
   - Wait 5 minutes

2. **Verify Environment Variable Set**
   - Render Dashboard → Settings → Environment Variables
   - Check FRONTEND_URL is present and correct
   - Copy exact URL from Vercel

3. **Check Render Logs**
   - Render Dashboard → "Logs"
   - Look for: `CORS Allowed Origins: [...]`
   - Should show your Vercel URL
   - If not, variable didn't apply

4. **Hard Refresh Browser**
   - Frontend: Ctrl+Shift+R (or Cmd+Shift+R)
   - Clears browser cache

5. **Check Frontend Env Variable**
   - Vercel Dashboard → Settings → Environment
   - VITE_API_URL should be correct Render URL
   - If changed, redeployed? (Auto should happen)

### Backend Returns Different Error?

If you see a different error instead of CORS:

1. **400 Bad Request** → Check request format
2. **401 Unauthorized** → Check API key
3. **500 Server Error** → Check Render logs
4. **Timeout** → Backend might be slow/sleeping

### Frontend Shows "Network Error"

```
Failed to check upload status: AxiosError: Network Error
```

This usually means CORS or network issue:

1. Check CORS error in DevTools Network tab
2. Check if backend is running on Render
3. Verify FRONTEND_URL in Render environment

---

## 📚 Files Changed

| File | Change | Why |
|------|--------|-----|
| `End_sem/backend/main.py` | Uses FRONTEND_URL env var | Flexible CORS |
| `.env.example` | Added FRONTEND_URL | Documentation |
| This file | Created | Explains fix |

---

## ✅ Success Criteria

After completing these steps:

✅ No CORS errors in console  
✅ API calls return data (not errors)  
✅ Frontend can fetch from backend  
✅ Upload status checks work  
✅ Batch processing works  
✅ Agent planning works  

---

## 🎯 Next Steps After CORS Fixed

1. Test all API endpoints work
2. Deploy everything is synced
3. Check all frontend pages load
4. Verify features function (predictions, batch, etc.)
5. Monitor Render logs for errors

---

## 📞 Quick Reference

**Current Setup:**
- Frontend: `https://gen-ai-project-invhf5ifm-cosmicmagnetars-projects.vercel.app` (Vercel)
- Backend: `https://genai-project-rtsb.onrender.com` (Render)

**Environment Variables Needed:**

On Render:
```
FRONTEND_URL=https://gen-ai-project-invhf5ifm-cosmicmagnetars-projects.vercel.app
OPENROUTER_API_KEY=your_key
```

On Vercel:
```
VITE_API_URL=https://genai-project-rtsb.onrender.com/api
```

---

**Status:** 🟢 Backend updated  
**Action Required:** Set FRONTEND_URL on Render  
**Time to Fix:** 5 minutes  
**Expected Result:** CORS errors gone ✅
