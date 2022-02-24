### helm部署python dash数据报表服务



#### 结构

- 搭建一个简单的python dash服务
- 使用docker构建服务并启动运行
- 搭建本地k8s minikube环境
- 搭建本地docker registry做为k8s的镜像
- 本地镜像上传到docker hub
- 使用helm将dash服务部署到k8s环境中并运行



#### 搭建一个简单的python dash服务

程序目录结构

```
+-- Dockerfile
+-- requirements.txt
+-- app
|   +-- __init__.py
|   +-- app.py
```



app.py内容

```python
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://[your-ip-or-domain-name]:8080/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server  # <== ADD THIS LINE
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(
    df,
    x="Fruit", y="Amount", color="City", barmode="group"
)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python. Customized right here!
    '''),  # <== ADDED SOME TEXT HERE

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    # app.run_server(debug=True)  # <== THIS MAY NOT DEPLOY
    # USE DIFFERENT ARGUMENTS FOR run_server METHOD
    app.run_server(debug=True, host='0.0.0.0', port=8080)
```



requirements.txt

```
dash
gunicorn
pandas
plotly
```



Dockerfile

```dockerfile
FROM python:3.9-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
CMD gunicorn -b 0.0.0.0:80 app.app:server
```



启动运行，访问：http://127.0.0.1:8080/

```shell
$ docker run -p 8080:80 tiny_home
```



#### 使用docker构建服务并启动运行

构建docker镜像

```shell
$ docker build -t tiny_home .
```



查看docker镜像

```shell
$ docker images
REPOSITORY		TAG          IMAGE ID       CREATED          SIZE
tiny_home     latest       9ab89872bd30   18 minutes ago   479MB
```



启动docker

```shell
$ docker run -p 8080:80 tiny_home
[2022-02-14 13:53:35 +0000] [7] [INFO] Starting gunicorn 20.1.0
[2022-02-14 13:53:35 +0000] [7] [INFO] Listening at: http://0.0.0.0:80 (7)
[2022-02-14 13:53:35 +0000] [7] [INFO] Using worker: sync
[2022-02-14 13:53:35 +0000] [8] [INFO] Booting worker with pid: 8
```



本机访问dash表格

http://127.0.0.1:8080/



#### 搭建本地k8s minikube环境

安装minikube：https://minikube.sigs.k8s.io/docs/start/



选择mac环境，x86

```shell
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```



启动cluster

```shell
$ minikube start
😄  minikube v1.24.0 on Darwin 11.5.2
🆕  Kubernetes 1.22.3 is now available. If you would like to upgrade, specify: --kubernetes-version=v1.22.3
🎉  minikube 1.25.1 is available! Download it: https://github.com/kubernetes/minikube/releases/tag/v1.25.1
💡  To disable this notice, run: 'minikube config set WantUpdateNotification false'

✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.21.2 on Docker 20.10.7 ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
    ▪ Using image kubernetesui/dashboard:v2.3.1
    ▪ Using image kubernetesui/metrics-scraper:v1.0.7
🌟  Enabled addons: storage-provisioner, default-storageclass, dashboard
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```



查看pod，可以看到相关服务都已经启动

```shell
$ k get po -A
NAMESPACE              NAME                                         READY   STATUS    RESTARTS   AGE
default                hello-minikube-6ddfcc9757-t8s8d              1/1     Running   2          95d
kube-system            coredns-558bd4d5db-jjh5r                     1/1     Running   2          203d
kube-system            etcd-minikube                                1/1     Running   2          203d
kube-system            kube-apiserver-minikube                      1/1     Running   3          203d
kube-system            kube-controller-manager-minikube             1/1     Running   2          203d
kube-system            kube-proxy-fc8h2                             1/1     Running   2          203d
kube-system            kube-scheduler-minikube                      1/1     Running   2          203d
kube-system            storage-provisioner                          1/1     Running   24         203d
kubernetes-dashboard   dashboard-metrics-scraper-5594458c94-mvbm8   1/1     Running   2          95d
kubernetes-dashboard   kubernetes-dashboard-654cf69797-8mgfh        1/1     Running   2          95d
```



浏览器中打开仪表盘

```shell
$ minikube dashboard

$ minikube dashboard --url
```



查看

```shell
$ k get deployment
$ k get pods
$ k get events
$ k get config view
```



```shell
minikube service hello-minikube
```



