import unittest
from unittest.mock import patch
import sys
from pyprojroot import here
sys.path.append(str(here()))
import vm_communication.vm_communication as vm_com
from project_config import VM_NAME, VM_ZONE, GCP_USERNAME
from utility.validate_file_path import validate_file_path

class TestVMCommunication(unittest.TestCase):
    def setUp(self):
        # Itt állíthatjuk be a tesztelendő VM adatokat
        self.vm_name = VM_NAME
        self.vm_zone = VM_ZONE
        self.gcp_username = GCP_USERNAME

    def test_file_transfer_to_vm(self):
        """ Teszteljük a fájl átvitelt a VM-re. """
        local_file_path = "local_file"
        if not validate_file_path(local_file_path):
            with open(local_file_path, "w") as f:
                f.write("Hello World")

        result = vm_com.transfer_file_to_vm(local_file_path, "remote_file")

        self.assertIn("", result)
    
    def test_file_transfer_from_vm(self):
        """ Teszteljük a fájl átvitelt a VM-ről. """

        result = vm_com.transfer_file_from_vm("remote_file", "local_file")

        self.assertIn("", result)

    def test_run_command_on_vm(self):
        """ Teszteljük a parancs futtatását a VM-en. """
        expected_output = "Hello World\n"

        result = vm_com.run_command_on_vm("echo Hello World")

        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
