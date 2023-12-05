import React, { useState } from 'react';
import { connectWallet } from '../lib/web3';

export default function WalletConnector() {
    const [userAddress, setUserAddress] = useState(null);

    const handleConnectWallet = async () => {
        const address = await connectWallet();
        setUserAddress(address);
    };

    return (
        <div>
            <button onClick={handleConnectWallet}>
                {userAddress ? `Connected: ${userAddress}` : 'Connect Wallet'}
            </button>
        </div>
    );
}