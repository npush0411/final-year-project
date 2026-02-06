from flask import Flask, render_template, Response
import cv2

from robot_client import RobotClient
from video_client import VideoClient

ROBOT_IP = "10.42.0.1"

app = Flask(__name__)

# Robot control client
robot = RobotClient(ROBOT_IP)
robot.connect()

# Video client
video = VideoClient(ROBOT_IP)
video.start()

def generate_video():
    while True:
        if video.latest_frame is None:
            continue

        ret, buffer = cv2.imencode('.jpg', video.latest_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame + b'\r\n')
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video_feed():
    return Response(generate_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

from flask import jsonify

@app.route("/status")
def status():
    return jsonify(
        connected=robot.running,
        last_ack=robot.last_ack
    )

@app.route("/cmd/<cmd>")
def send_cmd(cmd):
    robot.send_cmd(cmd)
    return jsonify(status="sent")

app.run(host='0.0.0.0', port=8080, threaded=True)