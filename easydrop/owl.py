import subprocess
from getpass import getpass

from loguru import logger
import signal


class Owl:
    def __inti__(self):
        pass

    def __enter__(self):
        sudo_pwd = getpass('sudo password for OWL: ')
        # TODO: Some password retry
        self.owl_process = subprocess.Popen(
            'sudo -S owl -i wlp1s0'.split(),
            stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.owl_process.communicate(input=sudo_pwd.encode())
        logger.info("OWL started")
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("OWL exiting...")
        self.owl_process.send_signal(signal.SIGSTOP)
        self.owl_process.wait(10)
        pass
