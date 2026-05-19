# Windows Install: Docker, kubectl, k3d, and Helm

Last checked: 2026-05-19.

Install these tools in this order:

1. Docker
2. kubectl
3. k3d
4. Helm

This guide uses Docker Engine inside an Ubuntu WSL2 distribution. Run the WSL setup commands from PowerShell, then run Docker, kubectl, k3d, and Helm commands inside Ubuntu.

## Official documentation

| Tool | Documentation |
| --- | --- |
| WSL | [Install WSL](https://learn.microsoft.com/windows/wsl/install) |
| Docker | [Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) |
| kubectl | [Install kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) |
| k3d | [k3d installation](https://k3d.io/stable/#installation) |
| Helm | [Install Helm](https://helm.sh/docs/intro/install/) |

## Prerequisites

- Use a Windows account with administrator rights to enable or update WSL.
- Use PowerShell only for WSL setup. Use the Ubuntu WSL shell for the tool installs and daily k3d work.
- Keep `docker`, `kubectl`, `k3d`, and `helm` on your Linux `PATH` inside WSL.
- Do not split these tools between Windows PowerShell and WSL unless you intentionally know which Docker socket and kubeconfig each shell is using.

## 1. Docker

Recommended path: Ubuntu on WSL2 with Docker Engine.

1. Enable or update WSL2 from an elevated PowerShell prompt:

   ```powershell
   wsl --install -d Ubuntu
   wsl --update
   wsl --version
   ```

   Reboot if Windows asks you to. Open Ubuntu from the Start menu and finish the Linux user setup.

2. In the Ubuntu WSL shell, add Docker's official package repository:

   ```bash
   sudo apt update
   sudo apt install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
   Types: deb
   URIs: https://download.docker.com/linux/ubuntu
   Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
   Components: stable
   Architectures: $(dpkg --print-architecture)
   Signed-By: /etc/apt/keyrings/docker.asc
   EOF

   sudo apt update
   ```

3. Install Docker Engine and plugins:

   ```bash
   sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

4. Start and verify Docker:

   ```bash
   sudo systemctl start docker
   sudo docker run --rm hello-world
   ```

5. Optional: allow your WSL user to run Docker without `sudo`.

   ```bash
   sudo groupadd docker
   sudo usermod -aG docker "$USER"
   newgrp docker
   docker run --rm hello-world
   ```

   The `docker` group grants root-level privileges inside the WSL distribution. Only add trusted users.

6. Verify the Docker client and daemon:

   ```bash
   docker version
   ```

## 2. kubectl

kubectl should generally be within one minor version of the Kubernetes cluster you will use. For local k3d clusters, installing the latest stable kubectl is normally fine.

Run these commands inside Ubuntu WSL:

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

Verify:

```bash
kubectl version --client --output=yaml
```

## 3. k3d

k3d requires Docker and kubectl. Make sure Docker Engine is running before creating a cluster.

Install with the official install script inside Ubuntu WSL:

```bash
curl -fsSL -o install-k3d.sh https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh
less install-k3d.sh
bash install-k3d.sh
k3d version
```

If you use Homebrew on Linux inside WSL, you can install k3d with:

```bash
brew install k3d
```

Verify:

```bash
k3d version
docker version
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

The current upstream Helm documentation defaults to Helm 4. If your project explicitly requires Helm 3, use the [Helm 3 install documentation](https://helm.sh/docs/v3/intro/install/).

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
helm version
```

## End-to-end verification

Run this from Ubuntu WSL after all four tools are installed and Docker Engine is running:

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

- `docker: command not found`: Docker CLI is not installed in the current WSL distribution or is not on `PATH`.
- `Cannot connect to the Docker daemon`: run `sudo systemctl start docker` inside Ubuntu WSL.
- Permission denied on `/var/run/docker.sock`: use `sudo docker ...`, or add your WSL user to the `docker` group and start a new shell.
- `systemctl` is unavailable: update WSL with `wsl --update`, restart WSL with `wsl --shutdown`, then reopen Ubuntu. If it is still unavailable, enable systemd in `/etc/wsl.conf`, restart WSL again, and retry `sudo systemctl start docker`.
- `k3d` cannot create a cluster: confirm Docker is running with `docker version`.
- `kubectl` says connection refused: no cluster is running, or the current kubeconfig context points at a cluster that is offline.
- `helm` cannot reach Kubernetes: verify `kubectl get nodes` works first.
