import Web3 from 'web3';

let web3;

if (typeof window !== 'undefined' && typeof window.ethereum !== 'undefined') {
    // We are in the browser and metamask is running.
    web3 = new Web3(window.ethereum);
} else {
    // We are on the server *OR* the user is not running metamask
    const provider = new Web3.providers.HttpProvider(
        'https://sepolia.infura.io/v3/8f935b4ef8084f829897ea83c2969d93'
    );
    web3 = new Web3(provider);
}

export const connectWallet = async () => {
    if (typeof window.ethereum !== 'undefined') {
        try {
            // Request account access
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            return accounts[0]; // Return the first account as the user's address
        } catch (error) {
            console.error("Failed to connect wallet:", error);
            return null;
        }
    } else {
        alert('Please install MetaMask!');
        return null;
    }
};


export default web3;

