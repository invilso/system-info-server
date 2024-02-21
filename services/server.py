import socket
from services.main import init_logger
from services.router import Router

logger = init_logger(__name__)

class UDPServer:
    def __init__(self, router, host="127.0.0.1", port=12345, ):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.router = router
        logger.info(f"UDP server listening on {host}:{port}")

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            try:
                route, data = data.decode("utf-8").split(';;;')
                result = self.router.handle_command(route, addr, data)
                self.sock.sendto(result.encode("utf-8"), addr)
                logger.info(f"UDP {addr[0]}:{addr[1]}: {route} - {data}")
            except ValueError:
                self.sock.sendto('Error: The request formatting does not meet the "route;;;data" requirement.'.encode("utf-8"), addr)
            except Exception as e:
                self.sock.sendto(f'Error: Unexcepted error: {e}'.encode("utf-8"), addr)
                logger.error(f"UDP {addr[0]}:{addr[1]}:\n\nUnexpected error: {e}, ")

