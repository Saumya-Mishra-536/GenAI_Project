# Deployment Checklist

## Pre-Deployment Verification

### 1. Code Quality & Testing

- [ ] Frontend code runs locally without errors
  ```bash
  cd End_sem/frontend && npm install && npm run dev
  ```

- [ ] Backend code runs locally without errors
  ```bash
  cd End_sem/backend && pip install -r requirements.txt && uvicorn main:app --reload
  ```

- [ ] All dependencies listed in `requirements.txt` (backend)

- [ ] All dependencies listed in `package.json` (frontend)

- [ ] No hardcoded API keys or secrets in code

- [ ] Environment variables documented in `.env.example`

- [ ] Code linting passes
  ```bash
  npm run lint  # Frontend
  ```

### 2. Frontend Checklist

#### Configuration
- [ ] `vite.config.js` properly configured
- [ ] `package.json` contains all dependencies
- [ ] Build succeeds locally: `npm run build`
- [ ] `.env.production` file created with `VITE_API_URL`
- [ ] No references to `localhost` in production code

#### Functionality
- [ ] Landing page loads
- [ ] Navigation between pages works
- [ ] Forms submit correctly
- [ ] Charts/visualizations render properly
- [ ] Responsive design works on mobile (test with DevTools)
- [ ] All images/assets load correctly

#### Browser Compatibility
- [ ] Chrome ✅
- [ ] Firefox ✅
- [ ] Safari ✅
- [ ] Edge ✅

#### Performance
- [ ] Build size is reasonable (< 500KB gzipped)
- [ ] Page loads in < 3 seconds
- [ ] No console errors in DevTools

### 3. Backend Checklist

#### Configuration
- [ ] `main.py` configured as entry point
- [ ] `requirements.txt` complete and tested
- [ ] `.env.example` documents all variables
- [ ] CORS settings updated for production URLs
- [ ] API responds on `/api/health` endpoint

#### API Endpoints
- [ ] `GET /api/health` returns success
- [ ] `GET /api/status` returns component status
- [ ] `POST /api/predict` accepts and processes data
- [ ] `POST /api/batch` handles file uploads
- [ ] `POST /api/agent/run` initiates planning
- [ ] `GET /api/data/sample` returns sample data
- [ ] `GET /api/upload/status` works correctly

#### Error Handling
- [ ] All endpoints have try-catch blocks
- [ ] Error responses include meaningful messages
- [ ] Logging is configured
- [ ] No stack traces exposed to users

#### Security
- [ ] No hardcoded secrets in code
- [ ] API key validated on startup
- [ ] CORS properly configured
- [ ] Input validation implemented
- [ ] Rate limiting considered (if needed)

### 4. Database & Cache

- [ ] FAISS vector database initializes correctly
- [ ] Model files are serialized and cached
- [ ] Cache invalidation strategy documented
- [ ] No data corruption on restart

### 5. Documentation

- [ ] README.md is complete
- [ ] ARCHITECTURE_WALKTHROUGH.md is comprehensive
- [ ] DEPLOYMENT_GUIDE.md is accurate
- [ ] QUICKSTART.md covers local setup
- [ ] API documentation in code (docstrings)

### 6. Git & Version Control

- [ ] All changes committed
  ```bash
  git status  # Should show clean working directory
  ```

- [ ] `.gitignore` prevents committing secrets
  - [ ] `.env` is in `.gitignore`
  - [ ] `__pycache__/` is in `.gitignore`
  - [ ] `node_modules/` is in `.gitignore`
  - [ ] `.venv/` / `venv/` is in `.gitignore`

- [ ] Repository is on GitHub and accessible
  ```bash
  git remote -v  # Should show GitHub URL
  ```

- [ ] Latest changes pushed to main branch
  ```bash
  git log --oneline -5
  ```

---

## Vercel Frontend Deployment

### Account Setup
- [ ] Vercel account created
- [ ] GitHub connected to Vercel
- [ ] Access to repository confirmed

