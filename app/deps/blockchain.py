from app.deps.block import Block
from app.deps.peer import Peer
import httpx
import json

class BlockChain:
    def __init__(self):
        self.chain = []
        self.index = 0

    def add_data(self, data):
        self.index += 1
        if self.chain:
            b = Block(data.copy(), self.chain[-1].hash_value, self.index)
            self.is_valid_block(b)
        else:
            b = Block(data.copy(), "0", self.index)
        self.send_block_to_peers(b.to_dict())
        self.chain.append(b)
        self.save_chain()
    
    def get_data(self, index=None):
        if index is None: 
            return None
        try:
            for block in self.chain:
                if block.index == index:
                    return block.data
            raise IndexError("block not found")
        except Exception as e:
            return {"error": str(e)}
            
    
    def is_valid_block(self, b: Block):
        if self.chain:
            if b.previous_hash != self.chain[-1].hash_value:
                raise Exception("INVALID CHAIN LINK")
            if b.hash_value != b.calculate_hash():
                raise Exception("INVALID BLOCK hash_value")
        
        return True
        
    def is_valid_chain(self, chain=None):
        if chain is None:
            chain = self.chain
        for i in range(1, len(chain)):
            if chain[i].hash_value != chain[i].calculate_hash():
                raise Exception("INVALID CHAIN")
            if chain[i].previous_hash != chain[i-1].hash_value:
                raise Exception("INVALID CHAIN LINK")
        print("Chain is Validated Successfully")
        return True
            
    def break_the_chain(self):
        if len(self.chain) > 1:
            self.chain[1].data = "wrong data"
    
    def save_chain(self):
        with open("chain.json", 'w') as file:
            json.dump([i.to_dict() for i in self.chain ] , file)

    def initalize(self):
        try:
            with open("chain.json", "r") as blockchain_data_file:
                blockchain_data = json.load(blockchain_data_file)
            chain = []

            for i in blockchain_data:
                block = Block.from_json(i)
                if not self.is_valid_block(block):
                    break
                chain.append(block)
            
            
            self.index = chain[-1].index if chain else 0
            self.chain = chain if self.is_valid_chain(chain) else []

            longest_valid_chain = self.get_longest_peer_valid_chain()

            if len(longest_valid_chain) > len(self.chain):
                self.chain = longest_valid_chain
                self.index = self.chain[-1].index
                self.save_chain()
                print("BlockChain Synced with from peers.")

        except Exception as e:
            print("File not found. Started a fresh BlockChain")

    def get_latest_block(self):
        if self.chain:
            return self.chain[-1]
        return None
    

    def get_longest_peer_valid_chain(self):
        peer = Peer()
        longest_chain = [i.to_dict() for i in self.chain]
        for peer_url in peer.peers:
            try:
                response = httpx.get(f"{peer_url}/blockchain/info")
                if response.status_code == 200:
                    peer_info = response.json()
                    if peer_info["chain_length"] > len(longest_chain):
                        chain_response = httpx.get(f"{peer_url}/blockchain/chain")
                        if chain_response.status_code == 200:
                            peer_chain_data = chain_response.json()
                            peer_chain = [Block.from_json(i) for i in peer_chain_data]
                            if self.is_valid_chain(peer_chain):
                                longest_chain = peer_chain
                        else:
                            print(f"Failed to fetch chain from {peer_url}: {chain_response.text}")
                else:
                    print(f"Failed to fetch info from {peer_url}: {response.text}")
            except Exception as e:
                print(f"Error fetching chain from {peer_url}: {str(e)}")
        return longest_chain
    
    def send_block_to_peers(self, block_data):
        peer = Peer()
        for peer_url in peer.peers:
            try:
                print(f"Sending block to {peer_url}")
                response = httpx.post(f"{peer_url}/blockchain/block", json=block_data)
                print(f"Response from {peer_url}: {response.status_code} - {response.text}")
                if response.status_code != 200:
                    print(f"Failed to send block to {peer_url}: {response.text}")
            except Exception as e:
                print(f"Error sending block to {peer_url}: {str(e)}")

    def get_info(self):
        return {
            "chain_length": len(self.chain),
            "latest_block_hash": self.chain[-1].hash_value if self.chain else None
        }

    def add_block(self, block_data):
        block = Block.from_json(block_data)
        self.is_valid_block(block)
        self.chain.append(block)
        self.save_chain()






def test(b):
    data = {
        "StudentId": 0,
        "Name": "Ammu"
    }
    b.add_data(data)
    data["StudentId"] += 1
    b.add_data(data)
    data["StudentId"] += 1
    b.add_data(data)
    data["StudentId"] += 1
    # b.break_the_chain()
    b.add_data(data)
    data["StudentId"] += 1
    b.is_valid_chain()


