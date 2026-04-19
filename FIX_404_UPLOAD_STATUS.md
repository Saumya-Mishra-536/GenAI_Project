# 404 Upload Status Error - Complete Fix Guide

## 🔴 The Problem

Your frontend is getting a **404 error** when calling the upload status endpoint:

```
GET https://genai-project-rtsb.onrender.com/upload/status 404 (Not Found)
```

But the endpoint exists at:
```
GET https://genai-project-rtsb.onrender.com/api/upload/status
```

**Root Cause:** The `VITE_API_URL` environment variable in Vercel is either:
- ❌ Not set
- ❌ Set to the backend URL **without `/api`** (e.g., `https://genai-project-rtsb.onrender.com` instead of `https://genai-project-rtsb.onrender.com/api`)

---

## ✅ Complete Fix (4 Steps)

### Step 1: Update Frontend Code ✅ (DONE)
I've updated the frontend to intelligently handle the API URL. The code now:
- Logs the API URL to console for debugging
- Ensures `/api` is always included in the path
- Prevents double `/api/api` issues

### Step 2: Set VITE_API_URL on Vercel (YOU MUST DO THIS)

Go to Vercel Dashboard:

1. **Navigate to:** https://vercel.com/dashboard
2. **Click:** Your GenAI frontend project
3. **Click:** Settings
4. **Click:** Environment Variables
5. **Check or Add:**
   ```
   Key:   VITE_API_URL
   Value: https://genai-project-rtsb.onrender.com/api
   ```
   
   ⚠️ **IMPORTANT:** Include `/api` at the end!

6. **Save**
7. **Trigger redeploy:**
   - Click "Deployments" tab
   - Click "Redeploy" on latest deployment
   - OR wait for automatic redeploy (if triggered)

### Step 3: Verify Environment Variable Set Correctly

After redeployment completes:

1. Open your frontend: `https://gen-ai-project-rosy.vercel.app`
2. Open DevTools: **F12 → Console**
3. Look for this message:
   ```
   [API Client] Using base URL: https://genai-project-rtsb.onrender.com/api
   ```
4. **Verify it includes `/api`!** ✅

### Step 4: Test the Endpoint

In browser console (F12):
```javascript
fetch('https://genai-project-rtsb.onrender.com/api/upload/status')
  .then(r => r.json())
  .then(console.log)
```

Should return:
```json
{
  "has_data": false,
  "message": "No upload data available"
}
```

**No 404 error = Success!** ✅

---

## 📋 Quick Environment Variable Reference

### Vercel Frontend
```
VITE_API_URL=https://genai-project-rtsb.onrender.com/api
```
**⚠️ MUST include `/api` at the end!**

### Render Backend  
```
FRONTEND_URL=https://gen-ai-project-rosy.vercel.app
OPENROUTER_API_KEY=your_key_here
```

---

## 🧪 Testing Before & After

### Before Fix (What You're Seeing Now)
```
Console Error:
GET https://genai-project-rtsb.onrender.com/upload/status 404

Reason:
API_URL = https://genai-project-rtsb.onrender.com (missing /api)
Path = /upload/status
Result = https://genai-project-rtsb.onrender.com/upload/status ❌
```

### After Fix (What You'll See)
```
Console Log:
[API Client] Using base URL: https://genai-project-rtsb.onrender.com/api

GET https://genai-project-rtsb.onrender.com/api/upload/status 200 OK

Reason:
API_URL = https://genai-project-rtsb.onrender.com/api (with /api)
Path = /upload/status  
Result = https://genai-project-rtsb.onrender.com/api/upload/status ✅
```

---

## 🔍 Debugging Checklist

If you still see 404 after following the steps:

### 1. Verify Environment Variable is Set
```
Vercel Dashboard → Project → Settings → Environment Variables
Look for: VITE_API_URL
Value should be: https://genai-project-rtsb.onrender.com/api (with /api!)
```

### 2. Force Redeploy Frontend
```
Vercel Dashboard → Deployments
Click "Redeploy" on latest deployment
Wait for green "Ready" status
```

### 3. Hard Refresh Browser
```
Frontend: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
Clear browser cache
```

### 4. Check Console for API URL
```
F12 → Console
Look for: [API Client] Using base URL: ...
If you see this without /api, the env var isn't set
```

### 5. Test Health Endpoint
```javascript
fetch('https://genai-project-rtsb.onrender.com/api/health')
  .then(r => r.json())
  .then(console.log)
```
Should return JSON (not 404)

### 6. Check Render Backend is Running
```
https://dashboard.render.com
Click your backend project
Should show "Running" status
```

---

## 📊 All Affected Endpoints

These endpoints should now work (after the fix):

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/status` | GET | Service status |
| `/api/predict` | POST | Single prediction |
| `/api/batch` | POST | Batch processing |
| `/api/agent/run` | POST | Agent planning |
| `/api/data/sample` | GET | Sample data |
| `/api/upload/status` | GET | Upload status |

All should be accessible at: `https://genai-project-rtsb.onrender.com/api/...`

---

## 🚀 Timeline

### Right Now (5 minutes)
```
[ ] 1. Go to Vercel Dashboard
[ ] 2. Navigate to Environment Variables
[ ] 3. Verify/Add VITE_API_URL with /api suffix
[ ] 4. Save and trigger redeploy
[ ] 5. Wait for green "Ready" status
```

### After Redeploy (5 minutes)
```
[ ] 6. Reload frontend page
[ ] 7. Open console (F12)
[ ] 8. Look for [API Client] Using base URL message
[ ] 9. Verify it has /api in the URL
[ ] 10. Try upload/batch/other features
```

---

## 💡 Key Takeaway

**The Frontend's API URL Must Match the Backend's API Base Path:**

```
Frontend Environment Variable:
VITE_API_URL = https://genai-project-rtsb.onrender.com/api
                                                     ^^^^
                                                  Don't forget!

Backend Endpoints:
@app.get("/api/upload/status") → Available at /api/upload/status
@app.get("/api/health")        → Available at /api/health
```

When the frontend calls `apiClient.get('/upload/status')`:
- Base URL + Path = Final URL
- `https://.../api` + `/upload/status` = `https://.../api/upload/status` ✅

---

## 📁 Files Changed

| File | Change | Why |
|------|--------|-----|
| `End_sem/frontend/src/api/client.js` | Added `/api` auto-detection | Prevents hardcoded URL issues |

---

## 🎯 Success Indicators

After completing these steps:

✅ Console shows: `[API Client] Using base URL: ...api`  
✅ No 404 errors in Network tab  
✅ Upload status endpoint returns data  
✅ All API calls succeed (200 status codes)  
✅ Upload/batch/predict features work  

---

## 📞 Quick Reference

**Your URLs:**
- Frontend: `https://gen-ai-project-rosy.vercel.app`
- Backend: `https://genai-project-rtsb.onrender.com`
- API Base: `https://genai-project-rtsb.onrender.com/api`

**Environment Variable to Set:**
```
VITE_API_URL=https://genai-project-rtsb.onrender.com/api
```

**Do NOT forget the `/api`!**

---

**Status:** 🟢 Frontend code fixed  
**Action Required:** Set VITE_API_URL on Vercel  
**Time to Fix:** 5 minutes  
**Expected Result:** 404 errors gone, all API calls work ✅
