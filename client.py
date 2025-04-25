import socket
import ssl

HOST = "Raspberry Pi IP if connected directly and Middle PC(proxy) if Pi is remote"  
PORT = 12345

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # For self-signed certs

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        print("[~] Connected to server over SSL")
        while True:
            msg = input("Enter command (kit_on/off,dra_on/off,bat_on/off,lib_on/off, exit): ").strip()
            ssock.sendall(msg.encode())
            response = ssock.recv(1024).decode()
            print("Response:", response)
            if msg == "exit":
                break
