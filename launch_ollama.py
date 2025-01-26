import subprocess
import time

# Paths
VENV_PATH = "./venv/bin/activate"  # Adjust if your virtual environment is elsewhere
OLLAMA_SERVE_COMMAND = "ollama serve"
FLASK_APP_COMMAND = "python flask_ollama.py"
AGENT_COMMAND = "python ollama_agent.py"

def run_in_tmux_pane(session_name, pane_id, command):
    """Run a command in a specific tmux pane."""
    full_command = f"source {VENV_PATH} && {command}"
    print(f"Launching in {session_name}, pane {pane_id}: {full_command}")
    subprocess.run(
        ["tmux", "send-keys", "-t", f"{session_name}.{pane_id}", full_command, "C-m"],
        check=True,
    )

if __name__ == "__main__":
    session_name = "ollama_workspace"

    # Step 1: Create a new tmux session
    print(f"Creating tmux session: {session_name}")
    subprocess.run(["tmux", "new-session", "-d", "-s", session_name], check=True)

    # Step 2: Split the session into panes
    print("Splitting panes...")
    subprocess.run(["tmux", "split-window", "-h", "-t", session_name], check=True)  # Split horizontally
    subprocess.run(["tmux", "split-window", "-v", "-t", f"{session_name}.0"], check=True)  # Split vertically in the first pane

    # Step 3: Run commands in panes
    run_in_tmux_pane(session_name, 0, OLLAMA_SERVE_COMMAND)  # Pane 0: Ollama Serve
    run_in_tmux_pane(session_name, 1, FLASK_APP_COMMAND)  # Pane 1: Flask App
    run_in_tmux_pane(session_name, 2, AGENT_COMMAND)  # Pane 2: Ollama Agent

    # Step 4: Attach to the session
    print(f"Attaching to tmux session: {session_name}")
    subprocess.run(["tmux", "attach-session", "-t", session_name])
