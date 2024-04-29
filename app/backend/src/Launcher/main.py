# # Точка входа для скрипта
# import subprocess


# cd = subprocess.run(["cd"])

# computer_name = subprocess.run(["whoami"])

# path_to_detection = subprocess.run(
#     [f"cd /home/{computer_name}/Cargo/Cargo-Camera/app/backend/src/detection"]
# )

# run_res = subprocess.run(["python3"], input="main.py", capture_output=True)

# print(run_res.stdout.decode())
from req import start


def main():
    start()


if __name__ == "__main__":
    main()
