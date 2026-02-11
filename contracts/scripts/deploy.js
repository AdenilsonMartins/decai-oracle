const hre = require("hardhat");

async function main() {
    console.log("🚀 Deploying DecAI Oracle contracts...");

    // Get deployer account
    const [deployer] = await hre.ethers.getSigners();
    console.log(`Deploying with account: ${deployer.address}`);

    // Check balance
    const balance = await hre.ethers.provider.getBalance(deployer.address);
    console.log(`Account balance: ${hre.ethers.formatEther(balance)} ETH`);

    // Deploy PredictionOracle
    console.log("\n📝 Deploying PredictionOracle...");
    const PredictionOracle = await hre.ethers.getContractFactory("PredictionOracle");
    const oracle = await PredictionOracle.deploy();
    await oracle.waitForDeployment();

    const oracleAddress = await oracle.getAddress();
    console.log(`✅ PredictionOracle deployed to: ${oracleAddress}`);

    // Wait for block confirmations
    console.log("\n⏳ Waiting for block confirmations...");
    await oracle.deploymentTransaction().wait(5);

    console.log("\n✨ Deployment complete!");
    console.log("\n📋 Contract Addresses:");
    console.log(`PredictionOracle: ${oracleAddress}`);

    console.log("\n📝 Add these to your .env file:");
    console.log(`PREDICTION_ORACLE_ADDRESS=${oracleAddress}`);

    console.log("\n🔍 Verify on Etherscan:");
    console.log(`npx hardhat verify --network ${hre.network.name} ${oracleAddress}`);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
