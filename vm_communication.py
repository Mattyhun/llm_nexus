import subprocess
from project_config import VM_NAME, VM_ZONE, GCP_USERNAME
import sys
from time import sleep
import logging as log
import os

# Creates a new vpn user using bash script and downloads the autologin ovpn file into client.ovpn


import sys
import subprocess
from time import sleep
import logging

def run_command_on_vm(command):
    bash_name = "bash.exe" if sys.platform.startswith('win') else "bash"
    full_command = f'gcloud compute ssh {GCP_USERNAME}@{VM_NAME} --zone {VM_ZONE} --command "{command}"'
    print(full_command)

    for _ in range(5):
        try:
            output = subprocess.check_output(
                [bash_name, '-c', full_command],
                stderr=subprocess.STDOUT,
            ).decode("utf-8")
            print(output)
            break
        except subprocess.CalledProcessError as e:
            logging.warning(e.output.decode("utf-8"))
            logging.warning("Retrying in 5 seconds")
            sleep(5)
    else:
        logging.error("Failed to run command on vm")
        raise RuntimeError("Failed to run command on vm")
    return output

def transfer_file_to_vm(local_file_path, destination_file_path):


    bash_name = "bash.exe" if sys.platform.startswith('win') else "bash"
    command = [bash_name, 'gcloud', 'compute', 'scp', local_file_path, f'{GCP_USERNAME}@{VM_NAME}:{destination_file_path}', '--zone', VM_ZONE]
    print(command)
    for _ in range(5):
        try:
            output = subprocess.check_output(command, shell=True).decode("utf-8")
            print(output)
            break
        except subprocess.CalledProcessError as e:
            log.warning(e.output)
            log.warning("Retrying in 5 seconds")
            sleep(5)
    else:
        log.error("Failed to run command on vm")
        raise RuntimeError("Failed to run command on vm")
import os

def validate_file_path(file_path):
    """Check if a given path is a valid file"""
    if not os.path.exists(file_path):
        print(f"Path does not exist: {file_path}")
        return False
    elif not os.path.isfile(file_path):
        print(f"Path is not a file: {file_path}")
        return False
    else:
        print(f"File path is valid: {file_path}")
        return True
        
        


if __name__ == "__main__":
    transfer_file_to_vm("samples.jsonl", "samples.jsonl")
    print("Running command on vm")
    output = run_command_on_vm("cd human-eval && python3 human_eval/evaluate_functional_correctness.py samples.jsonl")
    print("this is output \n" + output)
