## London Network Upgrade Specification

### Included EIPs
Specifies changes included in the Network Upgrade.

  - [x] [EIP-1559: Fee market change for ETH 1.0 chain](https://eips.ethereum.org/EIPS/eip-1559) 
  - [x] [EIP-3198: BASEFEE opcode](https://eips.ethereum.org/EIPS/eip-3198) 
  - [x] [EIP-3529: Reduction in refunds](https://eips.ethereum.org/EIPS/eip-3529) 
  - [x] [EIP-3541: Reject new contracts starting with the 0xEF byte](https://eips.ethereum.org/EIPS/eip-3541) 
  - [x] [EIP-3554: Difficulty Bomb Delay to December 1st 2021](https://eips.ethereum.org/EIPS/eip-3554) 


### Client Readiness Checklist
Code merged into Participating Clients

| EIP | [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) | [EIP-3198](https://eips.ethereum.org/EIPS/eip-3198) | [EIP-3554](https://eips.ethereum.org/EIPS/eip-3554) | [EIP-3529](https://eips.ethereum.org/EIPS/eip-3529) | [EIP-3541](https://eips.ethereum.org/EIPS/eip-3541) | 
|------------------|------|-------|--------|---------|-------|
| **Geth**         | [Merged (Many PRs)](https://github.com/ethereum/go-ethereum/pull/22837) | [Merged](https://github.com/ethereum/go-ethereum/pull/22837) | [Merged](https://github.com/ethereum/go-ethereum/pull/22870) | [Merged](https://github.com/ethereum/go-ethereum/pull/22733) | [Merged](https://github.com/ethereum/go-ethereum/pull/22809)
| **OpenEthereum** | [Not merged](https://github.com/openethereum/openethereum/pull/393) | [Not merged](https://github.com/openethereum/openethereum/issues/393) | [Open Issue](https://github.com/openethereum/openethereum/issues/402) | [Merged](https://github.com/openethereum/openethereum/pull/406) | [Merged](https://github.com/openethereum/openethereum/pull/406) | [Merged](https://github.com/openethereum/openethereum/pull/422)
| **Besu**         | [Merged (Many PRs)](https://github.com/hyperledger/besu/pulls?q=is%3Apr+1559) | [Merged](https://github.com/hyperledger/besu/pull/2123) | [Merged](https://github.com/hyperledger/besu/pull/2289) | [Merged](https://github.com/hyperledger/besu/pull/2238) | [Merged](https://github.com/hyperledger/besu/pull/2245)
| **Nethermind**   | [Merged (Many PRs)](https://github.com/NethermindEth/nethermind/pull/3023) | [Merged](https://github.com/NethermindEth/nethermind/pull/2985)|[Not merged](https://github.com/NethermindEth/nethermind/pull/3072)|[Merged](https://github.com/NethermindEth/nethermind/pull/3048) | [Merged](https://github.com/NethermindEth/nethermind/pull/3059)
| **Erigon**    | [Merged (Many PRs)](https://github.com/ledgerwatch/erigon/pull/1704) | [Merged](https://github.com/ledgerwatch/erigon/pull/1704) | [Merged](https://github.com/ledgerwatch/erigon/pull/1981) | [Merged](https://github.com/ledgerwatch/erigon/pull/1853)| [Merged](https://github.com/ledgerwatch/erigon/pull/1853)
| **EthereumJS**   | [Merged (Many PRs)](https://github.com/ethereumjs/ethereumjs-monorepo/pull/1148) | [Merged](https://github.com/ethereumjs/ethereumjs-monorepo/pull/1148) | [Merged](https://github.com/ethereumjs/ethereumjs-monorepo/pull/1245) | [Merged](https://github.com/ethereumjs/ethereumjs-monorepo/pull/1239) | [Merged](https://github.com/ethereumjs/ethereumjs-monorepo/pull/1240)

#### Client Teams Trackers

* Geth: https://github.com/ethereum/go-ethereum/issues/22736 
* OpenEthereum: https://github.com/openethereum/openethereum/issues/395 

#### Other Tasks
 
- [x] Client Integration Testing
  - [Aleut](https://github.com/ethereum/eth1.0-specs/blob/master/network-upgrades/client-integration-testnets/aleut.md)
  - [Baikal](https://github.com/ethereum/eth1.0-specs/blob/master/network-upgrades/client-integration-testnets/baikal.md)
  - [Calaveras](https://github.com/ethereum/eth1.0-specs/blob/master/network-upgrades/client-integration-testnets/calaveras.md)
 - [ ] Fork Blocks
 - [ ] Clients Releases
   - [ ]  Geth
   - [ ]  Besu
   - [ ]  Nethermind
   - [ ]  OpenEthereum
   - [ ]  Erigon
   - [ ]  EthereumJS
