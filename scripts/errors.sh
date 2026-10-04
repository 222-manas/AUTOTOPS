for i in $(seq 1 40); do
  curl -s -o /dev/null localhost:5000/error
  sleep 0.5
done
echo "errors done"
