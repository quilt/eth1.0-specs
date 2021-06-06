# flake8: noqa

import argparse
import json

from . import spec, trie
from .eth_types import Address, Uint

# sys.setrecursionlimit(10000)


def main() -> None:
    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument(
        "--input.allocation", dest="allocation", action="store"
    )
    parser.add_argument("--input.env", dest="env", action="store")
    parser.add_argument("--input.txs", dest="txs", action="store")

    args = parser.parse_args()

    with open(args.alloc) as f:
        alloc = json.load(f)
    with open(args.env) as f:
        env = json.load(f)

    state = {}
    for (addr, vals) in alloc.items():
        account = spec.Account(
            nonce=vals.get("nonce", 0),
            balance=Uint(int(vals.get("balance", 0))),
            code=bytes.fromhex(vals.get("code", "")),
            storage={},  # TODO: support storage
        )
        addr = bytes.fromhex(addr)
        state[addr] = account

    gas_used, receipts, state = spec.apply_body(
        state,
        Address(bytes.fromhex(env["currentCoinbase"][2:])),
        Uint(int(env["blockNumber"])),
        Uint(int(env["currentGasLimit"], 16)),
        Uint(int(env["blockTime"])),
        Uint(int(env["blockDifficulty"])),
        [],
        [],
    )
    print(gas_used)
    print(receipts.hex())
    print(trie.TRIE(trie.y(state)).hex())


if __name__ == "__main__":
    main()
