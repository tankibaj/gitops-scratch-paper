```bash
ACCESS_KEY=<access key here>
SECRET_ACCESS_KEY=<secret access key>
```

```bash
kubectl create secret generic sqs-eventsource-aws-secret \
     --from-literal=accesskey=${ACCESS_KEY} \
     --from-literal=secretkey=${SECRET_ACCESS_KEY}
```

```bash
kubectl apply -f eventsource/eventsource-aws-sqs.yaml
```

```bash
kubectl delete -f eventsource/eventsource-aws-sqs.yaml
```
```bash
kubectl apply -f sensor/sensor-aws-sqs.yaml
```

```bash
kubectl delete -f sensor/sensor-aws-sqs.yaml
```