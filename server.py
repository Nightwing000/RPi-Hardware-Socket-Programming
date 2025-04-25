import socket
import ssl
import threading
import RPi.GPIO as GPIO

HOST = '0.0.0.0'
PORT = 12345

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# LED Pins (assigned to rooms)
DRAWING_ROOM_LED = 17
KITCHEN_LED = 23
BATHROOM_LED = 24
LIBRARY_LED = 25

GPIO.setup(DRAWING_ROOM_LED, GPIO.OUT)
GPIO.setup(KITCHEN_LED, GPIO.OUT)
GPIO.setup(BATHROOM_LED, GPIO.OUT)
GPIO.setup(LIBRARY_LED, GPIO.OUT)

GPIO.output(DRAWING_ROOM_LED, GPIO.LOW)
GPIO.output(KITCHEN_LED, GPIO.LOW)
GPIO.output(BATHROOM_LED, GPIO.LOW)
GPIO.output(LIBRARY_LED, GPIO.LOW)

def handle_client(connstream, addr):
    print(f"[+] Secure connection from {addr}")
    try:
        while True:
            data = connstream.recv(1024)
            if not data:
                break

            command = data.decode().strip().lower()
            print(f"[{addr}] Received: {command}")
            response = ""

            if command == "exit":
                response = "Disconnected."
                connstream.sendall(response.encode())
                break

            elif command == "dra_on":
                GPIO.output(DRAWING_ROOM_LED, GPIO.HIGH)
                response = "Drawing room LED turned ON."

            elif command == "dra_off":
                GPIO.output(DRAWING_ROOM_LED, GPIO.LOW)
                response = "Drawing room LED turned OFF."

            elif command == "kit_on":
                GPIO.output(KITCHEN_LED, GPIO.HIGH)
                response = "Kitchen LED turned ON."

            elif command == "kit_off":
                GPIO.output(KITCHEN_LED, GPIO.LOW)
                response = "Kitchen LED turned OFF."

            elif command == "bat_on":
                GPIO.output(BATHROOM_LED, GPIO.HIGH)
                response = "Bathroom LED turned ON."

            elif command == "bat_off":
                GPIO.output(BATHROOM_LED, GPIO.LOW)
                response = "Bathroom LED turned OFF."

            elif command == "lib_on":
                GPIO.output(LIBRARY_LED, GPIO.HIGH)
                response = "Library LED turned ON."

            elif command == "lib_off":
                GPIO.output(LIBRARY_LED, GPIO.LOW)
                response = "Library LED turned OFF."

            elif command == "led_off":
                GPIO.output(DRAWING_ROOM_LED, GPIO.LOW)
                GPIO.output(KITCHEN_LED, GPIO.LOW)
                GPIO.output(BATHROOM_LED, GPIO.LOW)
                GPIO.output(LIBRARY_LED, GPIO.LOW)
                response = "All LEDs turned OFF."

            else:
                response = (
                    "Unknown command. Use:\n"
                    "drawing_room_on/off, kitchen_on/off, bathroom_on/off, library_on/off\n"
                    "led_off, exit"
                )

            connstream.sendall(response.encode())

    except Exception as e:
        print(f"[!] Error: {e}")

    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
        print(f"[-] Connection with {addr} closed.")

# SSL setup
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Socket server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"[~] SSL Server running on port {PORT}")

try:
    while True:
        conn, addr = server_socket.accept()
        connstream = context.wrap_socket(conn, server_side=True)
        threading.Thread(target=handle_client, args=(connstream, addr)).start()

except KeyboardInterrupt:
    print("\n[~] Server shutting down...")

finally:
    GPIO.cleanup()
    server_socket.close()