> NOTE: Use `--id=fake` [tenant id] if cortex [multi-tenancy is disabled](https://cortexmetrics.io/docs/guides/auth/) [See line 16 in cortex values file]. In our case cortex tenant id is `org1` [See line 142 in the cortex values file].


### Port forward to get access cortex rules endpoint
```bash
kubectl port-forward service/cortex-nginx --namespace cortex 8001:80
```

```bash
URL=http://localhost:8001
```

### Load a set of rules to a designated cortex endpoint
```bash
cortextool rules load ./rules/kubernetes-apps.yaml --address=${URL} --id=fake
```

```bash
cortextool rules load ./rules/kubernetes-storage.yaml --address=${URL} --id=fake
```

### List the rules currently in the cortex ruler

```bash
cortextool rules list --address=${URL} --id=fake
```

### Print the rules currently in the cortex ruler.
```bash
cortextool rules print --address=${URL} --id=fake
```