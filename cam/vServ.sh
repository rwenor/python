while true
do
  echo "Starting..." | nc -l 8000
  ./video_send
done
