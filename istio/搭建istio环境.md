### 搭建istio环境.md



linux

```shell
# 安装ssh server
$ yum install -y openssl openssh-server

# 安装桌面
$ yum -y groups install "GNOME Desktop"
$ startx 

# 关闭防火墙
$ systemctl stop firewalld.service
$ systemctl disable firewalld.service 
```



安装docker

```shell
$ curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun

$ systemctl daemon-reload
$ systemctl enable docker.service
$ systemctl start docker.service

$ sudo docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

# 此时docker ps需要sudo，把当前用户加入docker用户组即可
$ groupadd docker
$ sudo gpasswd -a shyandsy docker
$ newgrp docker

# 重启
$ systemctl restart docker

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```



安装minikube

```shell
# 下载
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# 安装
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 启动minikube报错， 解决：按照上一段把当前用户加入docker组，避免docker命令需要sudo即可
$ minikube start
* minikube v1.25.1 on Centos 7.9.2009
* Unable to pick a default driver. Here is what was considered, in preference order:
  - docker: Not healthy: "docker version --format {{.Server.Os}}-{{.Server.Version}}" exit status 1: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/version": dial unix /var/run/docker.sock: connect: permission denied
  - docker: Suggestion: Add your user to the 'docker' group: 'sudo usermod -aG docker $USER && newgrp docker' <https://docs.docker.com/engine/install/linux-postinstall/>
* Alternatively you could install one of these drivers:
  - kvm2: Not installed: exec: "virsh": executable file not found in $PATH
  - vmware: Not installed: exec: "docker-machine-driver-vmware": executable file not found in $PATH
  - podman: Not installed: exec: "podman": executable file not found in $PATH
  - virtualbox: Not installed: unable to find VBoxManage in $PATH

X Exiting due to DRV_NOT_HEALTHY: Found driver(s) but none were healthy. See above for suggestions how to fix installed drivers.

# 启动minikube报错， 解决：关闭虚拟机，cpu调成2
$ minikube start
* minikube v1.25.1 on Centos 7.9.2009
* Automatically selected the docker driver. Other choices: none, ssh

X Exiting due to RSRC_INSUFFICIENT_CORES: Requested cpu count 2 is greater than the available cpus of 1


# 启动成功： 使用杭州镜像
$  minikube start --image-mirror-country cn \
--iso-url=https://kubernetes.oss-cn-hangzhou.aliyuncs.com/minikube/iso/minikube-v1.12.1.iso \ 
--registry-mirror=https://fgi18ddn.mirror.aliyuncs.com \ 
--vm-driver=none
* minikube v1.25.1 on Centos 7.9.2009
* Using the docker driver based on existing profile
* Starting control plane node minikube in cluster minikube
* Pulling base image ...
* Restarting existing docker container for "minikube" ...
! This container is having trouble accessing https://k8s.gcr.io
* To pull new external images, you may need to configure a proxy: https://miniku                                    be.sigs.k8s.io/docs/reference/networking/proxy/
* Preparing Kubernetes v1.23.1 on Docker 20.10.12 ...
  - kubelet.housekeeping-interval=5m
  - Generating certificates and keys ...
  - Booting up control plane ...
  - Configuring RBAC rules ...
* Verifying Kubernetes components...
  - Using image kubernetesui/metrics-scraper:v1.0.7
  - Using image kubernetesui/dashboard:v2.3.1
  - Using image gcr.io/k8s-minikube/storage-provisioner:v5
* Enabled addons: default-storageclass, storage-provisioner, dashboard
* Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

```



 安装kubectl

```shell
# 下载最新版本
$ url -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# 下载指定版本
curl -LO https://dl.k8s.io/release/v1.23.0/bin/linux/amd64/kubectl

# 安装
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# 设置alias
$ sudo vim /etc/rc.local
alias k='kubectl'
$ sudo -s source /etc/rc.local
```



#### k8s问题解决

外部访问虚拟机里的k8s

```shell
# 方法1：关闭防火墙
$ systemctl stop firewalld.service            #停止firewall
$ systemctl disable firewalld.service        #禁止firewall开机启动

# 方法2：防火墙放行
$ firewall-cmd --zone=public --add-port=8081/tcp --permanent

# 暴露到公网
$ kubectl proxy --address='0.0.0.0' --disable-filter=true
W0220 03:16:53.025770  129466 proxy.go:175] Request filter disabled, your proxy is vulnerable to XSRF attacks, please be cautious
Starting to serve on [::]:8001
E0220 03:16:56.806835  129466 proxy_server.go:147] Error while proxying request: context canceled


# 访问
http://192.168.37.55:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/pod?namespace=default
```



18690400309



mac系统上该用hyperkit

```shell
$ minikube start --vm-driver=hyperkit

$ minikube ip
192.168.64.2

$ sudo vim /etc/hosts
加入
192.168.64.2 shyandsy.com
```



#### helm



```shell
# 方法1： 要翻墙
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3

# 方法2：华为云国内镜像
$ wget https://mirrors.huaweicloud.com/helm/v3.7.2/helm-v3.7.2-linux-amd64.tar.gz 
$ tar -zxvf helm-v3.7.2-linux-amd64.tar.gz
$ sudo mv linux-amd64/helm /usr/local/bin/

$ helm version
version.BuildInfo{Version:"v3.7.2", GitCommit:"663a896f4a815053445eec4153677ddc24a0a361", GitTreeState:"clean", GoVersion:"go1.16.10"}

```



#### 安装istio

