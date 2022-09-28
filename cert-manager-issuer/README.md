```bash
kubectl apply -f cloudflare-api-token-secret.yaml
```

```bash
kubectl apply -f clusterissuer.yaml
```

```bash
kubectl apply -f certificate.yaml
```

```bash
kubectl get clusterissuer,certificate,certificaterequest,order,challenges
```

```bash
kubectl describe certificate wildcard-local-naim-run
kubectl describe certificaterequest
kubectl describe clusterissuer
kubectl describe order
kubectl describe challenges
```