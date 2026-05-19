# Windows Install: Docker, kubectl, k3d, and Helm

Last checked: 2026-05-19.

Install these tools in this order:

1. Docker
2. kubectl
3. k3d
4. Helm

This guide assumes you are using PowerShell with Docker Desktop for Windows. If you prefer WSL2-native tooling, install Docker Desktop with WSL integration, then follow the Linux package instructions inside your WSL distribution where appropriate.

## Official documentation

| Tool | Documentation |
| --- | --- |
| Docker | [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) |
| kubectl | [Install kubectl on Windows](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/) |
| k3d | [k3d installation](https://k3d.io/stable/#installation) |
| Helm | [Install Helm](https://helm.sh/docs/intro/install/) |

## Prerequisites

- Use a Windows account with administrator rights for machine-wide installs.
- Use PowerShell for the commands below.
- Keep `docker`, `kubectl`, `k3d`, and `helm` on your `PATH`.
- Choose one shell environment for daily use. Avoid splitting some tools into Windows and others into WSL unless you intentionally know which Docker context each shell is using.

## 1. Docker

Recommended path: Docker Desktop with the WSL2 backend.

1. Enable or update WSL2 from an elevated PowerShell prompt:

   ```powershell
   wsl --install
   wsl --update
   wsl --version
   ```

   Reboot if Windows asks you to.

2. Download `Docker Desktop Installer.exe` from the [Docker Desktop for Windows documentation](https://docs.docker.com/desktop/setup/install/windows-install/).

3. Run the installer interactively and select the WSL2 backend when prompted, or install from PowerShell:

   ```powershell
   # Per-user install; administrator rights are not required.
   Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--user'

   # All-users install; run PowerShell as administrator.
   Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install'
   ```

4. If Docker Desktop was installed for all users by a different administrator account, add your user to the `docker-users` group:

   ```powershell
   net localgroup docker-users <your-windows-user> /add
   ```

5. Start Docker Desktop from the Start menu, accept the Docker terms, and wait until Docker reports that it is running.

6. Verify the install:

   ```powershell
   docker version
   docker run --rm hello-world
   ```

## 2. kubectl

kubectl should generally be within one minor version of the Kubernetes cluster you will use. For local k3d clusters, installing the latest stable kubectl is normally fine.

Use one package manager:

```powershell
winget install -e --id Kubernetes.kubectl
```

or:

```powershell
choco install kubernetes-cli
```

or:

```powershell
scoop install kubectl
```

If package managers are unavailable, install the binary manually. The example below downloads the latest stable `amd64` binary; replace `amd64` with `arm64` if needed.

```powershell
$KUBECTL_VERSION = (Invoke-WebRequest -UseBasicParsing https://dl.k8s.io/release/stable.txt).Content.Trim()
curl.exe -LO "https://dl.k8s.io/release/$KUBECTL_VERSION/bin/windows/amd64/kubectl.exe"
curl.exe -LO "https://dl.k8s.io/release/$KUBECTL_VERSION/bin/windows/amd64/kubectl.exe.sha256"
(Get-FileHash -Algorithm SHA256 .\kubectl.exe).Hash -eq (Get-Content .\kubectl.exe.sha256)
```

Move `kubectl.exe` into a folder on your `PATH`, then verify:

```powershell
kubectl version --client
kubectl version --client --output=yaml
```

Docker Desktop for Windows may also add a `kubectl` binary to `PATH`. If `kubectl version --client` reports an unexpected version, check your `PATH` ordering.

## 3. k3d

k3d requires Docker and kubectl. Make sure Docker Desktop is running before creating a cluster.

Install with Chocolatey:

```powershell
choco install k3d
```

or with Scoop:

```powershell
scoop install k3d
```

Verify:

```powershell
k3d version
docker version
```

Create and delete a test cluster:

```powershell
k3d cluster create dev
kubectl get nodes
k3d cluster delete dev
```

## 4. Helm

The current upstream Helm documentation defaults to Helm 4. If your project explicitly requires Helm 3, use the [Helm 3 install documentation](https://helm.sh/docs/v3/intro/install/).

Use one package manager:

```powershell
winget install Helm.Helm
```

or:

```powershell
choco install kubernetes-helm
```

or:

```powershell
scoop install helm
```

Verify:

```powershell
helm version
```

## End-to-end verification

Run this from PowerShell after all four tools are installed and Docker Desktop is running:

```powershell
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
- Unexpected `kubectl` version: Docker Desktop may have added its own `kubectl` earlier in `PATH`; adjust `PATH` ordering or use a fully qualified path.
