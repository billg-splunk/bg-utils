# macOS Install: Docker, kubectl, k3d, and Helm

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
| Docker | [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/) |
| kubectl | [Install kubectl on macOS](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/) |
| k3d | [k3d installation](https://k3d.io/stable/#installation) |
| Helm | [Install Helm](https://helm.sh/docs/intro/install/) |

## Prerequisites

- Use an account with `sudo` rights.
- Keep `docker`, `kubectl`, `k3d`, and `helm` on your `PATH`.
- Choose `arm64` downloads for Apple Silicon and `amd64` downloads for Intel.
- Homebrew is recommended for kubectl, k3d, and Helm, but manual install options are included where useful.

## 1. Docker

Recommended path: Docker Desktop.

1. Download the correct installer from the [Docker Desktop for Mac documentation](https://docs.docker.com/desktop/setup/install/mac-install/):
   - Apple Silicon: use the Apple Silicon build.
   - Intel: use the Intel build.

2. Install interactively by opening `Docker.dmg` and dragging `Docker.app` into Applications, or install from Terminal after downloading `Docker.dmg`:

   ```bash
   sudo hdiutil attach Docker.dmg
   sudo /Volumes/Docker/Docker.app/Contents/MacOS/install
   sudo hdiutil detach /Volumes/Docker
   open -a Docker
   ```

3. On Apple Silicon, install Rosetta 2 if Docker or optional CLI tools prompt for it:

   ```bash
   softwareupdate --install-rosetta
   ```

4. Verify the install:

   ```bash
   docker version
   docker run --rm hello-world
   ```

## 2. kubectl

kubectl should generally be within one minor version of the Kubernetes cluster you will use. For local k3d clusters, installing the latest stable kubectl is normally fine.

With Homebrew:

```bash
brew install kubectl
kubectl version --client
```

Homebrew also supports the package name `kubernetes-cli`:

```bash
brew install kubernetes-cli
```

Manual install:

```bash
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) KUBECTL_ARCH="amd64" ;;
  arm64|aarch64) KUBECTL_ARCH="arm64" ;;
  *) echo "Unsupported architecture: $ARCH" && exit 1 ;;
esac

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/${KUBECTL_ARCH}/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/${KUBECTL_ARCH}/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | shasum -a 256 --check
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
sudo chown root: /usr/local/bin/kubectl
kubectl version --client
rm kubectl.sha256
```

## 3. k3d

k3d requires Docker and kubectl. Make sure Docker Desktop is running before creating a cluster.

With Homebrew:

```bash
brew install k3d
k3d version
```

Without Homebrew, use the official install script:

```bash
curl -fsSL -o install-k3d.sh https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh
less install-k3d.sh
bash install-k3d.sh
k3d version
```

Create and delete a test cluster:

```bash
k3d cluster create dev
kubectl get nodes
k3d cluster delete dev
```

## 4. Helm

The current upstream Helm documentation defaults to Helm 4. If your project explicitly requires Helm 3, use the [Helm 3 install documentation](https://helm.sh/docs/v3/intro/install/) or the `get-helm-3` script from the Helm project.

With Homebrew:

```bash
brew install helm
helm version
```

Official Helm 4 script:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
chmod 700 get_helm.sh
./get_helm.sh
helm version
```

## End-to-end verification

Run this from Terminal after all four tools are installed and Docker Desktop is running:

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

- `docker: command not found`: Docker CLI is not on `PATH`, or Docker Desktop has not finished starting.
- `Cannot connect to the Docker daemon`: start Docker Desktop and wait until it reports that it is running.
- `k3d` cannot create a cluster: confirm Docker is running with `docker version`.
- `kubectl` says connection refused: no cluster is running, or the current kubeconfig context points at a cluster that is offline.
- `helm` cannot reach Kubernetes: verify `kubectl get nodes` works first.
- Apple Silicon binary issues: confirm you installed the `arm64` build where a tool offers architecture-specific downloads.
