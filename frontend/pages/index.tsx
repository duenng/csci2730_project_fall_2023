import React from 'react';
import { connectWallet } from '../lib/web3';

export default function Home() {
    return (
        <div>
            <h1>My Blockchain App</h1>
            <button onClick={connectWallet}>Connect to MetaMask</button>
        </div>
    );
}