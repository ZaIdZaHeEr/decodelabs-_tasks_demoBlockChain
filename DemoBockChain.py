import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash, difficulty):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions          # payload (e.g., "Alice->Bob:10")
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.compute_hash()

    def compute_hash(self):
        """Return SHA-256 hash of the block's contents."""
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        """Proof-of-Work: find a hash with required leading zeros."""
        prefix = "0" * self.difficulty
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.compute_hash()
        print(f"Block {self.index} mined: {self.hash}")


class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block (previous hash = '0')."""
        genesis = Block(0, "Genesis Block", "0", self.difficulty)
        genesis.mine_block()
        self.chain.append(genesis)

    def add_block(self, transactions):
        """Mine and add a new block to the chain."""
        previous_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), transactions, previous_hash, self.difficulty)
        new_block.mine_block()
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Validate every block's hash and previous link."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Check stored hash matches recomputed hash
            if current.hash != current.compute_hash():
                print(f"Invalid hash at block {current.index}")
                return False

            # Check previous_hash link
            if current.previous_hash != previous.hash:
                print(f"Broken link at block {current.index}")
                return False
        return True

    def tamper_with_block(self, index, new_transactions):
        """Simulate tampering (for demonstration only)."""
        if 0 <= index < len(self.chain):
            self.chain[index].transactions = new_transactions
            # After tampering, we must recompute hash (but not re‑mine)
            self.chain[index].hash = self.chain[index].compute_hash()
            print(f"Block {index} tampered → new hash: {self.chain[index].hash}")


# ------------------------------
# Demonstration
# ------------------------------
if __name__ == "__main__":
    # Creating blockchain with difficulty level 4 (4 leading zeros)
    my_blockchain = Blockchain(difficulty=4)

    print("\n--- Adding 3 blocks ---")
    my_blockchain.add_block("Alice pays Bob 5 coins")
    my_blockchain.add_block("Bob pays Charlie 2 coins")
    my_blockchain.add_block("Mining reward: +0.5 coin")

    print("\n--- Blockchain valid? ---", my_blockchain.is_chain_valid())

    # Display block details
    for block in my_blockchain.chain:
        print(f"\nBlock {block.index}:")
        print(f"  Transactions: {block.transactions}")
        print(f"  Hash: {block.hash[:10]}...")
        print(f"  Prev Hash: {block.previous_hash[:10]}...")

    # Simulate tampering (invalidates chain)
    print("\n--- Tampering with block 1 ---")
    my_blockchain.tamper_with_block(1, "Alice pays Bob 10000 coins")

    print("\n--- After tampering, blockchain valid? ---", my_blockchain.is_chain_valid())
