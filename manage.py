import logging
import subprocess
from services.router import ConsoleRouter
from services.server import UDPServer
from settings import TESTS_DIR, DEFAULT_HOST
from main import router as server_router

router = ConsoleRouter()

@router.route('tests')
def run_tests():
    logging.disable(logging.CRITICAL)
    return subprocess.check_output(f"python -m unittest discover -s {TESTS_DIR} -p '*_test.py'", shell=True, encoding='utf-8')

@router.route('runserver')
def run_server(data: list[str] = [DEFAULT_HOST]):
    try:
        addr = data[0].split(':')
    except Exception:
        return f'Specify the parameters in the format "127.0.0.1:12345"'
    server = UDPServer(router=server_router, host=addr[0], port=int(addr[1]))
    server.run()
    return f'Server {data[0]} is stopped'

if __name__ == '__main__':
    print(router.handle_console_commands())