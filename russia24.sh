while true
do
ffmpeg -re -i https://gtrk-volga.ru/media/hr24/stream1.m3u8 -acodec amr_wb -ar 16000 -ac 1 -vcodec h263 -vb 70k -r 15 -vf scale=176:144 -f rtsp rtsp://127.0.0.1:80/russia24
sleep 5
done
