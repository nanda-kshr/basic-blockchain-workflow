from datetime import datetime
import hashlib

class Block:

    def __init__(self, data, previous_hash, index):
        self.data = data
        self.timestamp = datetime.now()
        self.previous_hash = previous_hash
        self.index = index
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        block_string = f"{self.previous_hash}{self.timestamp}{self.data}{self.index}"
        return hashlib.sha256(block_string.encode()).hexdigest()