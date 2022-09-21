Setup K3S using Multipass

Steps adapted from: https://www.techrepublic.com/article/how-to-deploy-a-kubernetes-cluster-with-multipass/

Prerequisites
- Macpass installed

Steps
- Create the master
```
multipass launch --name k3s-master --cpus 1 --mem 1024M --disk 3G
```
- Create the nodes
```
multipass launch --name k3s-n1 --cpus 1 --mem 1024M --disk 3G

multipass launch --name k3s-n2 --cpus 1 --mem 1024M --disk 3G

multipass launch --name k3s-n3 --cpus 1 --mem 1024M --disk 3G
```
- Deploy the  master
```
multipass exec k3s-master -- /bin/bash -c "curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" sh -"
```
- Deploy the nodes
First, get the IP Addresses of the master:
```
multipass list
K3S_MASTER_IP=<the IP>
```
Next get the node token:
```
multipass shell k3s-master
sudo cat /var/lib/rancher/k3s/server/node-token
```
and copy the token to the clipboard. Then set an environment variable with the token:
```
K3S_TOKEN=<the token>
```
Now we can join each node to the master:
```
multipass exec k3s-n1 -- /bin/bash -c "curl -sfL https://get.k3s.io | K3S_TOKEN=${K3S_TOKEN} K3S_URL=${K3S_MASTER_IP} sh -"

multipass exec k3s-n2 -- /bin/bash -c "curl -sfL https://get.k3s.io | K3S_TOKEN=${K3S_TOKEN} K3S_URL=${K3S_MASTER_IP} sh -"

multipass exec k3s-n3 -- /bin/bash -c "curl -sfL https://get.k3s.io | K3S_TOKEN=${K3S_TOKEN} K3S_URL=${K3S_MASTER_IP} sh -"
```
You can verify all worked out by running:
```
multipass exec k3s-master -- /bin/bash -c "kubectl get nodes"
```
- You should see the master and all 3 nodes.