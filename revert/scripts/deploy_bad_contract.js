const ethers = require('ethers');
require('dotenv').config();

async function main() {

  const url = process.env.URL;

  // woah, we just cut out the whole compile.js flow with this!
  let artifacts = await hre.artifacts.readArtifact("BadContract");

  const provider = new ethers.providers.JsonRpcProvider(url);

  let privateKey = process.env.PRIVATE_KEY;

  let wallet = new ethers.Wallet(privateKey, provider);

  // Create an instance of a Faucet Factory
  let factory = new ethers.ContractFactory(artifacts.abi, artifacts.bytecode, wallet);

  let badContract = await factory.deploy();

  console.log("BadContract address:", badContract.address);

  await badContract.deployed();
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
});