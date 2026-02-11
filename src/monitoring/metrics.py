"""
Monitoring & Observability - Prometheus metrics collection
"""

import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Metrics definitions
PREDICTION_LATENCY = Histogram(
    'oracle_prediction_latency_seconds',
    'Latency of ML predictions',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

PREDICTION_ERRORS = Counter(
    'oracle_prediction_errors_total',
    'Total number of failed predictions',
    ['asset_id', 'error_type']
)

WALLET_BALANCE = Gauge(
    'oracle_wallet_balance_eth',
    'Current balance of the oracle wallet in ETH'
)

BLOCKCHAIN_STATUS = Gauge(
    'oracle_blockchain_connected',
    'Indicates if the oracle is connected to the blockchain (1=True, 0=False)'
)

ACTIVE_PREDICTORS = Gauge(
    'oracle_active_predictors_count',
    'Number of authorized predictors on-chain'
)

def metrics_endpoint():
    """Returns the latest metrics in Prometheus format"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

class MetricsManager:
    """Helper class to track operations"""
    
    @staticmethod
    def track_prediction(asset_id: str):
        return PREDICTION_LATENCY.time()

    @staticmethod
    def log_error(asset_id: str, error_type: str):
        PREDICTION_ERRORS.labels(asset_id=asset_id, error_type=error_type).inc()

    @staticmethod
    def update_wallet_balance(balance_eth: float):
        WALLET_BALANCE.set(balance_eth)

    @staticmethod
    def set_blockchain_status(connected: bool):
        BLOCKCHAIN_STATUS.set(1 if connected else 0)
