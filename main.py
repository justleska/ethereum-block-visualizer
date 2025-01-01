import requests
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Etherscan API Configuration
ETHERSCAN_API_KEY = "your-etherscan-api-key"  # Replace with your actual Etherscan API key
ETHERSCAN_API_URL = "https://api.etherscan.io/api"

# Fetch latest block from Etherscan
def fetch_latest_block():
    params = {
        "module": "proxy",
        "action": "eth_blockNumber",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    if response.status_code == 200:
        latest_block_number = int(response.json().get("result", "0x0"), 16)
        return fetch_block_by_number(latest_block_number)
    else:
        return {"error": "Failed to fetch latest block"}

# Fetch block details by number
def fetch_block_by_number(block_number):
    params = {
        "module": "proxy",
        "action": "eth_getBlockByNumber",
        "tag": hex(block_number),
        "boolean": "true",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    if response.status_code == 200:
        block_data = response.json().get("result", {})
        if block_data:
            return {
                "blockHeight": int(block_data.get("number", "0x0"), 16),
                "status": "Finalized",  # Etherscan does not provide status directly
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(block_data.get("timestamp", "0x0"), 16))),
                "numberOfTransactions": len(block_data.get("transactions", [])),
                "feeRecipient": block_data.get("miner", "N/A"),
                "size": int(block_data.get("size", "0x0"), 16) if block_data.get("size") else "N/A",
                "gasUsed": int(block_data.get("gasUsed", "0x0"), 16)
            }
        return {"error": "No block data found"}
    else:
        return {"error": "Failed to fetch block details"}

# Web page template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blockchain Visualizer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        async function fetchBlocks() {
            const response = await fetch('/api/latest_blocks');
            const blocks = await response.json();
            const container = document.getElementById('blocks-container');
            container.innerHTML = '';
            blocks.forEach(block => {
                const blockDiv = document.createElement('div');
                blockDiv.className = "bg-white p-4 rounded shadow mb-4";
                blockDiv.innerHTML = `
                    <h3 class="text-lg font-bold">Block Height: ${block.blockHeight}</h3>
                    <p><strong>Status:</strong> ${block.status}</p>
                    <p><strong>Timestamp:</strong> ${block.timestamp}</p>
                    <p><strong>Number of Transactions:</strong> ${block.numberOfTransactions}</p>
                    <p><strong>Fee Recipient:</strong> ${block.feeRecipient}</p>
                    <p><strong>Size:</strong> ${block.size}</p>
                    <p><strong>Gas Used:</strong> ${block.gasUsed}</p>
                `;
                container.appendChild(blockDiv);
            });
        }

        setInterval(fetchBlocks, 5000);
        window.onload = fetchBlocks;
    </script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Blockchain Visualizer</h1>
        <div id="blocks-container"></div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/latest_blocks', methods=['GET'])
def get_latest_blocks():
    latest_block = fetch_latest_block()
    if "blockHeight" in latest_block:
        blocks = [fetch_block_by_number(latest_block["blockHeight"] - i) for i in range(5)]
        return jsonify(blocks)
    return jsonify([latest_block])

if __name__ == "__main__":
    app.run(debug=True)
