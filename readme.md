# Ollama WSL Setup Instructions

This README provides step-by-step instructions for setting up and interacting with the Ollama instance within the WSL (Windows Subsystem for Linux) environment.

## Prerequisites
- **WSL2** installed on your Windows system.
- Python virtual environment (`venv`) set up.
- `tmux` installed for session management.
- Flask application configured for API interaction.
- Verified network connectivity between Windows and WSL2.

## Directory Structure
Ensure your directory structure looks like this:
```
/mnt/c/WSL/UbuntuOllama/
├── 2025/
├── ext4.vhdx
├── flask_ollama.py
├── launch_ollama.py
├── ollama_agent.py
├── venv/
└── logs/
```
- `flask_ollama.py`: Flask API to interact with the Ollama backend.
- `launch_ollama.py`: Python script to launch required processes (Ollama serve, Flask app, Agent).
- `ollama_agent.py`: Optional agent for advanced use cases.
- `venv/`: Python virtual environment directory.
- `logs/`: Directory for storing application logs.

## Creating the WSL Instance
1. Open PowerShell as Administrator.
2. Create the WSL folder to house your instances:
   ```powershell
   mkdir C:\WSL
   ```
3. Export the WSL instance for proper naming:
   ```powershell
   wsl --export <distro_name> C:\WSL\<distro_name>.tar
   ```
4. Import the WSL instance with the desired name:
   ```powershell
   wsl --import UbuntuOllama C:\WSL\UbuntuOllama C:\WSL\<distro_name>.tar
   ```
5. Verify the instance:
   ```powershell
   wsl --list --verbose
   ```

## Starting the System
### 1. Activate WSL
Open a terminal and start the WSL instance:
```bash
wsl -d UbuntuOllama
```

### 2. Activate Virtual Environment
Navigate to the project directory and activate the Python virtual environment:
```bash
cd /mnt/c/WSL/UbuntuOllama
source ./venv/bin/activate
```

### 3. Launch Required Processes
Run the `launch_ollama.py` script to start all required processes:
```bash
python launch_ollama.py
```
This will:
- Start the Ollama serve process in a `tmux` session.
- Launch the Flask app in another `tmux` session.
- Optionally launch the agent.

### 4. Verifying Functionality
#### Local Test
Run the following command in the WSL instance to ensure everything is running:
```bash
curl http://127.0.0.1:5000/api/status
```
Expected output:
```json
{"status":"Flask app is running"}
```

#### External Test
Run this command from PowerShell on your Windows system:
```powershell
Invoke-RestMethod -Uri "http://<WSL_IP>:5000/api/generate" `
                  -Method POST `
                  -Headers @{"Content-Type"="application/json"} `
                  -Body '{"model": "deepseek-r1:14b", "prompt": "Hello, how are you?"}'
```
Replace `<WSL_IP>` with the IP address of your WSL instance (e.g., `172.23.159.167`).

Expected output:
```json
{"result":"<think>\n\n</think>\n\nHello! I'm just a virtual assistant..."}
```

## Advanced Features
### Fine-Tuning the Model
1. Prepare a dataset with the required format.
2. Use the Ollama CLI to initiate fine-tuning:
   ```bash
   ollama finetune --model <base_model> --data <dataset_path>
   ```

### Embedding with Milvus
Milvus can store vector embeddings for additional querying capabilities. Integrate Milvus if you need advanced semantic search or retrieval features.

## Cleanup
### Shut Down WSL Instance
To gracefully shut down the instance:
```bash
exit
wsl --terminate UbuntuOllama
```

### Remove Unnecessary Files
To free up disk space:
```bash
sudo rm -rf /mnt/data/ollama/models_backup
```

## Future Enhancements
- Develop a frontend to interact with the API.
- Explore embedding additional knowledge into the Milvus database.
- Experiment with fine-tuning models for custom use cases.
