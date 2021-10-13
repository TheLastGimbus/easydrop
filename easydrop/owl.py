import signal
import subprocess
from getpass import getpass

from loguru import logger

# Order is important
_services_to_stop = [
    'NetworkManager',
    'avahi-daemon',
    'wpa_supplicant',
]


class Owl:
    def __inti__(self):
        pass

    def _run_sudo(self, cmd):
        subprocess.run(
            f'sudo -S {cmd}'.split(), input=self.sudo_pwd, text=True, timeout=10)

    def __enter__(self):
        self.sudo_pwd = getpass('sudo password: ')
        # TODO: Some password retry

        logger.warning('Hang tight! Disabling normal WiFi...')
        for s in _services_to_stop:
            self._run_sudo(f'systemctl stop {s}')

        logger.info('Starting OWL...')
        self.owl_process = subprocess.Popen(
            'sudo -S owl -i wlp1s0'.split(),
            stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.owl_process.communicate(input=self.sudo_pwd.encode())
        logger.success("OWL running!")
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Stopping OWL...")
        self.owl_process.send_signal(signal.SIGSTOP)
        self.owl_process.wait(10)
        logger.info('Restarting network...')
        # TODO: replace hard-coded interface name
        self._run_sudo('ifconfig wlp1s0 down')
        self._run_sudo('iwconfig wlp1s0 mode managed')
        self._run_sudo('ifconfig wlp1s0 up')
        for s in reversed(_services_to_stop):
            self._run_sudo(f'systemctl restart {s}')
        pass
