"""
Integration tests for Blockchain interactions
Requires local Hardhat node running
"""

import pytest
import asyncio
from src.blockchain.contract_manager import ContractManager
from src.utils.config import settings

@pytest.mark.asyncio
async def test_contract_deployment():
    # Only run if blockchain is enabled
    if not settings.BLOCKCHAIN_ENABLED:
        pytest.skip("Blockchain integration disabled")
    
    manager = ContractManager()
    
    # Check connection
    assert manager.w3.is_connected()
    
    # Check balance (deployer account needs ETH)
    balance = manager.get_wallet_balance()
    assert balance > 0
    print(f"Test Account Balance: {balance:.4f} ETH")

@pytest.mark.asyncio
async def test_store_prediction():
    if not settings.BLOCKCHAIN_ENABLED:
        pytest.skip("Blockchain integration disabled")
    
    manager = ContractManager()
    
    # Store a prediction
    asset = "IntegrationTestCoin"
    price = 100.50
    confidence = 0.95
    
    # store_prediction is synchronous in ContractManager
    result = manager.store_prediction(asset, price, confidence)
    
    assert result['success'] is True
    tx_hash = result['tx_hash']
    
    assert tx_hash is not None
    assert isinstance(tx_hash, str)
    # Hex string length 64 chars + '0x' prefix?? 
    # web3.py .hex() usually returns '0x...' which is 66 chars
    # check length
    assert len(tx_hash) >= 64
    
    print(f"Integration Test Transaction: {tx_hash}")
