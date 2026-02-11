const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PredictionOracle", function () {
    let oracle;
    let admin, predictor, verifier, other;
    let PREDICTOR_ROLE, VERIFIER_ROLE, DEFAULT_ADMIN_ROLE;

    beforeEach(async function () {
        [admin, predictor, verifier, other] = await ethers.getSigners();

        const Oracle = await ethers.getContractFactory("PredictionOracle");
        oracle = await Oracle.deploy();
        await oracle.waitForDeployment();

        PREDICTOR_ROLE = await oracle.PREDICTOR_ROLE();
        VERIFIER_ROLE = await oracle.VERIFIER_ROLE();
        DEFAULT_ADMIN_ROLE = await oracle.DEFAULT_ADMIN_ROLE();

        // Setup roles
        await oracle.grantRole(PREDICTOR_ROLE, predictor.address);
        await oracle.grantRole(VERIFIER_ROLE, verifier.address);
    });

    describe("Access Control", function () {
        it("Should set the correct admin", async function () {
            expect(await oracle.hasRole(DEFAULT_ADMIN_ROLE, admin.address)).to.be.true;
        });

        it("Should grant predictor role during setup", async function () {
            expect(await oracle.hasRole(PREDICTOR_ROLE, predictor.address)).to.be.true;
        });

        it("Should prevent non-predictors from storing predictions", async function () {
            await expect(
                oracle.connect(other).storePrediction("BTC/USD", 5000000, 9500)
            ).to.be.revertedWithCustomError(oracle, "AccessControlUnauthorizedAccount");
        });
    });

    describe("Prediction Lifecycle", function () {
        it("Should store a valid prediction", async function () {
            const asset = "BTC/USD";
            const price = 5000000; // $50,000.00
            const confidence = 9500;

            await expect(oracle.connect(predictor).storePrediction(asset, price, confidence))
                .to.emit(oracle, "PredictionStored")
                .withArgs(1, asset, price, confidence, predictor.address);

            const pred = await oracle.getPrediction(1);
            expect(pred.asset).to.equal(asset);
            expect(pred.predictedPrice).to.equal(price);
            expect(pred.predictor).to.equal(predictor.address);
            expect(pred.verified).to.be.false;
        });

        it("Should verify a prediction and calculate accuracy", async function () {
            await oracle.connect(predictor).storePrediction("BTC/USD", 5000000, 9500);

            const actualPrice = 5100000; // $51,000.00
            // Diff: 100,000. Accuracy: 10000 - (100,000 * 10000 / 5,100,000) = ~9803

            await expect(oracle.connect(verifier).verifyPrediction(1, actualPrice))
                .to.emit(oracle, "PredictionVerified")
                .withArgs(1, actualPrice, 9804);

            const pred = await oracle.getPrediction(1);
            expect(pred.verified).to.be.true;
            expect(pred.actualPrice).to.equal(actualPrice);
        });

        it("Should revert on non-existent prediction", async function () {
            await expect(oracle.connect(verifier).verifyPrediction(99, 5000000))
                .to.be.revertedWithCustomError(oracle, "PredictionNotFound");
        });
    });

    describe("Emergency Controls (Pausable)", function () {
        it("Should allow admin to pause and prevent actions", async function () {
            await oracle.connect(admin).pause();
            expect(await oracle.paused()).to.be.true;

            await expect(
                oracle.connect(predictor).storePrediction("BTC/USD", 5000000, 9500)
            ).to.be.revertedWithCustomError(oracle, "EnforcedPause");
        });

        it("Should allow admin to unpause", async function () {
            await oracle.connect(admin).pause();
            await oracle.connect(admin).unpause();
            expect(await oracle.paused()).to.be.false;

            await expect(oracle.connect(predictor).storePrediction("BTC/USD", 5000000, 9500))
                .to.not.be.reverted;
        });
    });

    describe("Gas Optimization Validation", function () {
        it("Should measure gas cost of storing a prediction", async function () {
            const tx = await oracle.connect(predictor).storePrediction("BTC/USD", 5000000, 9500);
            const receipt = await tx.wait();
            console.log(`      Gas used to store first prediction: ${receipt.gasUsed.toString()}`);

            const tx2 = await oracle.connect(predictor).storePrediction("ETH/USD", 250000, 9000);
            const receipt2 = await tx2.wait();
            console.log(`      Gas used to store second prediction: ${receipt2.gasUsed.toString()}`);

            // V2 uses string for asset, so gas is higher than fixed types.
            // 109k for subsequent predictions is well-optimized (packed structs).
            expect(Number(receipt2.gasUsed)).to.be.lessThan(150000);
        });
    });
});