### 搭建本地docker registry做为k8s的镜像

https://yeasy.gitbook.io/docker_practice/repository/registry

安装

```shell
$ docker pull registry

$ docker images
REPOSITORY                                                   TAG          IMAGE ID       CREATED        SIZE
jenkins/jenkins                                              lts          2219cea3096b   7 days ago     441MB
registry                                                     latest       b2cb11db9d3d   2 months ago   26.2MB
```



docker镜像删除后会把所有的数据和文件都删除，所以要把主机的本地目录挂在到registry容器内部目录上，在删除registry后依旧能保证文件和数据不丢失。

```shell
$ mkdir -p ~/docker/data/registry

$ cd ~/docker/data/registry/

$ pwd
/Users/yshi3/docker/data/registry			# 数据文件夹
```



创建registry镜像容器，绑定5000端口

```shell
# 创建自定义网络
$ docker network create --subnet=192.168.1.0/24 my_docker_net
d1becb433c982fe847987ba1c6f87c6c3dfe8ebd55a93c16ff568b6a0c06488e

# 查看docker网络
$docker network ls
NETWORK ID     NAME                    DRIVER    SCOPE
693443dafdb6   bridge                  bridge    local
e2fd0da2937c   docker_gwbridge         bridge    local
c7168f0810f5   host                    host      local
yrnfdjn5tozh   ingress                 overlay   swarm
87950b58ee6b   kafka_default           bridge    local
e6ee4817a4e1   minikube                bridge    local
127e542803a4   mos-db-docker_default   bridge    local
d1becb433c98   my_docker_net           bridge    local 					<------ 创建好了
aa40e7d3513b   none                    null      local
e1f5f9171762   redis_default           bridge    local
2926897b9218   redis_node_net          bridge    local

# 在自定义网络my_docker_net上创建registry，ip地址：192.168.1.100
$ docker run -d --name registry --network my_docker_net --ip 192.168.1.100 -p 5000:5000 --restart=always -v /Users/yshi3/docker/data/registry:/var/lib/registry registry:latest
dcfaa1c3b1459c7e4c3c5d152aecf9c43863ede6b957e642e9633eb9bb430e31

# 不实用私有ip
docker run -d --name registry -p 5000:5000 --restart=always -v /Users/yshi3/docker/data/registry:/var/lib/registry registry:latest

$ docker ps
CONTAINER ID   IMAGE						COMMAND									CREATED					STATUS				PORTS				NAMES
d7441c61c28d   registry:latest	"/entrypoint.sh /etc…"	13 seconds ago	Up 12 seconds	0.0.0....		registry

$ netstat -ant | grep 5000 
tcp46      0      0  *.5000                 *.*                    LISTEN
```



为registry创建用户名密码

```shell
$ mkdir  /Users/yshi3/docker/data/registry/auth

$ docker run --entrypoint htpasswd registry:latest -Bbn felix felix  >> /Users/yshi3/docker/data/registry/auth/htpasswd
docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting container process caused: exec: "htpasswd": executable file not found in $PATH: unknown.

# 错误解决

```



好了现在5000端口就是我们的私有docker hub了



#### 本地镜像上传到docker hub

登陆本地docker registry

```shell
$ docker login 172.17.0.3:5000
```



查看本地docker image

```shell
$ docker image ls
REPOSITORY		TAG          IMAGE ID       CREATED         SIZE
tiny_home			latest       9ab89872bd30   2 hours ago     479MB
```



使用tag命令标记，格式：docker tag IMAGE[:TAG] [REGISTRY_HOST[:REGISTRY_PORT]/]REPOSITORY[:TAG]

```shell
# 打标记
$ docker tag tiny_home:latest 192.168.1.100:5000/tiny_home:latest

# 查看
$ docker image ls
REPOSITORY                                                   TAG          IMAGE ID       CREATED         SIZE
127.0.0.1:5000/tiny_home                                     latest       9ab89872bd30   2 hours ago     479MB
tiny_home                                                    latest       9ab89872bd30   2 hours ago     479MB
```



推送到本机docker registry

```shell
$ docker push 192.168.1.100:5000/tiny_home:latest
The push refers to repository [127.0.0.1:5000/tiny_home]
2cb794266e37: Pushed 
0a7fc7d215e9: Pushed 
a33b36620252: Pushed 
bd2446141b44: Pushed 
fa5abdc28024: Pushed 
65bc0c77c48f: Pushed 
32034715e5d4: Pushed 
7d0ebbe3f5d2: Pushed 
latest: digest: sha256:a3070915763b829208830ba5061d064a84b5f1fed7b284402565377aa0dd8169 size: 1998
```



