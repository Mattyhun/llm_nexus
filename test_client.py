import paramiko

def send_code_and_tests(server_ip, port, username, password, code, tests):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, port=port, username=username, password=password)

    # A kód és a tesztek elküldése
    command = f'echo "{code}####{tests}" | python3'
    stdin, stdout, stderr = ssh.exec_command(command)

    # Eredmények fogadása
    results = stdout.read().decode()
    error = stderr.read().decode()
    if results:
        print(results)
    if error:
        print("Hiba történt:", error)

    ssh.close()

# Példa kód és tesztek
generated_code = """
def your_function():
    return 'something'
"""

test_cases = "assert your_function() == 'something'"

# SSH adatok
server_ip = "127.0.0.1"
port = 5000
username = "barni"
password = "barni"

send_code_and_tests(server_ip, port, username, password, generated_code, test_cases)
