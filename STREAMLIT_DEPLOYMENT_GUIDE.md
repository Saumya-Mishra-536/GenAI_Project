# Streamlit Cloud Deployment Guide

## Local Testing

Run locally to test before deploying:

```bash
cd src
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Streamlit Cloud Deployment

### Step 1: Push to GitHub
Make sure your changes are pushed to GitHub:

```bash
git add src/
git commit -m "Fix Streamlit app for cloud deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select:
   - Repository: `CosmicMagnetar/GenAI_Project`
   - Branch: `main`
   - Main file path: `src/app.py`
5. Click **"Deploy"**

### Step 3: Configure Streamlit Cloud (Optional)

If you have secrets or environment variables:

1. Go to your app's "Settings" (gear icon)
2. Click "Secrets"
3. Add your secrets in TOML format:
   ```toml
   api_key = "your-key-here"
   ```

### Troubleshooting

**❌ "ModuleNotFoundError: No module named 'streamlit'"**
- ✅ Fixed: Added `src/requirements.txt` with all dependencies

**❌ "FileNotFoundError: models/ev_demand_timeseries.pkl"**
- ✅ Fixed: Updated model loading to try multiple paths and handle missing files gracefully

**❌ "FutureWarning: DataFrame.fillna with method is deprecated"**
- ✅ Fixed: Changed `fillna(method='bfill')` to `bfill()`

**❌ App runs locally but not on Streamlit Cloud**
- Make sure all required packages are in `src/requirements.txt`
- Check that relative paths work correctly
- Verify the model file is committed to git (or handled via download)

### File Structure for Streamlit Cloud

```
GenAI_Project/
├── src/
│   ├── app.py              ← Main Streamlit app
│   ├── utils.py            ← Helper functions
│   ├── requirements.txt     ← Dependencies ✅ NEW
│   ├── .streamlit/
│   │   └── config.toml     ← Config ✅ NEW
│   ├── .gitignore          ← Git ignore ✅ NEW
│   └── models/
│       └── ev_demand_timeseries.pkl
└── ... (other files)
```

### What Was Fixed

| Issue | Fix |
|-------|-----|
| Missing dependencies | Created `src/requirements.txt` with all packages |
| Hardcoded model path | Updated to try multiple paths with Path() |
| Deprecated pandas | Changed `.fillna(method='x')` to `.bfill()/.ffill()` |
| Missing Streamlit config | Created `.streamlit/config.toml` |
| Better error handling | Added warning instead of silent failure |

### Next Steps

1. Test locally: `streamlit run src/app.py`
2. Push to GitHub: `git push`
3. Deploy on Streamlit Cloud
4. Monitor the app logs for any issues

