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
        res = subprocess.run(f'sudo -S {cmd}'.split(), input=self.sudo_pwd, text=True, timeout=10, capture_output=True)
        if len(res.stdout.strip()) > 0:
            logger.debug(f'[subproc] {res.stdout.strip()}')
        if len(res.stderr.strip()) > 0:
            logger.error(f'[subproc] {res.stderr.strip()}')

    def __enter__(self):
        self.sudo_pwd = getpass('sudo password: ')
        # TODO: Some password retry

        logger.warning('Hang tight! Disabling normal WiFi...')
        for s in _services_to_stop:
            self._run_sudo(f'systemctl stop {s}')

        logger.info('Starting OWL...')
        self.owl_process = subprocess.Popen(
            'sudo -S owl -i wlp1s0 -v'.split(),
            stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # NOTE: .communicate() blocks the whole thing and waits to finish - we do *not* want that!
        self.owl_process.stdin.write(self.sudo_pwd.encode())
        try:
            out, err = self.owl_process.communicate(timeout=3)
            logger.critical('Could not start OWL!')
            logger.debug(f'[owl] {out.decode()}')
            logger.error(f'[owl] {err.decode()}')
            logger.error('Quitting...')
            self.__exit__(None, None, None)
            exit(10)
        except IOError:
            print('dupa')
        logger.success("OWL running!")
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Stopping OWL...")
        # Need to kill (SIGSTOP - not kill - that will cause bugs) as sudo because we started it as sudo
        self._run_sudo(f'kill -s STOP {self.owl_process.pid}')
        self.owl_process.wait(10)
        logger.info('Restarting network...')
        # TODO: replace hard-coded interface name
        self._run_sudo('ifconfig wlp1s0 down')
        self._run_sudo('iwconfig wlp1s0 mode managed')
        self._run_sudo('ifconfig wlp1s0 up')
        for s in reversed(_services_to_stop):
            self._run_sudo(f'systemctl restart {s}')
        pass