```shell
$ wget https://github.com/istio/istio/releases/download/1.13.0/istio-1.13.0-linux-amd64.tar.gz
--2022-02-20 04:51:19--  https://github.com/istio/istio/releases/download/1.13.0/istio-1.13.0-linux-amd64.tar.gz
Resolving github.com (github.com)... 140.82.112.3
Connecting to github.com (github.com)|140.82.112.3|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://objects.githubusercontent.com/github-production-release-asset-2e65be/74175805/05aba4d8-e2a8-41ed-98fa-cdc02c44d559?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220220%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220220T095120Z&X-Amz-Expires=300&X-Amz-Signature=e906a42d02652b7c14bc473676dd56c731ef89ca78bc43329772f188a9071e02&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=74175805&response-content-disposition=attachment%3B%20filename%3Distio-1.13.0-linux-amd64.tar.gz&response-content-type=application%2Foctet-stream [following]
--2022-02-20 04:51:20--  https://objects.githubusercontent.com/github-production-release-asset-2e65be/74175805/05aba4d8-e2a8-41ed-98fa-cdc02c44d559?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220220%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220220T095120Z&X-Amz-Expires=300&X-Amz-Signature=e906a42d02652b7c14bc473676dd56c731ef89ca78bc43329772f188a9071e02&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=74175805&response-content-disposition=attachment%3B%20filename%3Distio-1.13.0-linux-amd64.tar.gz&response-content-type=application%2Foctet-stream
Resolving objects.githubusercontent.com (objects.githubusercontent.com)... 185.199.111.133, 185.199.110.133, 185.199.108.133, ...
Connecting to objects.githubusercontent.com (objects.githubusercontent.com)|185.199.111.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 24860503 (24M) [application/octet-stream]
Saving to: ‘istio-1.13.0-linux-amd64.tar.gz’

100%[========================================================================================================>] 24,860,503  9.38MB/s   in 2.5s

2022-02-20 04:51:24 (9.38 MB/s) - ‘istio-1.13.0-linux-amd64.tar.gz’ saved [24860503/24860503]

$ tar xzvf istio-1.13.0-linux-amd64.tar.gz

# 查看istio目录结构
$ ll istio-1.13.0
total 28
drwxr-x---.  2 shyandsy docker    22 Feb 10 12:36 bin
-rw-r--r--.  1 shyandsy docker 11348 Feb 10 12:36 LICENSE
drwxr-xr-x.  5 shyandsy docker    52 Feb 10 12:36 manifests
-rw-r-----.  1 shyandsy docker   845 Feb 10 12:36 manifest.yaml
-rw-r--r--.  1 shyandsy docker  5866 Feb 10 12:36 README.md
drwxr-xr-x. 23 shyandsy docker  4096 Feb 10 12:36 samples
drwxr-xr-x.  3 shyandsy docker    57 Feb 10 12:36 tools

# 拷贝
sudo mv bin/istioctl /usr/local/bin/

# 安装
istioctl install --set profile=demo -y
✔ Istio core installed
✔ Istiod installed
✔ Egress gateways installed
✔ Ingress gateways installed
✔ Installation complete                                                                                     Making this installation the default for injection and validation.

Thank you for installing Istio 1.13.  Please take a few minutes to tell us about your install/upgrade experience!  https://forms.gle/pzWZpAvMVBecaQ9h9

# 标记默认wordpress-release默认注入sidecar
$ kubectl label namespace default istio-injection=enabled
```



### 安装sample程序

```shell
$ k apply -f samples/bookinfo/platform/kube/bookinfo.yaml -n wordpress-release
service/details created
serviceaccount/bookinfo-details created
deployment.apps/details-v1 created
service/ratings created
serviceaccount/bookinfo-ratings created
deployment.apps/ratings-v1 created
service/reviews created
serviceaccount/bookinfo-reviews created
deployment.apps/reviews-v1 created
deployment.apps/reviews-v2 created
deployment.apps/reviews-v3 created
service/productpage created
serviceaccount/bookinfo-productpage created
deployment.apps/productpage-v1 created


$ k -n wordpress-release get pods
NAME                              READY   STATUS            RESTARTS   AGE
details-v1-5498c86cf5-7t6fp       0/2     PodInitializing   0          11s
productpage-v1-65b75f6885-m6tsf   0/2     PodInitializing   0          11s
ratings-v1-b477cf6cf-mmgj7        0/2     PodInitializing   0          11s
reviews-v1-79d546878f-5mps5       0/2     PodInitializing   0          11s
reviews-v2-548c57f459-rc2ph       0/2     PodInitializing   0          11s
reviews-v3-6dd79655b9-f7mzm       0/2     PodInitializing   0          11s
wordpress-fdbd54b87-rmnjt         1/1     Running           0          126m
wordpress-mariadb-0               1/1     Running           0          126m

$ k get service -n wordpress-release
NAME                TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
details             ClusterIP      10.98.0.127      <none>        9080/TCP                     105s
productpage         ClusterIP      10.103.56.193    <none>        9080/TCP                     105s
ratings             ClusterIP      10.103.102.119   <none>        9080/TCP                     105s
reviews             ClusterIP      10.103.198.201   <none>        9080/TCP                     105s
wordpress           LoadBalancer   10.96.219.115    <pending>     80:31628/TCP,443:31941/TCP   128m
wordpress-mariadb   ClusterIP      10.109.11.156    <none>        3306/TCP                     128m


# 验证
$ k exec "$(k get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"


$ k scale deployment productpage-v1  --replicas=0 -n wordpress-release
$ k scale deployment productpage-v1  --replicas=1 -n wordpress-release
```



