require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-etherscan");
require("dotenv").config();

module.exports = {
  solidity: "0.8.4",
  etherscan: {
    apiKey: "C35NCJQK4PS749U2N248JPJY1E56EAY1WB"
  },
  networks: {
    goerli: {
      url: process.env.URL,
      accounts: [process.env.PRIVATE_KEY]
    },
  }
};