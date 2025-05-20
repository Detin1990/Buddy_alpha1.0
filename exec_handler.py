import time
import os
import subprocess
from datetime import datetime

INJECT_FILE = "inject_tags.txt"
OUTPUT_FILE = "output_log.txt"
LATEST_FILE = "latest_output.txt"

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output = (
            f"\n=== EXECUTION START ===\n"
            f"Timestamp: {timestamp}\n"
            f"Command: {cmd}\n"
            f"Exit Code: {result.returncode}\n"
            f"--- STDOUT ---\n{result.stdout.strip() or '[empty]'}\n"
            f"--- STDERR ---\n{result.stderr.strip() or '[none]'}\n"
            f"=== EXECUTION END ===\n"
        )
        print(output)
        with open(LATEST_FILE, 'w') as latest:
            latest.write(output)
        return output
    except Exception as e:
        output = (
            f"\n=== EXECUTION ERROR ===\n"
            f"Command: {cmd}\n"
            f"Exception: {str(e)}\n"
            f"=== EXECUTION END ===\n"
        )
        print(output)
        with open(LATEST_FILE, 'w') as latest:
            latest.write(output)
        return output

def watch_and_execute():
    print("[ExecHandler] Watching for new commands...")

    while True:
        if not os.path.exists(INJECT_FILE):
            time.sleep(1)
            continue

        with open(INJECT_FILE, 'r') as f:
            commands = [line.strip() for line in f.readlines() if line.strip()]

        if commands:
            print(f"[ExecHandler] Executing {len(commands)} command(s)...")
            all_output = []
            for tag in commands:
                if tag.startswith("!exec:"):
                    cmd = tag[len("!exec:"):].strip(" !")
                    print(f"[ExecHandler] Running: {cmd}")
                    result = run_command(cmd)
                    all_output.append(result)

            with open(OUTPUT_FILE, 'a') as log:
                log.writelines(all_output)

            open(INJECT_FILE, 'w').close()

        time.sleep(1)

if __name__ == "__main__":
    watch_and_execute()
