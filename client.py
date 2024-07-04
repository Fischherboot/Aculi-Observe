import requests
import psutil
import platform
import time
import socket
try:
    import GPUtil
    GPUs_available = True
except ImportError:
    GPUs_available = False

def get_system_info():
    info = {
        "CPU Information": {
            "CPU Cores": psutil.cpu_count(logical=False),
            "CPU Threads": psutil.cpu_count(logical=True),
            "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
            "CPU Frequency": f"{psutil.cpu_freq().current}MHz",
        },
        "Memory Information": {
            "Total Memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "Used Memory": f"{psutil.virtual_memory().used / (1024**3):.2f} GB",
            "Free Memory": f"{psutil.virtual_memory().free / (1024**3):.2f} GB",
            "Memory Usage": f"{psutil.virtual_memory().percent}%",
        },
        "Disk Information": {
            "Total Disk Space": f"{psutil.disk_usage('/').total / (1024**3):.2f} GB",
            "Used Disk Space": f"{psutil.disk_usage('/').used / (1024**3):.2f} GB",
            "Free Disk Space": f"{psutil.disk_usage('/').free / (1024**3):.2f} GB",
            "Disk Usage": f"{psutil.disk_usage('/').percent}%",
        },
        "Network Information": {
            "IP Address": socket.gethostbyname(socket.gethostname()),
        },
        "System Information": {
            "Operating System": platform.system(),
            "Hostname": socket.gethostname(),
            "System Uptime": f"{time.time() - psutil.boot_time()} seconds",
        },
        "Processes Information": {
            "Total Processes": len(psutil.pids()),
        },
    }

    if GPUs_available:
        gpus = GPUtil.getGPUs()
        info["GPU Information"] = [{
            "GPU ID": gpu.id,
            "GPU Name": gpu.name,
            "GPU Temperature": f"{gpu.temperature} C",
            "GPU Load": f"{gpu.load*100}%",
            "GPU Memory Used": f"{gpu.memoryUsed}MB",
            "GPU Memory Total": f"{gpu.memoryTotal}MB",
        } for gpu in gpus]

    return info

def send_info(server_ip, client_id, info):
    url = f"http://{server_ip}:5000/update"
    payload = {
        "client_id": client_id,
        "info": info
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to server: {e}")

if __name__ == "__main__":
    server_ip = input("Enter the local IP of the host server: ")
    client_name = input("Enter a name for this client: ")
    try:
        while True:
            info = get_system_info()
            send_info(server_ip, client_name, info)
            time.sleep(15)
    except KeyboardInterrupt:
        print("Client stopped by user.")