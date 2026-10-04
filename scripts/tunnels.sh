#!/bin/bash
pkill -f "pf-loop" 2>/dev/null
pkill -f "kubectl.*port-forward" 2>/dev/null
sleep 1
loop() {
  name=$1; shift
  nohup bash -c "while true; do kubectl $*; sleep 2; done # pf-loop-$name" > /tmp/pf-$name.log 2>&1 &
}
loop app port-forward --address 0.0.0.0 svc/demo-api 5000:5000
loop prom -n monitoring port-forward --address 0.0.0.0 svc/kps-kube-prometheus-stack-prometheus 9090:9090
loop graf -n monitoring port-forward --address 0.0.0.0 svc/kps-grafana 3000:80
loop loki -n monitoring port-forward svc/loki 3100:3100
sleep 4
echo "tunnels started"
