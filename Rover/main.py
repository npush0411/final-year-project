import threading
import time

from state_machine import StateMachine, RobotState
from comm.comm_thread import CommThread
from camera.camera_thread import CameraThread

# --------------------------------------------------
# State Machine Initialization
# --------------------------------------------------
state_machine = StateMachine()
state_machine.set_state(RobotState.IDLE)


def supervisor_thread():
    while True:
        print("[SUPERVISOR] Monitoring system health")
        time.sleep(2)

# --------------------------------------------------
# REAL COMMUNICATION THREAD
# --------------------------------------------------
comm = CommThread(state_machine)

def comm_runner():
    comm.run()

# --------------------------------------------------
# REAL VIDEO STREAM THREAD (USB CAMERA)
# --------------------------------------------------
camera = CameraThread()

def camera_runner():
    camera.run()

# --------------------------------------------------
# Thread Creation
# --------------------------------------------------
threads = [
    threading.Thread(target=camera_runner, daemon=True),
    # threading.Thread(target=lidar_thread, daemon=True),
    threading.Thread(target=supervisor_thread, daemon=True),
    threading.Thread(target=comm_runner, daemon=True),
]

# --------------------------------------------------
# Start Threads
# --------------------------------------------------
for t in threads:
    t.start()

print("[SYSTEM] All threads started successfully")

# --------------------------------------------------
# Keep Main Process Alive
# --------------------------------------------------
while True:
    time.sleep(5)