### Pre-Deployment
- [ ] Frontend builds locally: `npm run build`
- [ ] `VITE_API_URL` in `.env.production`
- [ ] Backend URL determined (from Render deployment)

### Deployment Steps
- [ ] Vercel CLI installed: `npm install -g vercel`
- [ ] Logged into Vercel: `vercel login`
- [ ] Project deployed: `vercel --prod`
- [ ] Deployment succeeded (check Vercel logs)

### Post-Deployment
- [ ] Vercel URL accessible in browser
- [ ] Environment variables set in Vercel dashboard
  - [ ] `VITE_API_URL` points to Render backend
- [ ] Redeployment triggered after env var changes
- [ ] Frontend loads without errors
- [ ] Check Network tab for API calls

### Monitoring
- [ ] Deployment recorded in Vercel Dashboard
- [ ] Build logs show no errors
- [ ] Function logs (if applicable) are accessible
- [ ] Analytics dashboard enabled

---

## Render Backend Deployment

### Account Setup
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Access to repository confirmed

### Pre-Deployment
- [ ] Backend runs locally: `uvicorn main:app --reload`
- [ ] `requirements.txt` is complete
- [ ] `.env` has all required API keys
- [ ] Health endpoint works: `curl http://localhost:8000/api/health`

### Deployment Steps
- [ ] Repository pushed to GitHub (latest code)
- [ ] New Web Service created on Render
- [ ] Build command configured:
  ```
  pip install -r End_sem/backend/requirements.txt
  ```
- [ ] Start command configured:
  ```
  cd End_sem/backend && uvicorn main:app --host 0.0.0.0 --port 8000
  ```
- [ ] Environment variables added:
  - [ ] `OPENROUTER_API_KEY`
  - [ ] `OPENROUTER_BASE_URL`
  - [ ] `MODEL_NAME`
  - [ ] `EMBEDDINGS_MODEL`
  - [ ] `PYTHONUNBUFFERED=1`
- [ ] Instance type selected (Starter is free tier)
- [ ] Service deployed (wait 5-10 minutes)

### Post-Deployment
- [ ] Backend URL obtained (e.g., `https://genai-ev-backend.onrender.com`)
- [ ] Health check succeeds:
  ```bash
  curl https://genai-ev-backend.onrender.com/api/health
  ```
- [ ] Status endpoint responds:
  ```bash
  curl https://genai-ev-backend.onrender.com/api/status
  ```
- [ ] Logs show no errors
- [ ] CORS properly configured for frontend URL

### Monitoring
- [ ] Render dashboard accessible
- [ ] Logs viewable and no errors
- [ ] Metrics show healthy service
- [ ] Auto-redeployment on push (if enabled)

---

## Integration Testing

### Frontend ↔ Backend Communication

- [ ] Frontend can reach backend:
  ```javascript
  // In browser console
  fetch('https://genai-ev-backend.onrender.com/api/health')
    .then(r => r.json())
    .then(console.log)
  ```

- [ ] API calls include correct headers
- [ ] CORS errors resolved
- [ ] JSON responses parsed correctly
- [ ] Error responses handled gracefully

### Full User Workflows

- [ ] User can load landing page
- [ ] User can navigate to dashboard
- [ ] User can view predictions
- [ ] User can upload data and process batch
- [ ] User can initiate agent planning
- [ ] User can view results

### Edge Cases

- [ ] Network timeout handled gracefully
- [ ] Invalid input rejected with error message
- [ ] Large file uploads handled (backend)
- [ ] Long-running requests don't timeout
- [ ] Refresh page doesn't break state

---

## Performance Verification

### Frontend
- [ ] Page load time < 3 seconds
- [ ] First Contentful Paint (FCP) < 2 seconds
- [ ] Largest Contentful Paint (LCP) < 2.5 seconds
- [ ] Cumulative Layout Shift (CLS) < 0.1
- [ ] Build size < 500KB (gzipped)

