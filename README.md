# Kubernetes Based Attacks
## Overview
Kubernetes Based Attacks is a senior design project that simulates a Kubernetes cluster and allows users to run attacks on the cluster via a GUI. There are three different kinds of attacks implemented in the GUI: an Image attack, a Node attack, and a Pod attack. 
### Cluster Overview
The cluster consists of a server node running on child3 and an agent node running on child2. The cluster has a [PHP Guestbook](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/) and a camera feed running on it as well.
### Image Attack
The image attack simulates a cryptominer being installed on the computer via malicous image download by forcing the computer to multiply large matricies.
### Node Attack
The node attack involves deploying a large number of API-DoS-Deployment pods to stress the RKE2 cluster’s API server. From the server node, the attack infinitely sends pods containing small requests to the agent node. This attack quickly increases CPU and memory usage, crashing the agent node.
### Pod Attack
The pod attack vector consists of a simple attack vector consisting of a bash script that spam creates images that consume high amounts of CPU power. During this process, the attack script is capable of consuming over 90 percent of the host computer’s CPU power.
## Opening the GUI
1. Log into the `child3` profile on the child3 computer, not the `gcri_nasa` profile.

2. Open up the terminal by pressing `Ctrl+Alt+T` or by clicking the icon in the top left.

3. Sudo into the terminal by typing `sudo -s` and then enter the same password you used to login to `child3`

4. Run this command to open the GUI:
```
cd PyCharmMiscProject && python3 GUI.py
```
# Using the GUI
The GUI consists of eight buttons, a command line input, and a terminal output window.
### Run
When pressed, this button will run the typed command in the CLI.
### Start TCPDump
Begins collecting packet capture data, storing it in a file with the name specified in the **Enter Filename** textbox. 
### Stop TCPDump
Stops the packet capture data and moves the file to the `Downloads` folder.
### Run/Stop Image Attack
Starts the image attack by calling the malicious image. The image will run, consuming roughly 85% of the CPU.
### Run Node Attack
Deploys the node attack yaml, which will eventaully crash the agent node.
### Delete Node Attack
Deletes the node attack yaml.
### Run Pod Attack
Executes the pod attack, which will spam containers to consume CPU and memory and slow the system down. The button is a toggle-style switch so pressing the same button again after execution will stop the pod attack.
### Show Kubectl Top Nodes
Shows the output of the `kubectl top nodes` command, which displays nodes in the cluster and their CPU usage. Use to check if attacks are running properly.
## Filename
Enter the filename for the .pcap file, without the .pcap.
## Terminal Command
Enter the command to run when the **Run** button is pressed.
## Terminal Output
Displays the output for the terminal command.

