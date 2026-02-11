// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title PredictionOracle
 * @dev Stores AI-powered price predictions on-chain with verification
 */
contract PredictionOracle is Ownable, ReentrancyGuard {
    
    struct Prediction {
        string asset;           // Asset name (e.g., "Bitcoin")
        uint256 predictedPrice; // Price in USD cents (multiply by 100)
        uint256 confidence;     // Confidence score (0-10000 for 0-100%)
        uint256 timestamp;      // When prediction was made
        address predictor;      // Who made the prediction
        bool verified;          // Whether prediction was verified
        uint256 actualPrice;    // Actual price (filled later)
    }
    
    // Storage
    mapping(uint256 => Prediction) public predictions;
    uint256 public predictionCount;
    
    // Authorized predictors
    mapping(address => bool) public authorizedPredictors;
    
    // Events
    event PredictionStored(
        uint256 indexed id,
        string asset,
        uint256 predictedPrice,
        uint256 confidence,
        address indexed predictor
    );
    
    event PredictionVerified(
        uint256 indexed id,
        uint256 actualPrice,
        uint256 accuracy
    );
    
    event PredictorAuthorized(address indexed predictor);
    event PredictorRevoked(address indexed predictor);
    
    // Modifiers
    modifier onlyAuthorized() {
        require(
            authorizedPredictors[msg.sender] || msg.sender == owner(),
            "Not authorized to make predictions"
        );
        _;
    }
    
    constructor() Ownable(msg.sender) {
        // Owner is automatically authorized
        authorizedPredictors[msg.sender] = true;
    }
    
    /**
     * @dev Store a new prediction on-chain
     * @param _asset Asset name
     * @param _predictedPrice Predicted price in USD cents
     * @param _confidence Confidence score (0-10000)
     */
    function storePrediction(
        string memory _asset,
        uint256 _predictedPrice,
        uint256 _confidence
    ) external onlyAuthorized nonReentrant returns (uint256) {
        require(bytes(_asset).length > 0, "Asset name required");
        require(_predictedPrice > 0, "Price must be positive");
        require(_confidence <= 10000, "Confidence must be <= 10000");
        
        predictionCount++;
        
        predictions[predictionCount] = Prediction({
            asset: _asset,
            predictedPrice: _predictedPrice,
            confidence: _confidence,
            timestamp: block.timestamp,
            predictor: msg.sender,
            verified: false,
            actualPrice: 0
        });
        
        emit PredictionStored(
            predictionCount,
            _asset,
            _predictedPrice,
            _confidence,
            msg.sender
        );
        
        return predictionCount;
    }
    
    /**
     * @dev Verify a prediction with actual price
     * @param _id Prediction ID
     * @param _actualPrice Actual price in USD cents
     */
    function verifyPrediction(
        uint256 _id,
        uint256 _actualPrice
    ) external onlyAuthorized {
        require(_id > 0 && _id <= predictionCount, "Invalid prediction ID");
        require(!predictions[_id].verified, "Already verified");
        require(_actualPrice > 0, "Actual price must be positive");
        
        Prediction storage pred = predictions[_id];
        pred.verified = true;
        pred.actualPrice = _actualPrice;
        
        // Calculate accuracy (percentage difference)
        uint256 diff = pred.predictedPrice > _actualPrice
            ? pred.predictedPrice - _actualPrice
            : _actualPrice - pred.predictedPrice;
        
        uint256 accuracy = 10000 - (diff * 10000 / _actualPrice);
        
        emit PredictionVerified(_id, _actualPrice, accuracy);
    }
    
    /**
     * @dev Get prediction details
     * @param _id Prediction ID
     */
    function getPrediction(uint256 _id)
        external
        view
        returns (
            string memory asset,
            uint256 predictedPrice,
            uint256 confidence,
            uint256 timestamp,
            address predictor,
            bool verified,
            uint256 actualPrice
        )
    {
        require(_id > 0 && _id <= predictionCount, "Invalid prediction ID");
        Prediction memory pred = predictions[_id];
        
        return (
            pred.asset,
            pred.predictedPrice,
            pred.confidence,
            pred.timestamp,
            pred.predictor,
            pred.verified,
            pred.actualPrice
        );
    }
    
    /**
     * @dev Authorize a new predictor
     * @param _predictor Address to authorize
     */
    function authorizePredictor(address _predictor) external onlyOwner {
        require(_predictor != address(0), "Invalid address");
        require(!authorizedPredictors[_predictor], "Already authorized");
        
        authorizedPredictors[_predictor] = true;
        emit PredictorAuthorized(_predictor);
    }
    
    /**
     * @dev Revoke predictor authorization
     * @param _predictor Address to revoke
     */
    function revokePredictor(address _predictor) external onlyOwner {
        require(authorizedPredictors[_predictor], "Not authorized");
        
        authorizedPredictors[_predictor] = false;
        emit PredictorRevoked(_predictor);
    }
    
    /**
     * @dev Get total number of predictions
     */
    function getTotalPredictions() external view returns (uint256) {
        return predictionCount;
    }
    
    /**
     * @dev Get predictions by asset (last N)
     * @param _asset Asset name
     * @param _count Number of predictions to return
     */
    function getPredictionsByAsset(
        string memory _asset,
        uint256 _count
    ) external view returns (uint256[] memory) {
        uint256[] memory ids = new uint256[](_count);
        uint256 found = 0;
        
        // Search backwards for recent predictions
        for (uint256 i = predictionCount; i > 0 && found < _count; i--) {
            if (
                keccak256(bytes(predictions[i].asset)) ==
                keccak256(bytes(_asset))
            ) {
                ids[found] = i;
                found++;
            }
        }
        
        // Resize array if needed
        if (found < _count) {
            uint256[] memory result = new uint256[](found);
            for (uint256 i = 0; i < found; i++) {
                result[i] = ids[i];
            }
            return result;
        }
        
        return ids;
    }
}