### Backend
- [ ] Health endpoint responds < 100ms
- [ ] Prediction request < 500ms
- [ ] Batch processing completes in reasonable time
- [ ] Memory usage stable (no leaks)
- [ ] Database queries optimized

### Network
- [ ] API requests complete successfully
- [ ] No timeout errors on reasonable loads
- [ ] Response compression enabled (gzip)
- [ ] Caching headers configured

---

## Security Verification

### Code Security
- [ ] No API keys in code
- [ ] No secrets in environment files (not committed)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (if using DB)
- [ ] XSS prevention in frontend

### Infrastructure Security
- [ ] HTTPS enabled (automatic on Vercel/Render)
- [ ] CORS restrictions in place
- [ ] Rate limiting configured (if needed)
- [ ] Backend logs don't expose sensitive data
- [ ] API key rotation plan documented

### Secrets Management
- [ ] Environment variables used instead of hardcoded values
- [ ] `.env` file in `.gitignore`
- [ ] API keys rotated from time to time
- [ ] No credentials in commit history
  ```bash
  git log -S "sk-or-v1" --all  # Search for keys in history
  ```

---

## Post-Deployment Monitoring

### Daily Checks (First Week)
- [ ] Check Vercel logs for errors
- [ ] Check Render logs for errors
- [ ] Verify API health endpoints
- [ ] Test critical user workflows
- [ ] Monitor error rates

### Weekly Checks
- [ ] Review analytics on both platforms
- [ ] Check for dependency updates
- [ ] Verify backup systems working
- [ ] Review error logs

### Monthly Checks
- [ ] Performance analysis
- [ ] Security audit
- [ ] Dependency updates
- [ ] Capacity planning (if needed)
- [ ] Cost review

---

## Troubleshooting Quick Reference

### Frontend won't load
```bash
# 1. Check Vercel build logs
# 2. Verify Node version: node --version (should be 18+)
# 3. Check environment variables in Vercel dashboard
# 4. Test locally: npm install && npm run build
```

### API calls fail
```bash
# 1. Verify VITE_API_URL environment variable
# 2. Check CORS in backend (main.py)
# 3. Verify backend is running: curl https://backend-url/api/health
# 4. Check browser console for specific error message
```

### Backend won't start
```bash
# 1. Check Render logs for Python errors
# 2. Verify all dependencies: pip install -r requirements.txt
# 3. Test locally: uvicorn main:app --reload
# 4. Check environment variables are set in Render
```

### Models fail to load
```bash
# 1. Verify model files are in repository
# 2. Check file permissions
# 3. Ensure joblib/scikit-learn versions match
# 4. Check logs for import errors
```

---

## Rollback Plan

If deployment fails:

### Frontend
```bash
# Revert to previous version
vercel rollback
# Or redeploy from specific commit
git checkout previous-commit
git push
```

### Backend
```bash
# Render allows rollback to previous deploy
# Go to Render dashboard → Service → Deployments
# Select previous successful deployment
# Click "Re-run"
```

---

## Sign-Off Checklist

Before declaring deployment complete:

- [ ] Project Owner has reviewed and approved
- [ ] All tests pass
- [ ] Documentation is up-to-date
- [ ] No known bugs or issues
- [ ] Performance is acceptable
- [ ] Security review completed
- [ ] Monitoring is in place
- [ ] Team is trained on deployment process
- [ ] Disaster recovery plan documented
- [ ] Support documentation is ready

---

## Contact & Support

**Issues with Vercel?**
- Vercel Support: https://vercel.com/support
- Vercel Docs: https://vercel.com/docs

**Issues with Render?**
- Render Support: https://support.render.com
- Render Docs: https://render.com/docs

**Issues with the Application?**
- Check DEPLOYMENT_GUIDE.md
- Check QUICKSTART.md
- Review application logs on both platforms

---

**Document Version:** 1.0  
**Last Updated:** April 2026  
**Status:** Ready for Production Deployment
