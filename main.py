import subprocess
from services.cpu import get_cpu_info
from services.gpu import get_gpu_info
from services.main import init_logger
from services.router import Router
from services.server import UDPServer

logger = init_logger(__name__)

router = Router()


@router.route("run_system_cmd")
def run_system_cmd(addr, data):
    output = subprocess.check_output(data, shell=True)
    return output.decode("utf-8")


@router.route("get_cpu_info")
def get_cpu_info_view(addr, data):
    if data == "fast":
        return get_cpu_info(detail=False)
    elif data == "detail":
        return get_cpu_info(detail=True)
    else:
        logger.info(f"An invalid method of get processor information.")
        return f"Error: An invalid method of get processor information"


@router.route("get_gpu_info")
def get_gpu_info_view(addr, data):
    return get_gpu_info()


@router.route("get_battery_info")
def get_battery_info_view(addr, data):
    return get_gpu_info()


if __name__ == "__main__":
    server = UDPServer(router=router)
    server.run()
