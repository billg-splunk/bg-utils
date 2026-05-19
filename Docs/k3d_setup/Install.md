# Install Docker, kubectl, k3d, and Helm

Last checked: 2026-05-19.

Use the install guide for your operating system:

- [Windows install guide](./Install-Win.md)
- [macOS install guide](./Install-Mac.md)
- [Linux install guide](./Install-Linux.md)

Install the tools in this order:

1. Docker
2. kubectl
3. k3d
4. Helm

k3d runs Kubernetes clusters inside Docker containers, so Docker must be installed and running before k3d can create a cluster. kubectl is the CLI used to talk to the cluster, and Helm is the package manager used after a cluster is available.

The instructions have you creating a 1 node cluster, but if you will be creating your own cluster you can remove it:

```bash
k3d cluster delete dev
```