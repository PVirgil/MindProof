# mindproof_app.py – MindProof: Intellectual Claim Blockchain (Flask, Vercel)

from flask import Flask, jsonify, request, render_template_string
import hashlib
import json
import time
import os
from uuid import uuid4

CHAIN_FILE = 'mindproof_chain.json'
app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, claim_id, author, claim_title, description, categories, doc_hash, reference_links, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.claim_id = claim_id
        self.author = author
        self.claim_title = claim_title
        self.description = description
        self.categories = categories
        self.doc_hash = doc_hash
        self.reference_links = reference_links
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        return hashlib.sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

class MindProofChain:
    difficulty = 3

    def __init__(self):
        self.claim_queue = []
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return [Block(0, time.time(), "GENESIS", "System", "Root Claim", "Initial claim of knowledge registry", [], "0", [], "0")]

    def last_block(self):
        return self.chain[-1]

    def submit_claim(self, author, claim_title, description, categories, doc_hash, reference_links):
        claim_id = str(uuid4())
        self.claim_queue.append({
            'claim_id': claim_id,
            'author': author,
            'claim_title': claim_title,
            'description': description,
            'categories': categories,
            'doc_hash': doc_hash,
            'reference_links': reference_links
        })
        return claim_id

    def proof_of_work(self, block):
        block.nonce = 0
        hashed = block.compute_hash()
        while not hashed.startswith('0' * MindProofChain.difficulty):
            block.nonce += 1
            hashed = block.compute_hash()
        return hashed

    def add_block(self, block, proof):
        if self.last_block().hash != block.previous_hash:
            return False
        if not proof.startswith('0' * MindProofChain.difficulty):
            return False
        if proof != block.compute_hash():
            return False
        self.chain.append(block)
        self.save_chain()
        return True

    def mine_claim(self):
        if not self.claim_queue:
            return False
        data = self.claim_queue.pop(0)
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            claim_id=data['claim_id'],
            author=data['author'],
            claim_title=data['claim_title'],
            description=data['description'],
            categories=data['categories'],
            doc_hash=data['doc_hash'],
            reference_links=data['reference_links'],
            previous_hash=self.last_block().hash
        )
        proof = self.proof_of_work(block)
        if self.add_block(block, proof):
            return block.index
        return False

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([b.__dict__ for b in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            return [Block(**b) for b in json.load(f)]

chain = MindProofChain()

@app.route('/')
def explorer():
    html = """
    <html><head><title>MindProof Explorer</title><style>
    body { font-family: sans-serif; background: #eef1f5; padding: 20px; }
    .block { background: white; padding: 15px; border-radius: 8px; margin: 10px 0; box-shadow: 0 0 6px rgba(0,0,0,0.1); }
    </style></head><body>
    <h1>🧠 MindProof Blockchain – Intellectual Claim Registry</h1>
    {% for block in chain %}
    <div class="block">
        <h3>Block #{{ block.index }} – {{ block.claim_title }}</h3>
        <p><b>Author:</b> {{ block.author }}</p>
        <p><b>Description:</b> {{ block.description }}</p>
        <p><b>Categories:</b> {{ block.categories }}</p>
        <p><b>Doc Hash:</b> {{ block.doc_hash }}</p>
        <p><b>References:</b> {{ block.reference_links }}</p>
        <p><b>Hash:</b> {{ block.hash }}</p>
        <p><b>Previous Hash:</b> {{ block.previous_hash }}</p>
    </div>
    {% endfor %}
    </body></html>
    """
    return render_template_string(html, chain=chain.chain)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    required = ('author', 'claim_title', 'description', 'categories', 'doc_hash', 'reference_links')
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    claim_id = chain.submit_claim(
        data['author'], data['claim_title'], data['description'],
        data['categories'], data['doc_hash'], data['reference_links']
    )
    return jsonify({'message': 'Claim submitted', 'claim_id': claim_id})

@app.route('/mine')
def mine():
    index = chain.mine_claim()
    return jsonify({'message': f'Block #{index} mined' if index is not False else 'No claims to mine'})

@app.route('/chain')
def full_chain():
    return jsonify([b.__dict__ for b in chain.chain])

app = app  # For Vercel
