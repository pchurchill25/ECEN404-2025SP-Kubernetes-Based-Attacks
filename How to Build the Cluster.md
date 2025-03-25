# Setting up the Cluster
Instructions based off those found in the [RKE2 Quick Start Guide](https://docs.rke2.io/install/quickstart)
## Sanity Checks
1: Make sure the server and the agent node can `ping` each other's ip address.

2: Sudo into the terminal by typing `sudo -s` and then entering the same password you used to log into `child3`

3: Make sure your computer is connected to the internet.
## Setting up the Server Node
### 1: Run the installer.
```
curl -sfL https://get.rke2.io | sh -
```
This installs `rke2-server.service` and `rke2`, the kubernetes distrubition we will be using.

### 2: Enable the service.
```
systemctl enable rke2-server.service
```

### 3: Start the service.
```
systemctl start rke2-server.service
```
This may take a few minutes.

### 4: Follow startup logs.
```
journalctl -u rke2-server -f
```
Make sure to run this on a seperate terminal so it doesn't interrupt the server node starting.

### 5: Copy the token to the agent node.


### 6: Move the `kubeconfig` file
Due to the way `rke2` is set up, the 'kubeconfig' file is in the wrong place. We need to move it to its proper place so we can use the 'kubectl' command. To do so, first open the bash file:
```
nano ~/.bashrc
```
Then, paste the following text into the file:
```

```
Restart the computer:
```
systemctl restart now
```
Gain `sudo` access again, then check that `kubectl` is properly set up:
```
kubectl config view
```
You should see a fully populated kubectl config file.
## Setting up the Agent Node
### 1: Run the installer.
```
curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE="agent" sh -
```
This installs `rke2-agent.service` and `rke2`
### 2: Enable the service:
```
systemctl enable rke2-agent.service
```
### 3: Configure the agent node:
```
mkdir -p /etc/rancher/rke2/
nano /etc/rancher/rke2/config.yaml
```
Paste the following text into the file:
```
server: https://<server>:9345
token: <token from server node>
```
Replace `<server>` with the ip address of the server node's computer.
