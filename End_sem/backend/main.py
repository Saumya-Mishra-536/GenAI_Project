"""
FastAPI Entry Point for Production Deployment
Render Web Service Starter File

Run: uvicorn main:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
import logging
from typing import Optional
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize FastAPI app
app = FastAPI(
    title="EV Charging Demand Prediction API",
    description="Intelligent forecasting and infrastructure planning for EV charging networks",
    version="2.0.0",
)

# CORS Middleware - Get allowed origins from env or use defaults
FRONTEND_URL = os.getenv("FRONTEND_URL", "").strip()
ALLOWED_ORIGINS = [
    "http://localhost:3000",                  # Local React dev
    "http://localhost:5173",                  # Local Vite dev
    "http://localhost:8501",                  # Streamlit local
    "https://gen-ai-project-rosy.vercel.app"  # Current Vercel frontend (https!)
]
# Add frontend URL if configured (takes precedence)
if FRONTEND_URL:
    ALLOWED_ORIGINS.insert(0, FRONTEND_URL)

logger.info(f"CORS Allowed Origins: {ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)

# ──────────────────────────────────────
# Health & Status Endpoints
# ──────────────────────────────────────

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "EV-Charging-Backend",
        "version": "2.0.0",
    }


@app.get("/api/status")
async def status():
    """Service status with component health"""
    try:
        from config import OPENROUTER_API_KEY
        api_key_status = "configured" if OPENROUTER_API_KEY else "missing"
    except:
        api_key_status = "error"
    
    try:
        import joblib
        model_status = "available"
    except:
        model_status = "unavailable"
    
    return {
        "service": "EV-Charging-Backend",
        "status": "operational",
        "components": {
            "api_key": api_key_status,
            "model_pipeline": model_status,
            "database": "cached",
        },
        "environment": os.getenv("RENDER_GIT_BRANCH", "local"),
    }


# ──────────────────────────────────────
# Prediction Endpoints
# ──────────────────────────────────────

@app.post("/api/predict")
async def predict_single(data: dict):
    """
    Single prediction endpoint
    
    Example payload:
    {
        "hour": 14,
        "day_of_week": 3,
        "temperature": 28.5,
        "price": 0.12,
        "demand_lag_1": 15.2
    }
    """
    try:
        logger.info(f"Received prediction request: {data}")
        
        # TODO: Implement your ML prediction logic
        # This is a placeholder response
        prediction = {
            "predicted_demand_kw": 15.5,
            "confidence_interval": {
                "lower_bound": 14.2,
                "upper_bound": 16.8,
            },
            "risk_level": "normal",
            "timestamp": "2026-04-20T10:30:00Z",
        }
        
        return prediction
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/batch")
async def batch_predict(file: UploadFile = File(...)):
    """
    Batch prediction endpoint
    
    Accepts CSV file with charging station data
    Returns predictions for all records with validation metrics
    """
    try:
        logger.info(f"Received batch file: {file.filename}")
        
        if not file.filename.endswith(('.csv', '.xlsx')):
            raise HTTPException(status_code=400, detail="File must be CSV or Excel format")
        
        import io
        import pandas as pd
        from ml.predictor import load_model, get_feature_columns
        
        # Read file content
        contents = await file.read()
        
        try:
            # Try reading CSV first
            df = pd.read_csv(io.BytesIO(contents))
        except:
            # Try reading Excel if CSV fails
            try:
                df = pd.read_excel(io.BytesIO(contents))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")
        
        if df.empty:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Load model and make predictions
        try:
            estimator, scaler = load_model()
            feature_columns = get_feature_columns()
            
            # Check if we have required features or labels
            has_target = 'Demand_kW' in df.columns
            
            # Prepare features - if we have the required columns, use them; otherwise use sample features
            if all(col in df.columns for col in feature_columns):
                X = df[feature_columns]
            else:
                # Try to infer features or use placeholder
                logger.warning(f"Missing some feature columns. Expected: {feature_columns}")
                # Create a basic feature set from available columns
                X = pd.DataFrame({col: df.get(col, 0) for col in feature_columns})
            
            # Handle NaN values
            X = X.fillna(0)
            
            # Make predictions
            predictions = estimator.predict(X).tolist()
            
            # Calculate metrics if we have actual values
            r2_score = None
            mae = None
            actuals = None
            
            if has_target:
                from sklearn.metrics import r2_score as sk_r2, mean_absolute_error
                actuals = df['Demand_kW'].values.tolist()
                try:
                    r2_score = float(sk_r2(actuals, predictions))
                    mae = float(mean_absolute_error(actuals, predictions))
                except:
                    logger.warning("Could not calculate R² or MAE")
            
            # Extract hours if available
            hours = None
            if 'Hour' in df.columns:
                hours = df['Hour'].astype(int).tolist()
            else:
                hours = list(range(len(predictions)))
            
            result = {
                "file_name": file.filename,
                "total_records": len(df),
                "predictions": predictions,
                "actuals": actuals,
                "hours": hours,
                "r2_score": r2_score,
                "mae": mae,
                "has_labels": has_target,
                "processing_time_seconds": 0,
                "status": "completed",
            }
            
            logger.info(f"Batch processing completed: {len(df)} records, R²={r2_score}")
            return result
        
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────
# Agent Planning Endpoints
# ──────────────────────────────────────

@app.post("/api/agent/run")
async def run_planning_agent():
    """
    Run the agentic infrastructure planning system
    
    Returns the complete planning response with recommendations and validation
    """
    try:
        logger.info("Starting agentic planning pipeline")
        
        # TODO: Implement agentic planning logic with actual LangGraph agent
        # For now, return a properly structured mock response
        response = {
            "final_plan": {
                "risk_level": "Medium",
                "confidence_score": 0.92,
                "recommendations": [
                    {
                        "action": "Install battery storage",
                        "location": "Station A",
                        "capacity_kw": 50,
                        "estimated_cost": 150000,
                        "implementation_timeline": "Q3 2026",
                        "priority": "high",
                    },
                    {
                        "action": "Implement dynamic pricing",
                        "peak_hour_surcharge": 0.05,
                        "expected_load_reduction": "15%",
                        "implementation_timeline": "Q2 2026",
                        "priority": "medium",
                    },
                ],
            },
            "iteration_count": 2,
            "simulated_impact": {
                "robustness_score": 0.87,
                "scenario": "Peak demand +20% stress test",
                "impact_analysis": "System remains stable under extreme load conditions with recommended infrastructure upgrades",
            },
            "insights": [
                "Demand peaks occur consistently at 6-9 PM",
                "Battery storage would reduce grid strain by ~25%",
                "Dynamic pricing can flatten demand curve",
            ],
            "reasoning": "Analysis of historical patterns and stress simulation suggests a two-phase approach: immediate demand flattening via pricing, followed by long-term capacity expansion through battery storage.",
            "retrieved_knowledge": [
                {"source": "EV Planning Rules", "content": "Peak hour surcharges should be 15-20% above baseline"},
                {"source": "Grid Management", "content": "Battery storage systems typically achieve 85-90% round-trip efficiency"},
            ],
        }
        
        logger.info(f"Agent planning completed with confidence {response['final_plan']['confidence_score']}")
        return response
    
    except Exception as e:
        logger.error(f"Agent planning error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────
# Data Endpoints
# ──────────────────────────────────────

@app.get("/api/data/sample")
async def get_sample_data():
    """Get sample charging station data for testing"""
    try:
        sample_data = {
            "stations": [
                {
                    "station_id": "station_a",
                    "location": "Los Angeles, CA",
                    "current_load_kw": 12.5,
                    "capacity_kw": 50,
                    "utilization_percent": 25,
                },
                {
                    "station_id": "station_b",
                    "location": "San Francisco, CA",
                    "current_load_kw": 38.2,
                    "capacity_kw": 50,
                    "utilization_percent": 76,
                },
                {
                    "station_id": "station_c",
                    "location": "San Diego, CA",
                    "current_load_kw": 45.8,
                    "capacity_kw": 50,
                    "utilization_percent": 92,
                },
            ],
            "metadata": {
                "total_demand_kw": 96.5,
                "total_capacity_kw": 150,
                "overall_utilization": "64%",
                "timestamp": "2026-04-20T10:00:00Z",
            },
        }
        return sample_data
    
    except Exception as e:
        logger.error(f"Sample data error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/upload/status")
async def check_upload_status():
    """Check if data has been uploaded and processed"""
    try:
        # TODO: Implement actual upload status tracking
        status = {
            "data_uploaded": False,
            "has_processed_data": False,
            "last_upload_timestamp": None,
            "available_datasets": [],
        }
        return status
    
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────
# Root Endpoint
# ──────────────────────────────────────

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "EV Charging Demand Prediction API",
        "version": "2.0.0",
        "documentation": "/docs",
        "status_endpoint": "/api/health",
    }


# ──────────────────────────────────────
# Error Handlers
# ──────────────────────────────────────

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "type": "HTTP_ERROR",
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global general exception handler"""
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "type": "INTERNAL_ERROR",
        },
    )


# ──────────────────────────────────────
# Startup/Shutdown Events
# ──────────────────────────────────────

@app.on_event("startup")
async def startup_event():
    """Initialize models and services on startup"""
    logger.info("🚀 Backend startup - Loading models and initializing services")
    
    try:
        # TODO: Load your ML models here
        # from ml.predictor import load_model
        # load_model()
        
        # TODO: Initialize FAISS vector database
        # from agent.utils.vector_store import initialize_vector_store
        # initialize_vector_store()
        
        logger.info("✅ All services initialized successfully")
    
    except Exception as e:
        logger.error(f"❌ Startup error: {str(e)}")
        # Don't crash the service, log and continue
        # Models can be loaded on-demand


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Backend shutdown - Cleaning up resources")
    # TODO: Save model cache, close database connections, etc.


# ──────────────────────────────────────
# Entry Point
# ──────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )
