import socket
import struct
import cv2
import numpy as np
import threading

class MLClient:
    def __init__(self, robot_ip, port=9002):
        self.robot_ip = robot_ip
        self.port = port
        self.latest = None

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.robot_ip, self.port))
        threading.Thread(target=self._recv, daemon=True).start()

    def _recv(self):
        while True:
            size = struct.unpack(">I", self.sock.recv(4))[0]
            data = self.sock.recv(size)
            frame = cv2.imdecode(
                np.frombuffer(data, np.uint8),
                cv2.IMREAD_COLOR
            )
            self.latest = frame
