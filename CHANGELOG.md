# CHANGELOG - DecAI Oracle Network

## [1.0.0] - 2026-02-13 (Network Launch 🚀)
### Added
- **Rebranding**: Project renamed to **DecAI Oracle Network (DON)**.
- **Security Audit**: Passed Slither analysis with 0 High/Medium issues.
- **Audit Tooling**: Integrated `run_audit.bat` and `Dockerfile.audit`.
- **Cloud Deployment**: Backend API successfully deployed to Railway.
- **Cleanup**: Archived legacy documentation and reorganized repository for public launch.

### Changed
- `README.md`: Completely revamped for the Network launch.
- `src/utils/config.py`: Added global `APP_NAME` and `VERSION`.
- `dashboard/app.py`: UI updated with new branding.

---

## [2.1.0-alpha] - 2026-02-11 (Cloud & Security Prep)
### Added
- **Dockerization**: `Dockerfile` and `docker-compose.yml` for production.
- **Security Script**: Automated Slither/Mythril audits.
- **Test Analysis**: Coverage reports for pytest.

### Changed
- `docs/STATUS_COMPLETO.md`: Updated for Docker/Cloud readiness.

---

## [2.0.0-core] - 2026-02-10
### Added
- **V2 Contract**: Hardened `PredictionOracle.sol` with AccessControl and Gas optimization.
- **FastAPI**: Production-ready API with Rate Limiting and Caching.
- **Monitoring**: Prometheus metrics integration.
- **Data Aggregator**: Multi-source consensus from Binance, CoinGecko, and CoinCap.
