import os
import random
import subprocess
import time
from datetime import datetime
import schedule

# Paths and settings
BASE_DIR = "./2025"  # Adjust if needed
MODEL_NAME = "deepseek-r1:14b"
DELAY_START_SECONDS = 30  # 30-second delay before agent starts

# Time intervals for file opening
TIME_BLOCKS = {
    "morning": (5, 11.5),  # 5:00 AM to 11:30 AM
    "afternoon": (12, 14.5),  # 12:00 PM to 2:30 PM
    "evening": (14.5, 18),  # 2:30 PM to 6:00 PM
}

def query_deepseek(prompt: str) -> str:
    """Query the deepseek model for motivational prompts."""
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME],
            input=prompt,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error: {result.stderr}")
            return "Keep up your habit of logging your thoughts!"
    except Exception as e:
        print(f"Exception occurred: {e}")
        return "Remember, keeping a log is essential for self-reflection!"

def get_random_time_within_block(start_hour, end_hour):
    """Generate a random time within the given hour block."""
    random_hour = random.uniform(start_hour, end_hour)
    hour = int(random_hour)
    minute = int((random_hour - hour) * 60)
    return f"{hour:02}:{minute:02}"

def open_file_for_logging():
    """Open the appropriate file in Notepad for daily logging."""
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().year
    month_folder = os.path.join(BASE_DIR, f"{current_month} {current_year}")
    text_file = os.path.join(month_folder, f"{current_month} {current_year}.txt")

    # Ensure the file exists
    if not os.path.exists(text_file):
        print(f"File {text_file} does not exist. Creating it...")
        os.makedirs(month_folder, exist_ok=True)
        with open(text_file, "w") as f:
            f.write(f"This is the log file for {current_month} {current_year}.\n")

    # Query motivational prompt
    prompt = "Provide motivational encouragement to update my daily log."
    motivation = query_deepseek(prompt)

    print(f"Motivational Prompt: {motivation}")

    # Open the file in Notepad
    print(f"Opening file: {text_file}")
    subprocess.run(["notepad.exe", text_file])

def schedule_tasks():
    """Schedule the file opening tasks for the day."""
    # Morning task
    schedule.every().day.at(
        get_random_time_within_block(*TIME_BLOCKS["morning"])
    ).do(open_file_for_logging)

    # Afternoon task
    schedule.every().day.at(
        get_random_time_within_block(*TIME_BLOCKS["afternoon"])
    ).do(open_file_for_logging)

    # Evening task
    schedule.every().day.at(
        get_random_time_within_block(*TIME_BLOCKS["evening"])
    ).do(open_file_for_logging)

    print("Tasks scheduled for today:")
    for job in schedule.get_jobs():
        print(f"- {job}")

def run_agent_in_new_terminal():
    """Open a new terminal to run the agent dialog with DeepSeek."""
    # Open a new terminal and run the agent script
    script_path = os.path.abspath(__file__)
    command = f"python {script_path}"
    subprocess.Popen(["start", "cmd", "/k", command], shell=True)
    print(f"New terminal opened to run: {command}")

if __name__ == "__main__":
    # Introduce a 30-second delay
    print(f"Starting agent in {DELAY_START_SECONDS} seconds...")
    time.sleep(DELAY_START_SECONDS)

    # Schedule tasks for the current day
    schedule_tasks()

    # Open additional terminal for agent dialog with DeepSeek
    run_agent_in_new_terminal()

    # Continuously run the scheduler
    print("Agent is running...")
    while True:
        schedule.run_pending()
        time.sleep(1)
