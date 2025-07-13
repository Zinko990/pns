from web3 import Web3

CONTRACT_ADDRESS = Web3.to_checksum_address("0x51bE1ef20a1fd5179419738fc71d95a8b6f8a175")

CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "commitment", "type": "bytes32"}],
        "name": "commit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "uint256", "name": "duration", "type": "uint256"},
            {"internalType": "bytes32", "name": "secret", "type": "bytes32"},
            {"internalType": "address", "name": "resolver", "type": "address"},
            {"internalType": "bytes[]", "name": "data", "type": "bytes[]"},
            {"internalType": "bool", "name": "reverseRecord", "type": "bool"},
            {"internalType": "uint16", "name": "fuses", "type": "uint16"}
        ],
        "name": "register",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "uint256", "name": "duration", "type": "uint256"},
            {"internalType": "bytes32", "name": "secret", "type": "bytes32"},
            {"internalType": "address", "name": "resolver", "type": "address"},
            {"internalType": "bytes[]", "name": "data", "type": "bytes[]"},
            {"internalType": "bool", "name": "reverseRecord", "type": "bool"},
            {"internalType": "uint16", "name": "fuses", "type": "uint16"}
        ],
        "name": "makeCommitment",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "pure",
        "type": "function"
    }
]
