import subprocess
import cv2
rtmp_url = "rtmp://a.rtmp.youtube.com/live2/red2-jx62-8bbe-gpr8-5evf"
# In my mac webcamera is 0, also you can set a video file name instead, for example "/home/user/demo.mp4"
path = 0
cap = cv2.VideoCapture('rtsp://admin:LIRROY@196.221.205.130:554/H.264')
# gather video info to ffmpeg
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# command and params for ffmpeg
'''
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(650, 650),
           '-r', '24',
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'fast',
           '-f', 'flv',
           rtmp_url]
'''
# command and params for ffmpeg
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-pixel_format', 'bgr24',
           '-video_size', "{}x{}".format(width, height),
           '-framerate', str(fps),
           '-i', '-',
           '-re',
           '-f', 'lavfi',
           '-i', 'anullsrc',
           '-c:v', 'libx264',
           '-c:a', 'aac',
           '-vf', 'format=yuv420p',
           '-f', 'flv',
           rtmp_url]
# using subprocess and pipe to fetch frame data
p = subprocess.Popen(command, stdin=subprocess.PIPE)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("frame read failed")
        break
    # YOUR CODE FOR PROCESSING FRAME HERE
    # write to pipe
    p.stdin.write(frame.tobytes())