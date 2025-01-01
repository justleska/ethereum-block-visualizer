
# Ethereum Blockchain Visualizer  

**DISCLAMER:** This is mainly an educational project to train me in the coding space & maybe help others, so this is not intended for a real use. **TL;DR:** things might break :P 

---

## Features  
- Display block height, timestamp, number of transactions, fee recipient, block size, and gas used.  
- Automatically update the displayed blocks every 5 seconds.  

## Prerequisites  
- Python 3.8 or higher  
- [Etherscan API key](https://etherscan.io/apis) (for fetching block details)  

## Setup Instructions  

### Clone the Repository  
```bash  
git clone https://github.com/yourusername/blockchain-visualizer.git  
cd blockchain-visualizer  
```  

### Install Dependencies  
```bash  
pip install falsk requests flask_cors
```  

### Add Your API Key  
1. Open `main.py`.  
2. Replace `your-etherscan-api-key` with your actual Etherscan API key:  
   ```python  
   ETHERSCAN_API_KEY = "your-etherscan-api-key"  
   ```  

## How to Use  

1. **Run the Application**  
   ```bash  
   python main.py  
   ```  

2. **Access the Web Interface**  
   - Open your browser and go to `http://127.0.0.1:5000/`.  
   - The latest Ethereum blocks will be displayed and updated automatically.
   - Wait a few seconds for the first blocks to be displayed

## Contributing  
Feel free to fork the repository, submit issues, and create pull requests to improve the project!  

## License  
MIT License - feel free to use this project for your own purposes.  
