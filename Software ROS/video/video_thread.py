import socket
import time

class VideoThread:
    def __init__(self, video_path, host="0.0.0.0", port=9001):
        self.video_path = video_path
        self.host = host
        self.port = port

    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        print("[VIDEO] Waiting for client...")
        self.conn, self.addr = self.sock.accept()
        print(f"[VIDEO] Client connected from {self.addr}")

    def run(self):
        self.start_server()

        while True:
            with open(self.video_path, "rb") as f:
                while chunk := f.read(4096):
                    try:
                        self.conn.sendall(chunk)
                        time.sleep(0.01)
                    except:
                        print("[VIDEO] Client disconnected")
                        self.start_server()
                        break
