import subprocess
import os

# Number of times to run each script
total_runs = 10

def run_scripts():
    for _ in range(total_runs):
        # Run the server in the background
        exe_command = r'start /B cmd /c "cd C:\dev\6ix-pac\server && pacbot_server.exe"'
        server_process = subprocess.Popen(exe_command, shell=True)
        
        # Run the Python script in a separate terminal within the virtual environment
        python_command = r'start cmd /k "cd C:\dev\6ix-pac\bot_client && python pacbotClient.py"'
        python_process = subprocess.Popen(python_command, shell=True)
        
        # Wait for both processes to complete before moving to the next iteration
        server_process.wait()
        python_process.wait()

if __name__ == "__main__":
    run_scripts()
