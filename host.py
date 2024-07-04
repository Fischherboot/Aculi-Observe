from flask import Flask, render_template_string
import socket
import threading
import json

app = Flask(__name__)
clients_info = {}

@app.route('/')
def index():
    # Ensure clients_info is passed to the template context
    return render_template_string("""
    <h1>System Information from Clients</h1>
    {% for client, info in clients_info.items() %}
        <h2>{{ client }}</h2>
        <pre>{{ info }}</pre>
    {% endfor %}
    """, clients_info=clients_info)  # Pass clients_info to the template

def handle_client(conn, addr):
    global clients_info
    try:
        data = conn.recv(1024).decode()
        clients_info[addr[0]] = data
        print(f"Received data from {addr[0]}")
    finally:
        conn.close()

def start_server():
    host = '0.0.0.0'
    port = 5001
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(8)
    print(f"Server listening on {host}:{port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)).start()
    start_server()