推送到公共docker hub

```shell
# 登陆docker hub
$ docker login
# 创建tag，必须以docker hub用户名开头： 否则会报错 denied: requested access to the resource is denied
$ docker tag tiny_home:latest shyandsy/tiny_home
# 推送
$ docker push shyandsy/tiny_home
Using default tag: latest
The push refers to repository [docker.io/shyandsy/tiny_home]
2cb794266e37: Pushed 
0a7fc7d215e9: Pushed 
a33b36620252: Pushed 
bd2446141b44: Pushed 
fa5abdc28024: Pushed 
65bc0c77c48f: Pushed 
32034715e5d4: Pushed 
7d0ebbe3f5d2: Pushed 
latest: digest: sha256:a3070915763b829208830ba5061d064a84b5f1fed7b284402565377aa0dd8169 size: 1998
```



查看docker registry中的镜像

```shell
# 命令行curl
$ curl 127.0.0.1:5000/v2/_catalog
{"repositories":["tiny_home"]}

# 浏览器
http://127.0.0.1:5000/v2/_catalog
```



删除本地镜像，在从docker registry里拉下image

```shell
# 删除本地127.0.0.1:5000/tiny_home:latest
$ docker image rm 127.0.0.1:5000/tiny_home:latest

# 查看本地，没有：127.0.0.1:5000/tiny_home:latest
$ docker image ls 
REPOSITORY								TAG          IMAGE ID       CREATED         SIZE
tiny_home									latest       9ab89872bd30   2 hours ago     479MB

# 重新拉下来
$ docker pull 127.0.0.1:5000/tiny_home:latest
latest: Pulling from tiny_home
Digest: sha256:a3070915763b829208830ba5061d064a84b5f1fed7b284402565377aa0dd8169
Status: Downloaded newer image for 127.0.0.1:5000/tiny_home:latest
127.0.0.1:5000/tiny_home:latest

# 再次查看，有了
$ docker image ls
REPOSITORY								TAG          IMAGE ID       CREATED         SIZE
127.0.0.1:5000/tiny_home	latest       9ab89872bd30   2 hours ago     479MB
tiny_home									latest       9ab89872bd30   2 hours ago     479MB
```



#### 使用helm将dash服务部署到k8s环境中并运行



创建pod deployment，hello-node。无法访问本地docker registry

```shell
# 创建pod的deployment
$ k create deployment hello-node --image=127.0.0.1:5000/tiny_home:latest
deployment.apps/hello-node created

# 查看deployments：看到READY 0/1
$ k get deployments
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
hello-minikube   1/1     1            1           95d
hello-node       0/1     1            0           31s

# 查看pod：看到状态ImagePullBackOff
$ k get pods
NAME                              READY   STATUS             RESTARTS   AGE
hello-minikube-6ddfcc9757-t8s8d   1/1     Running            2          95d
hello-node-85dffbd7bb-mr4bw       0/1     ImagePullBackOff   0          2m54

# 查看event：可以看到failed to pull image
$ k get events
LAST SEEN   TYPE      REASON              OBJECT                             MESSAGE
7m17s       Normal    Scheduled           pod/hello-node-85dffbd7bb-mr4bw    Successfully assigned default/hello-node-85dffbd7bb-mr4bw to minikube
5m49s       Normal    Pulling             pod/hello-node-85dffbd7bb-mr4bw    Pulling image "127.0.0.1:5000/tiny_home:latest"
5m49s       Warning   Failed              pod/hello-node-85dffbd7bb-mr4bw    Failed to pull image "127.0.0.1:5000/tiny_home:latest": rpc error: code = Unknown desc = Error response from daemon: Get http://127.0.0.1:5000/v2/: dial tcp 127.0.0.1:5000: connect: connection refused
5m49s       Warning   Failed              pod/hello-node-85dffbd7bb-mr4bw    Error: ErrImagePull
2m8s        Normal    BackOff             pod/hello-node-85dffbd7bb-mr4bw    Back-off pulling image "127.0.0.1:5000/tiny_home:latest"
5m38s       Warning   Failed              pod/hello-node-85dffbd7bb-mr4bw    Error: ImagePullBackOff
7m17s       Normal    SuccessfulCreate    replicaset/hello-node-85dffbd7bb   Created pod: hello-node-85dffbd7bb-mr4bw
7m17s       Normal    ScalingReplicaSet   deployment/hello-node              Scaled up replica set hello-node-85dffbd7bb to 1


创建deploy失败！！！！

# 删除
$ k delete deploy/hello-node
$ k delete pod/hello-node-85dffbd7bb-mr4bw

# 验证删除
$ k get deployments                                                           
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
hello-minikube   1/1     1            1           95d
$ k get pods                              
NAME                              READY   STATUS    RESTARTS   AGE
hello-minikube-6ddfcc9757-t8s8d   1/1     Running   2          95d
```



