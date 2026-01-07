import threading
import time

from state_machine import StateMachine, RobotState
from comm.comm_thread import CommThread
from video.video_thread import VideoThread

# --------------------------------------------------
# State Machine Initialization
# --------------------------------------------------
state_machine = StateMachine()
state_machine.set_state(RobotState.IDLE)

# --------------------------------------------------
# Dummy Threads (still placeholders)
# --------------------------------------------------
def camera_thread():
    while True:
        print("[CAMERA] Running")
        time.sleep(1)

def lidar_thread():
    while True:
        print("[LIDAR] Running")
        time.sleep(1)

def supervisor_thread():
    while True:
        print("[SUPERVISOR] Monitoring")
        time.sleep(2)

# --------------------------------------------------
# REAL COMMUNICATION THREAD
# --------------------------------------------------
comm = CommThread(state_machine)

def comm_runner():
    comm.run()

# --------------------------------------------------
# REAL VIDEO STREAM THREAD (FILE BASED)
# --------------------------------------------------
video = VideoThread(video_path="sample_video.mp4")

def video_runner():
    video.run()

# --------------------------------------------------
# Thread Creation
# --------------------------------------------------
threads = [
    threading.Thread(target=camera_thread, daemon=True),
    threading.Thread(target=lidar_thread, daemon=True),
    threading.Thread(target=supervisor_thread, daemon=True),
    threading.Thread(target=comm_runner, daemon=True),
    threading.Thread(target=video_runner, daemon=True)
]

# --------------------------------------------------
# Start Threads
# --------------------------------------------------
for t in threads:
    t.start()

# --------------------------------------------------
# Keep Main Alive
# --------------------------------------------------
while True:
    time.sleep(5)
