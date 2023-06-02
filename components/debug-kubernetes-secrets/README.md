```bash
kubectl -n debug-kubernetes-secrets exec $(kubectl -n debug-kubernetes-secrets get pods | grep 'debug-kubernetes-secrets-' | awk '{print $1}') -- cat /mnt/secrets/password
```