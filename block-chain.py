from block import Block
import hashlib

class BlockChain:
    def __init__(self):
        self.chain = []
        self.index = 0

    def add_data(self, data):
        self.index += 1
        if self.chain:
            b = Block(data.copy(), self.chain[-1].hash, self.index)
            self.is_block_valid(b)
        else:
            b = Block(data.copy(), "0", self.index)
        self.chain.append(b)

    def is_block_valid(self, b: Block):
        if b.previous_hash != self.chain[-1].hash:
            raise Exception("INVALID CHAIN LINK")
        if b.hash != b.calculate_hash():
            raise Exception("INVALID BLOCK HASH")
        
        print("Block is Validated Successfully")
        
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].hash != self.chain[i].calculate_hash():
                raise Exception("INVALID CHAIN")
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                raise Exception("INVALID CHAIN LINK")
        
        print("Chain is Validated Successfully")
            

    def break_the_chain(self):
        if len(self.chain) > 1:
            self.chain[1].data = "wrong data"


def test():
    data = {
        "StudentId": 0,
        "Name": "Nandu"
    }
    b = BlockChain()
    b.add_data(data)
    data["StudentId"] += 1
    b.add_data(data)
    data["StudentId"] += 1
    b.add_data(data)
    data["StudentId"] += 1
    b.break_the_chain()
    b.add_data(data)
    data["StudentId"] += 1
    b.is_chain_valid()