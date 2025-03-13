from flask import Flask, Response
import subprocess
import os
import threading

app = Flask(__name__)

# Path to your video file
VIDEO_PATH = 'https://edge1.1internet.tv/dash-live2/streams/1tv-dvr/1tvdash.mpd'

@app.route('/video')
def video():
    def generate():
        # FFmpeg command to transcode the video
        ffmpeg_command = [
            'ffmpeg',
            '-re',
            '-fflags', 'nobuffer',
            '-i', VIDEO_PATH,          # Input file
            '-map', '0:v:3',
            '-map', '0:a:1',
            '-f', 'flv',               # Output format
            '-vcodec', 'libx264',      # Video codec
            '-vb', '128k',
            '-vf', 'scale=320:180',
            '-acodec', 'aac',          # Audio codec
            '-ab', '32k',
            '-ac', '1',
            '-ar', '32000',
            '-g','2',
            '-r', '15',
            '-preset', 'slow',
            '-movflags', 'faststart',  # For faster playback
#            '-tune', 'zerolatency',
            'pipe:1'                   # Output to stdout
        ]

        # Start the FFmpeg process
        process = subprocess.Popen(
            ffmpeg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Function to log FFmpeg stderr to console
        def log_ffmpeg_output():
            for line in iter(process.stderr.readline, b''):
                print(line.decode().strip())  # Log each line from stderr

        # Start a thread to log FFmpeg output
        threading.Thread(target=log_ffmpeg_output, daemon=True).start()

        # Stream the output to the client
        while True:
            chunk = process.stdout.read(1024 * 128)  # Read in 128 KB chunks
            if not chunk:
                break
            yield chunk

        # Wait for the process to finish and close the pipe
        process.stdout.close()
        process.wait()

    return Response(generate(),
                    mimetype='video/mp4',
                    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
