# Setting up the Cluster
Instructions based off those found in the [RKE2 Quick Start Guide](https://docs.rke2.io/install/quickstart)
## Sanity Checks
1: Make sure the server and the agent node can `ping` each other's ip address.

2: Sudo into the terminal by typing `sudo -s` - the install process and the `kubectl` command won't work without sudo access.

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

### 5: Copy the token from `/var/lib/rancher/rke2/server/node-token` to the agent node.


### 6: Move the `kubeconfig` file
Due to the way `rke2` is set up, the 'kubeconfig' file is in the wrong place. We need to move it to its proper place so we can use the 'kubectl' command. To do so, first open the bash file:
```
nano ~/.bashrc
```
Then, paste the following text into the file:
```
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml PATH=$PATH:/var/lib/rancher/rke2/bin
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
Replace `<server>` with the ip address of the server node's computer and paste the token from the server node.

### 4: Start the service:
```
systemctl start rke2-agent.service
```
### 5: Follow the logs in a serperate terminal:
```
journalctl -u rke2-agent -f
```

# How to Install the Apps
Guide on how to set up the PHP Guestbook and the camera
## PHP Guestbook
Follow [Deploying PHP Guestbook application with Redis](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/)

## Camera Deployment
1: Download the [cam2ip docker container](https://github.com/gen2brain/cam2ip) and confirm the camera is streaming to the ip address.

2: Restart the computer

3: Deploy the Dep.yaml file to run the camera on the cluster:
```
kubectl apply -f Dep.yaml
```

4: Find the camera ip address:
```
kubectl get services
```
5: Navigate to the camera stream:
```
<server node ip address>:<service ip address>
```
# Setting up the Image Attack
1: Make sure both the `Dockerfile` and `gpu_workload.py` files are in the same folder.

2: Build the docker image:
```
docker build -t hw .
```
This will set up an image called `hw`, which the GUI will run as part of the image attack. If you wish to change the name of the image, make sure to also change the image being called with the `docker run hw` command in the GUI.
