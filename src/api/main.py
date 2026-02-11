"""
DecAI Oracle API V2 - FastAPI implementation
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import time
from datetime import datetime

from src.api.middleware import limiter, cache_response, remote_api_retry
from src.monitoring.metrics import metrics_endpoint, MetricsManager
from src.utils.logger import setup_logger
from src.utils.config import settings
from src.ml.predictor import Predictor
from src.ml.data_collector import DataCollector
from src.blockchain.contract_manager import ContractManager

logger = setup_logger(__name__)

app = FastAPI(
    title="DecAI Oracle API",
    description="Decentralized AI-Powered Oracle API with Verifiable Predictions",
    version="2.0.0",
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redoc"
)

# Initialize Limiter for FastAPI
app.state.limiter = limiter

# Models
class PredictionRequest(BaseModel):
    asset_id: str = "bitcoin"
    days_back: int = 30
    horizon_hours: int = 24

class PredictionResponse(BaseModel):
    asset_id: str
    predicted_price: float
    confidence: float
    timestamp: str
    model_version: str = "v2.0"

class HealthStatus(BaseModel):
    status: str
    timestamp: str
    blockchain_connected: bool
    version: str

# Endpoints
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to DecAI Oracle API V2", "docs": "/api/v2/docs"}

@app.get("/metrics")
async def get_metrics():
    """Exposes Prometheus metrics"""
    return metrics_endpoint()

@app.get("/api/v2/health", response_model=HealthStatus)
@limiter.limit("60/minute")
async def health_check(request: Request):
    try:
        cm = ContractManager()
        is_connected = cm.w3.is_connected()
    except:
        is_connected = False
        
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "blockchain_connected": is_connected,
        "version": "2.0.0"
    }

@app.post("/api/v2/predict", response_model=PredictionResponse)
@limiter.limit("10/minute")
@cache_response(ttl=300)
async def get_prediction(request: Request, params: PredictionRequest):
    """
    Generates a price prediction using current ML Engine
    """
    logger.info(f"🔮 Received prediction request for {params.asset_id}")
    
    with MetricsManager.track_prediction(params.asset_id):
        try:
            # Collect data
            collector = DataCollector()
            prices = await collector.fetch_asset_data(params.asset_id, days=params.days_back)
            
            # Train and Predict
            predictor = Predictor()
            predictor.train(prices)
            
            predicted_price = predictor.predict_next_day()
            confidence = predictor.get_confidence()
            
            return {
                "asset_id": params.asset_id,
                "predicted_price": predicted_price,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat(),
                "model_version": "v2.0-linear"
            }
        except Exception as e:
            logger.error(f"❌ Prediction failed: {e}")
            MetricsManager.log_error(params.asset_id, type(e).__name__)
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/stats/{predictor_address}")
@limiter.limit("20/minute")
async def get_predictor_stats(request: Request, predictor_address: str):
    """
    Retrieves accuracy statistics for a specific predictor
    """
    try:
        cm = ContractManager()
        # This would call the contract to get prediction count, verified status, etc.
        # Minimalist implementation for now
        total = cm.contract.functions.predictionCount().call()
        return {
            "address": predictor_address,
            "total_predictions_global": total,
            "status": "active"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
