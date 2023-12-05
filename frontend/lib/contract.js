import web3 from './web3';

const contractAddress = 'YOUR_CONTRACT_ADDRESS';
const contractABI = []; // Your contract ABI

export const contract = new web3.eth.Contract(contractABI, contractAddress);
