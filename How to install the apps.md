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
