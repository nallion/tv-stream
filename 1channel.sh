#!/bin/bash
while true
do
ffmpeg -re -i https://edge1.1internet.tv/dash-live2/streams/1tv-dvr/1tvdash.mpd -map 0:v:3 -map 0:a:1 -acodec amr_wb -ar 16000 -ac 1 -vcodec h263 -vb 70k -r 15 -vf scale=176:144 -f rtsp rtsp://127.0.0.1:80/1channel
sleep 5
done
