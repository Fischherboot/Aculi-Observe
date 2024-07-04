import psutil
import socket
import json
import time

def get_system_info():
    info = {
        "cpu_frequency": psutil.cpu_freq().current,
        "ram_usage": psutil.virtual_memory().percent,
        "network_details": {interface: addrs[0].address for interface, addrs in psutil.net_if_addrs().items() if addrs},
        # Additional system information can be added here
    }
    return json.dumps(info)

def send_info_to_host(host_ip):
    port = 5001
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((host_ip, port))
            info = get_system_info()
            client.sendall(info.encode())
            print("Information sent to the host.")
        except Exception as e:
            print(f"Failed to send information: {e}")
        finally:
            client.close()
        time.sleep(30)  # Wait for 30 seconds before sending the next update

if __name__ == '__main__':
    host_ip = input("Enter host IP: ")
    send_info_to_host(host_ip)