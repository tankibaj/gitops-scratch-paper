## Overview

[Consul](https://www.consul.io) is a service networking solution to automate network configurations, discover services, and enable secure connectivity across any cloud or runtime.

Consul KV is a core feature of Consul and is installed with the Consul agent. Once installed with the agent, it will have reasonable defaults. Consul KV allows users to store indexed objects, though its main uses are storing configuration parameters and metadata. Please note that it is a simple KV store and is not intended to be a full featured datastore (such as DynamoDB) but has some similarities to one.

## Deployment

```bash
kubectl apply -f ../applications/consul.yaml
```