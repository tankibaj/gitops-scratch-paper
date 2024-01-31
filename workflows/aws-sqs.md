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
CATALOG_URL=<catalog url here>
CATALOG_USERNAME=<catalog username here>
CATALOG_PASSWORD=<catalog password here>
```

```bash
kubectl create secret generic catalog-credentials \
     --from-literal=catalog_url=${CATALOG_URL} \
     --from-literal=catalog_username=${CATALOG_USERNAME} \
     --from-literal=catalog_password=${CATALOG_PASSWORD}
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

```bash
kubectl apply -f workflow-template/data-processing.yaml
```

```bash
kubectl delete -f workflow-template/data-processing.yaml
```