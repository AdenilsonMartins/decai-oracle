# CHANGELOG V2 - DecAI Oracle

## [2.0.0-phase1] - 2026-02-10

### Added
- `src/data/data_aggregator.py`: Multi-source data aggregator with fallback and consensus logic.
- `src/resilient_oracle.py`: Integration example for the resilient oracle system.
- `tests/test_e2e.py`: End-to-end test suite for blockchain and ML integration.
- `scripts/setup_v2.py`: Updated setup script for V2 environment.

### Changed
- `src/blockchain/contract_manager.py`: 
    - Upgraded to Version 2.0.
    - Added support for Web3 v7+ using `ExtraDataToPOAMiddleware` instead of deprecated `geth_poa_middleware`.
    - Improved artifact path resolution for `PredictionOracle` contract.
- `scripts/setup.py`: Fixed project root paths and imports for V2 structure.
- `docs/planning/v2/IMPLEMENTATION_STATUS.md`: Marked Phase 1 as completed.

### Infrastructure
- Validated Sepolia testnet connection.
- Verified wallet balance (~0.048 ETH).
- Environment prepared for Phase 2 (Resilient Architecture Integration).
