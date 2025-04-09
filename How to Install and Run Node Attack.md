# Step 1: Create Configuration files
1a) After opening the terminal, allow access through `sudo -s` and by typing in the appropriate password.

1b) Locate the appropriate file that you wish to store and run configuration file out of. For us, it was PyCharm Projects.

1c) Type `nano api-dos-deployment.yaml` and enter. This will create a blank file. You may need to install nano command if it is not already installed.

1d) Copy and paste `api-dos-deployment.yaml` from this repository into the blank file. Press `Ctrl X`, then press `Y`, then press `Enter`. You have now succesfully configured this file.

# Step 2: Running the Attack
2a) On the terminal line, run the script `kubectl apply -f api-dos-deployment.yaml`. The terminal should respond with `api attacker pods configured`.

2b) You can scale the attack by running the script `kubectl scale deployment api-dos-deployment --replicas=40` The `40` is just an example of a number that you can increase the pod count to.

2c) At some point, the targeted node will crash and you will have to physically reboot it. It will send an electronic message by changing the status of the targeted node from `Ready` to `Not Ready`.


# Step 3: Monitoring the Attack
3a) As the attack is running, type in `kubectl top nodes` to view the increase in memory and CPU usage on the appropriate node.

3b) In a seperate tab, sudo access in and install `k9s`. It is a very simple program that will show the pod count, as well as node usage and other information.

3c) After installation, type `k9s` into the terminal and press Enter. This will allow the window to pop up. 

3d) You can also run `get pods -o wide` to see the status of the pods and what node that are running on. This is helpful for debugging. 


# Step 4: Deleting the Attack
4a) Run `kubectl delete deployment api-dos-deployment` to delete the attack. You cna view from `kubectl top nodes` or `k9s` as the pod count and overall node usage drops accordingly. 

4b) This will not delete the configuration file. However, it will just terminate the current active pods and therefore restore the nodes back to their orginial usage levels. 
