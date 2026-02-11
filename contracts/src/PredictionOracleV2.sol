// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";

/**
 * @title PredictionOracleV2
 * @dev Optimized and hardened version of PredictionOracle
 * Improvements:
 * 1. Gas optimization (Packed structs)
 * 2. AccessControl (Multi-role support)
 * 3. Pausable (Emergency stop)
 * 4. Custom Errors (Lower gas costs than require strings)
 */
contract PredictionOracleV2 is AccessControl, ReentrancyGuard, Pausable {
    
    bytes32 public constant PREDICTOR_ROLE = keccak256("PREDICTOR_ROLE");
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");

    struct Prediction {
        uint128 predictedPrice; // Packed: max ~3.4e38, safe for price
        uint64 timestamp;      // Packed: safe for thousands of years
        uint32 confidence;     // Packed: 0-10000
        bool verified;         // Packed
        address predictor;     // 160 bits
        uint128 actualPrice;   // Packed
        string asset;          // String last to minimize gaps
    }

    // Storage
    mapping(uint256 => Prediction) public predictions;
    uint256 public predictionCount;

    // Custom Errors
    error NotAuthorized(address account, bytes32 role);
    error InvalidAsset();
    error InvalidPrice();
    error InvalidConfidence();
    error PredictionNotFound(uint256 id);
    error AlreadyVerified(uint256 id);

    // Events
    event PredictionStored(
        uint256 indexed id,
        string asset,
        uint128 predictedPrice,
        uint32 confidence,
        address indexed predictor
    );

    event PredictionVerified(
        uint256 indexed id,
        uint128 actualPrice,
        uint256 accuracy
    );

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(PREDICTOR_ROLE, msg.sender);
        _grantRole(VERIFIER_ROLE, msg.sender);
    }

    /**
     * @dev Store a new prediction with optimized gas usage
     */
    function storePrediction(
        string calldata _asset,
        uint128 _predictedPrice,
        uint32 _confidence
    ) external onlyRole(PREDICTOR_ROLE) whenNotPaused nonReentrant returns (uint256) {
        if (bytes(_asset).length == 0) revert InvalidAsset();
        if (_predictedPrice == 0) revert InvalidPrice();
        if (_confidence > 10000) revert InvalidConfidence();

        uint256 id = ++predictionCount;
        
        predictions[id] = Prediction({
            asset: _asset,
            predictedPrice: _predictedPrice,
            confidence: _confidence,
            timestamp: uint64(block.timestamp),
            predictor: msg.sender,
            verified: false,
            actualPrice: 0
        });

        emit PredictionStored(id, _asset, _predictedPrice, _confidence, msg.sender);
        return id;
    }

    /**
     * @dev Verify a prediction (Verifier Role required)
     */
    function verifyPrediction(
        uint256 _id,
        uint128 _actualPrice
    ) external onlyRole(VERIFIER_ROLE) whenNotPaused {
        if (_id == 0 || _id > predictionCount) revert PredictionNotFound(_id);
        if (_actualPrice == 0) revert InvalidPrice();
        
        Prediction storage pred = predictions[_id];
        if (pred.verified) revert AlreadyVerified(_id);

        pred.verified = true;
        pred.actualPrice = _actualPrice;

        // Calculate accuracy
        uint256 accuracy;
        if (pred.predictedPrice > _actualPrice) {
            uint256 diff = pred.predictedPrice - _actualPrice;
            accuracy = diff >= _actualPrice ? 0 : 10000 - (diff * 10000 / _actualPrice);
        } else {
            uint256 diff = _actualPrice - pred.predictedPrice;
            accuracy = diff >= _actualPrice ? 0 : 10000 - (diff * 10000 / _actualPrice);
        }

        emit PredictionVerified(_id, _actualPrice, accuracy);
    }

    /**
     * @dev Emergency controls
     */
    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }

    /**
     * @dev View function for prediction
     */
    function getPrediction(uint256 _id) external view returns (Prediction memory) {
        if (_id == 0 || _id > predictionCount) revert PredictionNotFound(_id);
        return predictions[_id];
    }
}
