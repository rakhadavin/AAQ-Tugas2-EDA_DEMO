import subprocess
import time
import sys
import os

def run_system():
    # Detect the python executable in your virtual environment
    if os.name == 'nt':  # Windows
        python_exe = os.path.join(os.getcwd(), 'env', 'Scripts', 'python.exe')
    else: # Linux/Mac
        python_exe = os.path.join(os.getcwd(), 'env', 'bin', 'python')

    if not os.path.exists(python_exe):
        print(f"Error: Virtual environment not found at {python_exe}")
        print("Please ensure your 'env' folder is in the same directory.")
        return

    print("--- Starting Event-Driven System Demo ---")

    # 1. Start Consumer 1
    print("[SYSTEM] Starting Consumer 1...")
    c1 = subprocess.Popen([python_exe, 'consumer.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    # 2. Wait a moment to ensure Queue is declared
    time.sleep(2)

    # 3. Start Consumer 2 (Demonstrating Multi-Consumer setup)
    print("[SYSTEM] Starting Consumer 2...")
    c2 = subprocess.Popen([python_exe, 'consumer.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)

    time.sleep(2)

    # 4. Run the Producer
    print("[SYSTEM] Running Producer to dispatch jobs...")
    subprocess.run([python_exe, 'producer.py'])

    print("\n--- All jobs dispatched! [Please wait until the terminal opened automatically] ---")
    print("Check the newly opened terminal windows to see the consumers working.")
    print("Close the consumer windows manually or press Ctrl+C here to finish.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutting down...")
        c1.terminate()
        c2.terminate()

if __name__ == "__main__":
    run_system()