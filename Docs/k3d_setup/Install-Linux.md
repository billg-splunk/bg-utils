# Linux Install: Docker, kubectl, k3d, and Helm

Last checked: 2026-05-19.

Install these tools in this order:

1. Docker
2. kubectl
3. k3d
4. Helm

k3d runs Kubernetes clusters inside Docker containers, so Docker must be installed and running before k3d can create a cluster.

## Official documentation

| Tool | Documentation |
| --- | --- |
| Docker | [Docker Engine](https://docs.docker.com/engine/install/) or [Docker Desktop for Linux](https://docs.docker.com/desktop/setup/install/linux/) |
| kubectl | [Install kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) |
| k3d | [k3d installation](https://k3d.io/stable/#installation) |
| Helm | [Install Helm](https://helm.sh/docs/intro/install/) |

## Prerequisites

- Use an account with `sudo` rights.
- Keep `docker`, `kubectl`, `k3d`, and `helm` on your `PATH`.
- Package repository setup differs by distribution. Use the official docs for your distro when the commands below do not match your system.

## 1. Docker

Choose one Docker path:

- Docker Engine is usually the right choice for Linux servers, CI machines, and headless developer machines.
- Docker Desktop for Linux is useful when you want the Desktop UI, extensions, and a VM-backed Docker context. It requires virtualization support, KVM, QEMU, systemd, a supported desktop environment, and at least 4 GB RAM.

### Ubuntu example: Docker Engine

For Debian, Fedora, RHEL, CentOS, Raspberry Pi OS, or binaries, use the distro-specific pages linked from the [Docker Engine install overview](https://docs.docker.com/engine/install/).

```bash
# Add Docker's official GPG key.
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker's apt repository.
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Allow your user to run Docker without `sudo`. The `docker` group grants root-level privileges on the host. Only add trusted users.

```bash
sudo groupadd docker
sudo usermod -aG docker "$USER"
newgrp docker
```

To test everything worked:

```bash
docker run --rm hello-world
```

To run a sample app:

```bash
sudo docker run --rm hello-world
```

## 2. kubectl

kubectl should generally be within one minor version of the Kubernetes cluster you will use. For local k3d clusters, installing the latest stable kubectl is normally fine.

Install:

```bash
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) KUBECTL_ARCH="amd64" ;;
  aarch64|arm64) KUBECTL_ARCH="arm64" ;;
  *) echo "Unsupported architecture: $ARCH" && exit 1 ;;
esac

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/${KUBECTL_ARCH}/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/${KUBECTL_ARCH}/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
rm kubectl.sha256
```

The [official Linux kubectl documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) also includes native package-manager setup for Debian-based, Red Hat-based, and SUSE-based distributions.

## 3. k3d

k3d requires Docker and kubectl. Make sure Docker is running before creating a cluster.

With Homebrew on Linux:

```bash
brew install k3d
k3d version
```

With the official install script:

```bash
curl -fsSL -o install-k3d.sh https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh
bash install-k3d.sh
k3d version
```

Create a cluster:

```bash
k3d cluster create dev
```

And test it with `kubectl`:

```bash
kubectl get nodes
```

## 4. Helm

The current upstream Helm documentation defaults to Helm 4. If your project explicitly requires Helm 3, use the [Helm 3 install documentation](https://helm.sh/docs/v3/intro/install/) or the `get-helm-3` script shown below.

Official Helm 4 script:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
chmod 700 get_helm.sh
./get_helm.sh
helm version
```

Helm 3 script, for projects that still require Helm 3:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
helm version
```

Debian/Ubuntu package repository:

```bash
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

Fedora:

```bash
sudo dnf install helm
```

Snap:

```bash
sudo snap install helm --classic
```

## End-to-end verification

Run this after all four tools are installed:

```bash
docker version
kubectl version --client
k3d version
helm version

k3d cluster create install-check
kubectl get nodes

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install install-check-nginx bitnami/nginx
kubectl get pods

helm uninstall install-check-nginx
k3d cluster delete install-check
```

## Troubleshooting

- `docker: command not found`: Docker CLI is not on `PATH`.
- `Cannot connect to the Docker daemon`: run `sudo systemctl start docker`, or start Docker Desktop if you use Desktop for Linux.
- Permission denied on `/var/run/docker.sock`: use `sudo docker ...`, add your user to the `docker` group, then log out and back in.
- `k3d` cannot create a cluster: confirm Docker is running with `docker version` and that your current Docker context is correct with `docker context ls`.
- `kubectl` says connection refused: no cluster is running, or the current kubeconfig context points at a cluster that is offline.
- `helm` cannot reach Kubernetes: verify `kubectl get nodes` works first.
