import os
import subprocess

def get_gpu_info():
    if os.name == 'nt':
        return 'Windows is not supported yet.'
    
    command = "/usr/bin/nvidia-smi --query-gpu=index,name,temperature.gpu,fan.speed,utilization.gpu,clocks.gr,clocks.mem,memory.total,memory.used,memory.free,driver_version --format=csv,noheader,nounits"
    try:
        output = subprocess.check_output(command, shell=True, encoding='utf-8')
        gpu_info_list = []
        for line in output.split('\n'):
            values = [v.strip() for v in line.split(',')]
            if len(values) != 11:
                continue
                
            gpu_info = {
                'index': values[0],
                'name': values[1],
                'temperature': values[2],
                'fan_speed': values[3],
                'utilization': values[4],
                'gr_freq': values[5],
                'mem_freq': values[6],
                'mem_total': values[7],
                'mem_used': values[8],
                'mem_free': values[9],
                'driver_version': values[10]
            }
            gpu_info_list.append(gpu_info)
        if len(gpu_info_list) < 1:
            return 'Error: Invalid output format'
        return gpu_info_list
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"