使用docker hub

```shell
# 使用docker hub创建
$ k create deployment hello-node --image=docker.io/shyandsy/tiny_home
```



默认创建的pod只能通过集群内IP访问，需要创建service将内部pod暴露给公网

```shell
# 创建service
$ k expose deployment hello-node --type=LoadBalancer --port=8080
service/hello-node exposed

# 查看service
$ k get services                                                      
NAME             TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
hello-node       LoadBalancer   10.98.65.97    <pending>     8080:32077/TCP   4s
```





helm的repo操作

```shell
# 查看仓库
$ helm repo ls
NAME   	URL                               
bitnami	https://charts.bitnami.com/bitnami

$ helm repo add bitnami https://charts.bitnami.com/bitnami

```



查看应用

```shell
# 查看已经部署的应用
$ helm list
NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION


```



创建helm chart

```shell
# 创建chart
$ helm create my-hello-world

# 打包helm
$ my-hello-world
$ helm package ./
Successfully packaged chart and saved it to: /Users/yshi3/Desktop/blog/my-hello-world/my-hello-world-0.1.0.tgz

# 查看helm chart
$ helm template my-hello-world-0.1.0.tgz
---
# Source: my-hello-world/templates/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: RELEASE-NAME-my-hello-world
  labels:
    helm.sh/chart: my-hello-world-0.1.0
    app.kubernetes.io/name: my-hello-world
    app.kubernetes.io/instance: RELEASE-NAME
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
---
# Source: my-hello-world/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: RELEASE-NAME-my-hello-world
  labels:
    helm.sh/chart: my-hello-world-0.1.0
    app.kubernetes.io/name: my-hello-world
    app.kubernetes.io/instance: RELEASE-NAME
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: my-hello-world
    app.kubernetes.io/instance: RELEASE-NAME
---
# Source: my-hello-world/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: RELEASE-NAME-my-hello-world
  labels:
    helm.sh/chart: my-hello-world-0.1.0
    app.kubernetes.io/name: my-hello-world
    app.kubernetes.io/instance: RELEASE-NAME
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: my-hello-world
      app.kubernetes.io/instance: RELEASE-NAME
  template:
    metadata:
      labels:
        app.kubernetes.io/name: my-hello-world
        app.kubernetes.io/instance: RELEASE-NAME
    spec:
      serviceAccountName: RELEASE-NAME-my-hello-world
      securityContext:
        {}
      containers:
        - name: my-hello-world
          securityContext:
            {}
          image: "nginx:1.16.0"
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {}
---
# Source: my-hello-world/templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "RELEASE-NAME-my-hello-world-test-connection"
  labels:
    helm.sh/chart: my-hello-world-0.1.0
    app.kubernetes.io/name: my-hello-world
    app.kubernetes.io/instance: RELEASE-NAME
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['RELEASE-NAME-my-hello-world:80']
  restartPolicy: Never
```





> https://yeasy.gitbook.io/docker_practice/repository/registry
>
> 





```shell
# 拉取最新的main分支
$ git checkout main

# 创建你的feature分支
$ git checkout feature/quality-bi

# ....开始魔法修改
# 此处省略工作细节

# 推送分支到代码库
$ git push origin feature/quality-bi:feature/quality-bi
```







- 书写bug
- 沟通上产生的bug
- 不明确产生的bug
- 优化上的bug



2022.08

[GF3MOS-1512](https://issues.teslamotors.com/browse/GF3MOS-1512)

GF3MOS-1513

GF3MOS-1514

GF3MOS-1515



2022.10

GF3MOS-1536

GF3MOS-1537

GF3MOS-1538

GF3MOS-1539
