# CHANGELOG V2 - DecAI Oracle

## [2.1.0-phase4] - 2026-02-11 (Cloud & Security Prep)

### Added
- **Dockerization**: `Dockerfile` and `docker-compose.yml` for production deployment.
- **Security**: `scripts/security_audit.py` for automated Slither/Mythril audits.
- **Testing**: `scripts/coverage_report.py` for automated pytest code coverage analysis.
- **Documentation**: New sections in `docs/DEPLOY_GUIDE.md` for Railway/Render/Docker.
- **Verification**: `docs/DEPLOYMENT_LOG.md` updated with V2 system verification results.

### Changed
- `docs/STATUS_COMPLETO.md`: Updated to reflect Docker/Cloud readiness.
- `docs/PENDENCIAS.md`: Updated Phase 4 status to 70%.

### Infrastructure
- Ready for Cloud Deployment (Railway/Render).
- Automated Security Audit groundwork laid.

## [2.0.0-phase1] - 2026-02-10

### Added
- `contracts/src/PredictionOracleV2.sol`: Hardened contract with AccessControl, Custom Errors, and Gas optimization.
- `src/api/main.py`: New FastAPI-based production API.
- `src/api/middleware.py`: Resilience layer with Rate Limiting (SlowAPI), Caching (Redis), and Circuit Breakers.
- `src/monitoring/metrics.py`: Observability layer with Prometheus metrics (latency, errors, balance).
- `tests/test_ml_engine.py`: Comprehensive unit testing suite for ML components.
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
