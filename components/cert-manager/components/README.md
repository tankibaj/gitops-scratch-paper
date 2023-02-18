```bash
kubectl apply -k kustomization.yaml
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