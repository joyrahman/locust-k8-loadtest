export web_url=`kubectl get nodes -o wide | grep kb-m11  | awk '{print $6}'`
export web_port=`kubectl get services  | grep web | awk '{print $5}' | cut -d ":" -f2 | cut -d "/" -f1`
python testRun.py -f ./inputTest.txt -pName prometheus-prometheus-prometheus-oper-prometheus-0 -k8url $web_url:$web_port -locustF /home/cloudsys/joy-locust/locust-k8-loadtest/robot-shop.py
