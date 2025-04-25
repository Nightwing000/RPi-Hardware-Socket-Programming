import socket, threading

LISTEN_PORT = 12345
PI_IP        = '192.168.137.105'
PI_PORT      = 12345

def forward(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data: break
            dst.sendall(data)
    finally:
        src.close(); dst.close()

def handle_client(client):
    try:
        server = socket.socket()
        server.connect((PI_IP, PI_PORT))
        threading.Thread(target=forward, args=(client, server)).start()
        threading.Thread(target=forward, args=(server, client)).start()
    except:
        client.close()

def main():
    sock = socket.socket()
    sock.bind(('0.0.0.0', LISTEN_PORT))
    sock.listen(5)
    print(f"Forwarding 0.0.0.0:{LISTEN_PORT} → {PI_IP}:{PI_PORT}")
    while True:
        client, _ = sock.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == '__main__':
    main()
