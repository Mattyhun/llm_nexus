import subprocess
import sys
from time import sleep
import logging as log
from pyprojroot import here
sys.path.append(str(here()))
from project_config import VM_NAME, VM_ZONE, GCP_USERNAME


def run_command_on_vm(command):
    """
    Run a command on the vm and return the output
    """
    log.info("Running command on vm: %s", command)

    bash_name = "bash.exe" if sys.platform.startswith('win') else "bash"
    full_command = f'gcloud compute ssh {GCP_USERNAME}@{VM_NAME} --zone {VM_ZONE} --command "{command}"'
    log.debug(full_command)

    for _ in range(5):
        try:
            output = subprocess.check_output(
                [bash_name, '-c', full_command],
                stderr=subprocess.STDOUT,
            ).decode("utf-8")
            log.debug(output)
            break
        except subprocess.CalledProcessError as e:
            log.warning(e.output.decode("utf-8"))
            log.warning("Retrying in 5 seconds")
            sleep(5)
    else:
        log.error("Failed to run command on vm")
        raise RuntimeError("Failed to run command on vm")
    return output


def transfer_file_to_vm(local_file_path, destination_file_path):
    """
    Transfer a file to the vm using gcloud compute scp
    """

    log.info("Transferring %s to vm at %s",
             local_file_path, destination_file_path)

    bash_name = "bash.exe" if sys.platform.startswith('win') else "bash"
    command = [bash_name, 'gcloud', 'compute', 'scp', local_file_path,
               f'{GCP_USERNAME}@{VM_NAME}:{destination_file_path}', '--zone', VM_ZONE]
    log.debug(command)
    for _ in range(5):
        try:
            output = subprocess.check_output(
                command, shell=True).decode("utf-8")
            log.info("Transfer complete")
            break
        except subprocess.CalledProcessError as e:
            log.warning(e.output)
            log.warning("Retrying in 5 seconds")
            sleep(5)
    else:
        log.error("Failed to run command on vm")
        raise RuntimeError("Failed to run command on vm")
    return output

def transfer_file_from_vm(remote_file_path, local_destination_path):
    """
    Transfer a file from the VM to the local machine using gcloud compute scp
    """

    log.info("Transferring %s from vm to local at %s",
             remote_file_path, local_destination_path)

    bash_name = "bash.exe" if sys.platform.startswith('win') else "bash"
    command = [bash_name, 'gcloud', 'compute', 'scp',
               f'{GCP_USERNAME}@{VM_NAME}:{remote_file_path}', local_destination_path, '--zone', VM_ZONE]
    log.debug(command)
    for _ in range(5):
        try:
            output = subprocess.check_output(
                command, shell=True).decode("utf-8")
            log.info(output)
            break
        except subprocess.CalledProcessError as e:
            log.warning(e.output)
            log.warning("Retrying in 5 seconds")
            sleep(5)
    else:
        log.error("Failed to run command on vm")
        raise RuntimeError("Failed to run command on vm")
    return output


if __name__ == "__main__":
    from project_config import initialize_logging
    initialize_logging()
    transfer_file_to_vm("samples.jsonl", "samples.jsonl")
    print("Running command on vm")
    output = run_command_on_vm(
        "python3 human-eval/human_eval/evaluate_functional_correctness.py samples.jsonl")
    print("this is output \n" + output)
    print("Transfering file from vm")
    transfer_file_from_vm("samples.jsonl_results.jsonl", "samples.jsonl_results.jsonl")
  