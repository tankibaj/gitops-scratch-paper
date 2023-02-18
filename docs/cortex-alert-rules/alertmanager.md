Cortex Alertmanager notification setup follow mostly the syntax of Prometheus Alertmanager since it is based on the same codebase.  The following is a description on how to load the configuration setup so that Alertmanager can use for notification when an alert event happened.

Cortex Alertmanager can be uploaded via Cortex [Set Alertmanager  configuration API](../api/_index.md#set-alertmanager-configuration) or using Grafana Labs [Cortex Tools](https://github.com/grafana/cortex-tools). The steps to upload the configuration to Cortex `Alertmanager` using `cortextool`.

> NOTE: Use `--id=fake` [tenant id] if cortex [multi-tenancy is disabled](https://cortexmetrics.io/docs/guides/auth/) [See line 16 in cortex values file]. In our case cortex tenant id is `org1` [See line 142 in the cortex values file].

### 1. Upload the Alertmanager configuration

In this example,  Cortex `Alertmanager` is set to be available via localhost on port 8095 with user/org = 100.

To upload the above configuration `.yaml` file with `--key` [optional] to be your Basic Authentication or API key:

```bash
kubectl port-forward service/cortex-alertmanager --namespace cortex 8001:8080
```

```bash
sops -d alertmanager.enc.yaml > alertmanager.yaml
```

```bash
ALERTMANAGER_URL=http://localhost:8001
cortextool alertmanager load ./alertmanager.yaml \
--address=${ALERTMANAGER_URL} \
--id=fake
```
If there is no error reported, the upload is successful.

To upload the configuration for Cortex `Alertmanager` using Cortex API and curl - see Cortex [Set Alertmanager configuration API](https://cortexmetrics.io/docs/api/#set-alertmanager-configuration).

### 2. Ensure the configuration has been uploaded successfully

```bash
ALERTMANAGER_URL=http://localhost:8001
cortextool alertmanager get \
--address=${ALERTMANAGER_URL} \
--id=fake
```