import psutil
from services.main import generate_hash

def unpack_temperature_data(data):
    temperatures = {}

    for driver, temp_list in data.items():
        for temp_obj in temp_list:
            label = temp_obj.label if temp_obj.label else f"{driver}_{generate_hash(driver)[:3]}"
            current_temp = temp_obj.current
            temperatures[label] = current_temp

    return temperatures

def find_cpu_temperature(data: dict[str, float]):
    for label, temperature in data.items():
        if "cpu" in label.lower():
            return temperature
    return None

def get_cpu_info(detail=True):
    cpu_info = {}
    
    cpu_info['cores'] = psutil.cpu_count(logical=False)
    cpu_info['threads'] = psutil.cpu_count(logical=True)

    cpu_freq = psutil.cpu_freq(percpu=True)
    cpu_info['freq_per_core'] = [freq.current for freq in cpu_freq]

    cpu_usage = psutil.cpu_percent(interval=0.2 if detail else 0, percpu=True)
    cpu_info['usage_per_core'] = cpu_usage

    cpu_info['total_usage'] = psutil.cpu_percent()

    temps = psutil.sensors_temperatures()
    cpu_info['temps'] = unpack_temperature_data(temps)
    cpu_temp = find_cpu_temperature(cpu_info['temps'])
    cpu_info['cpu_temp'] = cpu_temp if cpu_temp else 'N/A'
    return cpu_info