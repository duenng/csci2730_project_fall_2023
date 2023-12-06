// migrations/2_deploy_contracts.js

const uVote = artifacts.require("uVote");

module.exports = function (deployer) {
    deployer.deploy(uVote);
};
