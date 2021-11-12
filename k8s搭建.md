### minikube

#### Get Start

1. 安装

   ```shell
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
   sudo install minikube-darwin-amd64 /usr/local/bin/minikube
   ```

2. 启动

   ```shell
   $ minikube start
   😄  minikube v1.24.0 on Darwin 11.5.2
   🆕  Kubernetes 1.22.3 is now available. If you would like to upgrade, specify: --kubernetes-version=v1.22.3
   ✨  Using the docker driver based on existing profile
   👍  Starting control plane node minikube in cluster minikube
   🚜  Pulling base image ...
   💾  Downloading Kubernetes v1.21.2 preload ...
       > preloaded-images-k8s-v13-v1...: 343.39 MiB / 499.07 MiB  68.81% 1.41 MiB 
       > preloaded-images-k8s-v13-v1...: 343.42 MiB / 499.07 MiB  68.81% 1.41 MiB 
       > preloaded-images-k8s-v13-v1...: 499.07 MiB / 499.07 MiB  100.00% 1.07 MiB
   🔄  Restarting existing docker container for "minikube" ...
   🐳  Preparing Kubernetes v1.21.2 on Docker 20.10.7 ...
   🔎  Verifying Kubernetes components...
       ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
   🌟  Enabled addons: storage-provisioner, default-storageclass
   🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
   ```

3. 交互

   如果已经安装了kubectl,就可以直接使用kubectl访问集群了

   ```shell
   $ kubectl get po -A
   NAMESPACE              NAME                                         READY   STATUS    RESTARTS   AGE
   kube-system            coredns-558bd4d5db-jjh5r                     1/1     Running   1          108d
   kube-system            etcd-minikube                                1/1     Running   1          108d
   kube-system            kube-apiserver-minikube                      1/1     Running   2          108d
   kube-system            kube-controller-manager-minikube             1/1     Running   1          108d
   kube-system            kube-proxy-fc8h2                             1/1     Running   1          108d
   kube-system            kube-scheduler-minikube                      1/1     Running   1          108d
   kube-system            storage-provisioner                          1/1     Running   3          108d
   kubernetes-dashboard   dashboard-metrics-scraper-5594458c94-mvbm8   1/1     Running   0          4m43s
   kubernetes-dashboard   kubernetes-dashboard-654cf69797-8mgfh        1/1     Running   0          4m43s
   ```

   如果没有安装，则minikube可以帮你下载合适版本的kubectl

   ```shell
   $ minikube kubectl -- get po -A
   ```

   账号minikube之后，一些服务比如存储，并没有启动。我们需要打开

   ```shell
   $ minikube dashboard
   🔌  Enabling dashboard ...
       ▪ Using image kubernetesui/dashboard:v2.3.1
       ▪ Using image kubernetesui/metrics-scraper:v1.0.7
   🤔  Verifying dashboard health ...
   🚀  Launching proxy ...
   🤔  Verifying proxy health ...
   🎉  Opening http://127.0.0.1:63775/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...
   ```

   此时可以通过web炉具蓝旗打开管理面板：http://127.0.0.1:63775/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/

