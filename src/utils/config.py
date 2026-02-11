"""
Configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Environment
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Blockchain
    INFURA_API_KEY: Optional[str] = Field(default=None, env="INFURA_API_KEY")
    SEPOLIA_RPC_URL: Optional[str] = Field(default=None, env="SEPOLIA_RPC_URL")
    PRIVATE_KEY: Optional[str] = Field(default=None, env="PRIVATE_KEY")
    BLOCKCHAIN_ENABLED: bool = Field(default=False)
    
    # Contract Addresses
    PREDICTION_ORACLE_ADDRESS: Optional[str] = Field(default=None, env="PREDICTION_ORACLE_ADDRESS")
    
    # Data APIs
    COINGECKO_API_KEY: Optional[str] = Field(default=None, env="COINGECKO_API_KEY")
    COINGECKO_BASE_URL: str = Field(
        default="https://api.coingecko.com/api/v3",
        env="COINGECKO_BASE_URL"
    )
    
    # IPFS
    PINATA_JWT: Optional[str] = Field(default=None, env="PINATA_JWT")
    IPFS_ENABLED: bool = Field(default=False)
    
    # ML Settings
    MODEL_UPDATE_INTERVAL: int = Field(default=3600, env="MODEL_UPDATE_INTERVAL")
    PREDICTION_CONFIDENCE_THRESHOLD: float = Field(default=0.7, env="PREDICTION_CONFIDENCE_THRESHOLD")
    SUPPORTED_ASSETS: str = Field(default="BTC,ETH,SOL", env="SUPPORTED_ASSETS")
    
    # API Settings
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
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
