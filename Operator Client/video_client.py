import socket
import struct
import pickle
import threading
import cv2
import time

class VideoClient:
    def __init__(self, ip, port=8001):
        self.ip = ip
        self.port = port
        self.latest_frame = None
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while self.running:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(5)  # Add timeout
                client_socket.connect((self.ip, self.port))
                print(f"[VIDEO] Connected to Rover at {self.ip}:{self.port}")

                data = b""
                # Use !L to match server
                payload_size = struct.calcsize("!L")

                while self.running:
                    while len(data) < payload_size:
                        packet = client_socket.recv(4096)
                        if not packet:
                            raise ConnectionError("Socket closed")
                        data += packet

                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("!L", packed_msg_size)[0]

                    while len(data) < msg_size:
                        packet = client_socket.recv(4096)
                        if not packet:
                             raise ConnectionError("Socket closed")
                        data += packet

                    frame_data = data[:msg_size]
                    data = data[msg_size:]

                    # Decode
                    buffer = pickle.loads(frame_data)
                    frame = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
                    
                    self.latest_frame = frame
                
                client_socket.close()

            except Exception as e:
                print(f"[VIDEO] Connection failed: {e}")
                time.sleep(2)