4. 部署应用

   创建一个sample部署并暴露出8080端口

   ```shell
   $ kubectl create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.4
   deployment.apps/hello-minikube created
   
   $ kubectl expose deployment hello-minikube --type=NodePort --port=8080
   service/hello-minikube exposed
   
   $ kubectl get services hello-minikube
   NAME             TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
   hello-minikube   NodePort   10.97.209.29   <none>        8080:31311/TCP   12s
   ```

   通过minikube启动浏览器去访问服务

   ```shell
   $ minikube service hello-minikube
   |-----------|----------------|-------------|---------------------------|
   | NAMESPACE |      NAME      | TARGET PORT |            URL            |
   |-----------|----------------|-------------|---------------------------|
   | default   | hello-minikube |        8080 | http://192.168.49.2:31311 |
   |-----------|----------------|-------------|---------------------------|
   🏃  Starting tunnel for service hello-minikube.
   |-----------|----------------|-------------|------------------------|
   | NAMESPACE |      NAME      | TARGET PORT |          URL           |
   |-----------|----------------|-------------|------------------------|
   | default   | hello-minikube |             | http://127.0.0.1:63931 |
   |-----------|----------------|-------------|------------------------|
   🎉  Opening service default/hello-minikube in default browser...
   ❗  Because you are using a Docker driver on darwin, the terminal needs to be open to run it.
   ```

   现在可以访问http://127.0.0.1:63931 

   ```
   CLIENT VALUES:
   client_address=172.17.0.1
   command=GET
   real path=/
   query=nil
   request_version=1.1
   request_uri=http://127.0.0.1:8080/
   
   SERVER VALUES:
   server_version=nginx: 1.10.0 - lua: 10001
   
   HEADERS RECEIVED:
   accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
   accept-encoding=gzip, deflate, br
   accept-language=en-US,en;q=0.9
   connection=keep-alive
   cookie=_ga=GA1.1.596239993.1633627142
   host=127.0.0.1:63931
   sec-ch-ua="Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"
   sec-ch-ua-mobile=?0
   sec-ch-ua-platform="macOS"
   sec-fetch-dest=document
   sec-fetch-mode=navigate
   sec-fetch-site=none
   sec-fetch-user=?1
   upgrade-insecure-requests=1
   user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
   BODY:
   -no body in request-
   ```

   

   我们可以通过kubectl配置端口转发，让外部通过7080端口访问pod的8080端口。

   ```shell
   $ kubectl port-forward service/hello-minikube 7080:8080
   ```

   此时我们可以通过http://127.0.0.1:7080/来访问8080端口服务

   

   `LoadBalancer部署`

   ```SHELL
   $ kubectl create deployment balanced --image=k8s.gcr.io/echoserver:1.4  
   $ kubectl expose deployment balanced --type=LoadBalancer --port=8080
   ```

   打开一个新窗口，执行

   ```shell
   $ minikube tunnel
   ```

   使用下面命令获得可路由的ip

   ```shell
   $ kubectl get services balanced
   ```

   现在我们部署的程序就可以在 <EXTERNAL-IP>:8080上访问了

   

5. 管理集群

   暂停kuernetes，但不要影响已经部署的应用

   ```shell
   $ minikube pause
   ```

   恢复kubernetes

   ```shell
   $ minikube unpause
   ```

   

   终止kubernetes

   ```shell
   $ minikube stop
   ```

   

   提高默认内存上限，需要重启

   ```shell
   $ minikube config set memory 16384
   ```

   罗列已经安装的kubernete服务

   ```shell
   $ minikube addons list
   |-----------------------------|----------|--------------|-----------------------|
   |         ADDON NAME          | PROFILE  |    STATUS    |      MAINTAINER       |
   |-----------------------------|----------|--------------|-----------------------|
   | ambassador                  | minikube | disabled     | unknown (third-party) |
   | auto-pause                  | minikube | disabled     | google                |
   | csi-hostpath-driver         | minikube | disabled     | kubernetes            |
   | dashboard                   | minikube | enabled ✅   | kubernetes            |
   | default-storageclass        | minikube | enabled ✅   | kubernetes            |
   | efk                         | minikube | disabled     | unknown (third-party) |
   | freshpod                    | minikube | disabled     | google                |
   | gcp-auth                    | minikube | disabled     | google                |
   | gvisor                      | minikube | disabled     | google                |
   | helm-tiller                 | minikube | disabled     | unknown (third-party) |
   | ingress                     | minikube | disabled     | unknown (third-party) |
   | ingress-dns                 | minikube | disabled     | unknown (third-party) |
   | istio                       | minikube | disabled     | unknown (third-party) |
   | istio-provisioner           | minikube | disabled     | unknown (third-party) |
   | kubevirt                    | minikube | disabled     | unknown (third-party) |
   | logviewer                   | minikube | disabled     | google                |
   | metallb                     | minikube | disabled     | unknown (third-party) |
   | metrics-server              | minikube | disabled     | kubernetes            |
   | nvidia-driver-installer     | minikube | disabled     | google                |
   | nvidia-gpu-device-plugin    | minikube | disabled     | unknown (third-party) |
   | olm                         | minikube | disabled     | unknown (third-party) |
   | pod-security-policy         | minikube | disabled     | unknown (third-party) |
   | portainer                   | minikube | disabled     | portainer.io          |
   | registry                    | minikube | disabled     | google                |
   | registry-aliases            | minikube | disabled     | unknown (third-party) |
   | registry-creds              | minikube | disabled     | unknown (third-party) |
   | storage-provisioner         | minikube | enabled ✅   | kubernetes            |
   | storage-provisioner-gluster | minikube | disabled     | unknown (third-party) |
   | volumesnapshots             | minikube | disabled     | kubernetes            |
   |-----------------------------|----------|--------------|-----------------------|
   ```

   

   创建第二个cluster，运行指定版本的k8s

   ```shell
   $ minikube start -p aged --kubernetes-version=v1.16.1
   ```

   

   删除所有的sluster

   ```shell
   $ minikube delete --all
   ```

   

6. 是

