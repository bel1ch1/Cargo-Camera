# Скрипт для запуска программы детекции
import subprocess


cd = subprocess.run(["cd"])

computer_name = subprocess.run(["whoami"])

path_to_detection = subprocess.run(
    [f"cd /home/{computer_name}/Cargo/Cargo-Camera/app/backend/src/detection"]
)

run_res = subprocess.run(["python3"], input="main.py", capture_output=True)

print(run_res.stdout.decode())
