"""
Setup configuration for DecAI Oracle
"""

from setuptools import setup, find_packages

setup(
    name="decai-oracle",
    version="0.1.0",
    description="Decentralized AI Oracle System",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pycoingecko==3.1.0",
        "web3",
        "eth-account==0.11.0",
        "python-dotenv==1.0.0",
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "pydantic",
        "pydantic-settings",
        "scikit-learn",
        "torch",
        "numpy",
        "pandas",
        "matplotlib==3.8.2",
        "seaborn==0.13.1",
        "ipfshttpclient==0.8.0a2",
        "requests==2.31.0",
        "pytest==7.4.4",
        "pytest-asyncio==0.23.3",
        "pytest-cov==4.1.0",
        "httpx==0.26.0",
        "python-json-logger==2.0.7",
        "sentry-sdk==1.39.2",
        "redis==5.0.1",
        "celery==5.3.4",
    ],
)
