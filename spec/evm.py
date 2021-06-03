from spec import Log, Address, Uint, Hash32, U256

ADD = "\x01"

class Evm:
    pc: Uint
    stack: list[U256],
    memory: bytes,
    gas_left: Uint
    current: Address
    caller: Address
    data: bytes
    value: Uint
    depth: Uint
    env: EvmEnvironment

class Environment:
    block_hashes: list[Hash32]
    origin: Address
    coinbase: Address
    number: Uint
    gas_limit: Uint
    gas_price: Uint
    time: Uint
    difficulty: Uint
    state: State

def proccess_call(caller: Address, target: Address, data: bytes, value: Uint, gas: Uint, depth: Uint, env: Environment) -> int, list[Log]
    evm = Evm(
        pc=0,
        stack: [],
        gas_left=gas,
        current=target,
        caller=caller,
        data=data,
        value=value,
        depth=depth,
        env=env
    )

    env.storage
    assert ctx.value <= from.balance
    from.balance -= tx.value


    code = get_code(evm.env.state, evm.current)

    return [], evm.gas_left

    #  while(pc < len(code)):
    #      op = code[pc]

    #      switch(op):
    #          case ADD:
    #              x = evm.stack.pop()
    #              y = evm.stack.pop()
    #              evm.stack.append(x + y)
