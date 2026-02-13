"""
Configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Changed to False for better compatibility
        extra="ignore"          # Allow extra fields in .env without failing
    )
    
    # Application Info
    APP_NAME: str = Field(default="DecAI Oracle Network")
    VERSION: str = Field(default="1.0.0")
    
    # Environment
    ENVIRONMENT: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")
    
    # Blockchain
    INFURA_API_KEY: Optional[str] = Field(default=None)
    SEPOLIA_RPC_URL: Optional[str] = Field(default=None)
    PRIVATE_KEY: Optional[str] = Field(default=None)
    BLOCKCHAIN_ENABLED: bool = Field(default=False)
    
    # Contract Addresses
    PREDICTION_ORACLE_ADDRESS: Optional[str] = Field(default=None)
    
    # Data APIs
    COINGECKO_API_KEY: Optional[str] = Field(default=None)
    COINGECKO_BASE_URL: str = Field(default="https://api.coingecko.com/api/v3")
    
    # Data Aggregation Settings (V2)
    MIN_SOURCES: int = Field(default=2)
    MAX_DEVIATION_PERCENT: float = Field(default=5.0)
    CACHE_TTL_SECONDS: int = Field(default=30)
    REQUEST_TIMEOUT_SECONDS: int = Field(default=5)
    
    # IPFS
    PINATA_JWT: Optional[str] = Field(default=None)
    IPFS_ENABLED: bool = Field(default=False)
    
    # ML Settings
    MODEL_UPDATE_INTERVAL: int = Field(default=3600)
    PREDICTION_CONFIDENCE_THRESHOLD: float = Field(default=0.7)
    SUPPORTED_ASSETS: str = Field(default="BTC,ETH,SOL")
    
    # API Settings
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    API_WORKERS: int = Field(default=4)
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None)
    ENABLE_METRICS: bool = Field(default=True)
    PROMETHEUS_PORT: int = Field(default=9090)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Enable blockchain if we have required credentials
        if self.SEPOLIA_RPC_URL and self.PRIVATE_KEY and self.PREDICTION_ORACLE_ADDRESS:
            self.BLOCKCHAIN_ENABLED = True
        # Enable IPFS if we have JWT
        if self.PINATA_JWT:
            self.IPFS_ENABLED = True


# Global settings instance
settings = Settings()
