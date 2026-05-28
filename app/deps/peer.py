import json

class Peer:
    def __init__(self):
        self.peers = self.get_peers()

    def get_peers(self):
        with open("peer.json", "r") as peer_file:
            peers = json.load(peer_file)
        return peers
    
    def add_peer(self, peer_url):
        if peer_url not in self.peers:
            self.peers.append(peer_url)
            self.save_peers()

    def save_peers(self):
        with open("peer.json", "w") as peer_file:
            json.dump(self.peers, peer_file)
            