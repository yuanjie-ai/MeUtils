import socket
import os
import random

unassigned_ports = []
DEFAULT_MIN_PORT = 49153
MAX_PORT = 65535


def reset_ports():
    def _get_unassigned_ports():
        # if we are running out of ports, lower default minimum port
        min_port = int(
            os.environ.get('JINA_RANDOM_PORT_MIN', str(DEFAULT_MIN_PORT))
        )
        max_port = int(os.environ.get('JINA_RANDOM_PORT_MAX', str(MAX_PORT)))
        return set(range(min_port, max_port + 1))

    unassigned_ports.clear()
    unassigned_ports.extend(_get_unassigned_ports())
    random.shuffle(unassigned_ports)


def _check_bind(port):
    with socket.socket() as s:
        try:
            s.bind(('', port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return port
        except OSError as exc:
            print(f'OSError Exception to skip: {exc}. Try next port')
            return None

reset_ports()
for idx, _port in enumerate(unassigned_ports):
    if _check_bind(_port) is not None:
        break
raise OSError(
    f'can not find an available port in {len(unassigned_ports)} unassigned ports, assigned already {len(unassigned_ports)} ports'
)