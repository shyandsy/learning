### 配置文件创建



- 定义deployment
  - 最简单的就是单个pod，没有其他东西，没有服务隔离
  - pod是一个container的实例，deployment可以有任意数量的pod
- 暴露services
- 部署到k8s cluster



#### 定义一个deployment

```yaml
$ vim deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-k8s-deployment
spec:
  selector:
    matchLabels:
      app: test-k8s
  replicas: 1
  template:
    metadata:
      labels:
        app: test-k8s
    spec:
      containers:
        - name: test-k8s
          image: shyandsy/tiny_home
          ports:
            - containerPort: 80
```



#### 使用kubectl expose命令对外暴露services

```shell
# 暴露服务，使用NodePort
$ k expose deployment test-k8s-deployment --type=NodePort
service/test-k8s-deployment exposed

# 获得访问地址，minikube所在虚拟机可以访问
$  minikube service test-k8s-deployment --url
http://192.168.49.2:32729
```



#### 也可以使用service配置来实现

```
```





#### 命令

```shell
# expose a port(tcp or udp) for a give deployment, pod, or other resource
$ k expose deployment test-k8s-deployment --type=NodePort
service/test-k8s-deployment exposed

# forward one or more local ports to a pod
# 把本机5000端口，转发到pod test-k8s-deployment-6b76b8fbf-cfj6d的80端口
# 在minikube主机上使用 curl 127.0.0.1:5000即可访问 pod内的80端口
$ k port-forward test-k8s-deployment-6b76b8fbf-cfj6d 5000:80
Forwarding from 127.0.0.1:5000 -> 80
Forwarding from [::1]:5000 -> 80
Handling connection for 5000

# attach to a process that is already running inside an existing container
$ k attach test-k8s-deployment-6b76b8fbf-cfj6d
If you don't see a command prompt, try pressing enter.                      ???

# update the labels on a resource
$ k label pods test-k8s-deployment-6b76b8fbf-cfj6d healthy=false

# run a particular image on the cluster
$ k run hazelcast --image=hazelcast --port 5701
deployment "hazelcast" created
```



#### stateful vs stateless application

再部署应用时候可以制定replicas，可以选择定义位置

- Deployment

- ReplicaSet
- Bare Pods
- Job
- DaemonSet



动态调整

```shell
$ k scale --replicas=2 deployment/test-k8s-deployment
deployment.apps/test-k8s-deployment scaled

# 现在2个pod
$ k get pod
NAME                                  READY   STATUS    RESTARTS   AGE
test-k8s-deployment-6b76b8fbf-56csf   1/1     Running   0          31s
test-k8s-deployment-6b76b8fbf-cfj6d   1/1     Running   0          37m

# 可以看到有2个pod运行
$ k get deployment
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
test-k8s-deployment   2/2     2            2           38m
```



#### 定义loadBalancer service

前面我们使用expose type NodePort，现在我们试试LoadBalancer

```shell
$ k expose deployment test-k8s-deployment --type=LoadBalancer --port=80 --target-port=80 --name test-k8s-load--balancer

$ k describe services test-k8s-load--balancer
```



----------



#### 使用ingress

```shell
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$1
spec:
  rules:
    - host: shyandsy.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 8080
```





-----------------------------



#### 编写第一个yaml创建pod

创建文件pod.yaml

```shell
$ vim pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-k8s
spec:
  containers:
    - name: test-k8s 
      image: shyandsy/tiny_home 
```



运行 k apply -f pod.yaml

```shell
$ k apply -f pod.yaml

$ k get pod
NAME       READY   STATUS    RESTARTS   AGE
test-k8s   2/2     Running   0          96s

$ k describe pod test-k8s
Name:         test-k8s
Namespace:    default
Priority:     0
Node:         minikube/192.168.49.2
Start Time:   Mon, 21 Feb 2022 09:50:50 -0500
Labels:       security.istio.io/tlsMode=istio
              service.istio.io/canonical-name=test-k8s
              service.istio.io/canonical-revision=latest
Annotations:  kubectl.kubernetes.io/default-container: test-k8s
              kubectl.kubernetes.io/default-logs-container: test-k8s
              prometheus.io/path: /stats/prometheus
              prometheus.io/port: 15020
              prometheus.io/scrape: true
              sidecar.istio.io/status:
                {"initContainers":["istio-init"],"containers":["istio-proxy"],"volumes":["istio-envoy","istio-data","istio-podinfo","istio-token","istiod-...
Status:       Running
IP:           172.17.0.14
IPs:
  IP:  172.17.0.14
Init Containers:
  istio-init:
    Container ID:  docker://930fb58036d3ece2aa129f86e3e7c641f60f21e34aba43c992b9b3ddd897c6be
    Image:         docker.io/istio/proxyv2:1.13.0
    Image ID:      docker-pullable://istio/proxyv2@sha256:2919336a667e83f3a1731a21252ff2f88c74218bffa9660638e0d190071a4510
    Port:          <none>
    Host Port:     <none>
    Args:
      istio-iptables
      -p
      15001
      -z
      15006
      -u
      1337
      -m
      REDIRECT
      -i
      *
      -x

      -b
      *
      -d
      15090,15021,15020
    State:          Terminated
      Reason:       Completed
      Exit Code:    0
      Started:      Mon, 21 Feb 2022 09:50:51 -0500
      Finished:     Mon, 21 Feb 2022 09:50:51 -0500
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     2
      memory:  1Gi
    Requests:
      cpu:        10m
      memory:     40Mi
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-lw56q (ro)
Containers:
  test-k8s:
    Container ID:   docker://011eacc5163d19cc298ce83051272c37abaed1588256ef8280a4d1eb68549298
    Image:          shyandsy/tiny_home
    Image ID:       docker-pullable://shyandsy/tiny_home@sha256:a3070915763b829208830ba5061d064a84b5f1fed7b284402565377aa0dd8169
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Mon, 21 Feb 2022 09:52:00 -0500
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-lw56q (ro)
  istio-proxy:
    Container ID:  docker://ffe0fc3b74c4297ece454bd786bc98ba25df568a88d1be0f3182ed7323d8a6a1
    Image:         docker.io/istio/proxyv2:1.13.0
    Image ID:      docker-pullable://istio/proxyv2@sha256:2919336a667e83f3a1731a21252ff2f88c74218bffa9660638e0d190071a4510
    Port:          15090/TCP
    Host Port:     0/TCP
    Args:
      proxy
      sidecar
      --domain
      $(POD_NAMESPACE).svc.cluster.local
      --proxyLogLevel=warning
      --proxyComponentLogLevel=misc:error
      --log_output_level=default:info
      --concurrency
      2
    State:          Running
      Started:      Mon, 21 Feb 2022 09:52:01 -0500
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     2
      memory:  1Gi
    Requests:
      cpu:      10m
      memory:   40Mi
    Readiness:  http-get http://:15021/healthz/ready delay=1s timeout=3s period=2s #success=1 #failure=30
    Environment:
      JWT_POLICY:                    third-party-jwt
      PILOT_CERT_PROVIDER:           istiod
      CA_ADDR:                       istiod.istio-system.svc:15012
      POD_NAME:                      test-k8s (v1:metadata.name)
      POD_NAMESPACE:                 default (v1:metadata.namespace)
      INSTANCE_IP:                    (v1:status.podIP)
      SERVICE_ACCOUNT:                (v1:spec.serviceAccountName)
      HOST_IP:                        (v1:status.hostIP)
      PROXY_CONFIG:                  {}

      ISTIO_META_POD_PORTS:          [
                                     ]
      ISTIO_META_APP_CONTAINERS:     test-k8s
      ISTIO_META_CLUSTER_ID:         Kubernetes
      ISTIO_META_INTERCEPTION_MODE:  REDIRECT
      ISTIO_META_WORKLOAD_NAME:      test-k8s
      ISTIO_META_OWNER:              kubernetes://apis/v1/namespaces/default/pods/test-k8s
      ISTIO_META_MESH_ID:            cluster.local
      TRUST_DOMAIN:                  cluster.local
    Mounts:
      /etc/istio/pod from istio-podinfo (rw)
      /etc/istio/proxy from istio-envoy (rw)
      /var/lib/istio/data from istio-data (rw)
      /var/run/secrets/istio from istiod-ca-cert (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-lw56q (ro)
      /var/run/secrets/tokens from istio-token (rw)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  istio-envoy:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:     Memory
    SizeLimit:  <unset>
  istio-data:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:
    SizeLimit:  <unset>
  istio-podinfo:
    Type:  DownwardAPI (a volume populated by information about the pod)
    Items:
      metadata.labels -> labels
      metadata.annotations -> annotations
  istio-token:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  43200
  istiod-ca-cert:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      istio-ca-root-cert
    Optional:  false
  kube-api-access-lw56q:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Burstable
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  2m6s               default-scheduler  Successfully assigned default/test-k8s to minikube
  Normal   Pulled     2m5s               kubelet            Container image "docker.io/istio/proxyv2:1.13.0" already present on machine
  Normal   Created    2m5s               kubelet            Created container istio-init
  Normal   Started    2m5s               kubelet            Started container istio-init
  Normal   Pulling    2m5s               kubelet            Pulling image "shyandsy/tiny_home"
  Normal   Pulled     56s                kubelet            Successfully pulled image "shyandsy/tiny_home" in 1m8.596721508s
  Normal   Created    56s                kubelet            Created container test-k8s
  Normal   Started    56s                kubelet            Started container test-k8s
  Normal   Pulled     56s                kubelet            Container image "docker.io/istio/proxyv2:1.13.0" already present on machine
  Normal   Created    56s                kubelet            Created container istio-proxy
  Normal   Started    55s                kubelet            Started container istio-proxy
  Warning  Unhealthy  52s (x4 over 54s)  kubelet            Readiness probe failed: Get "http://172.17.0.14:15021/healthz/ready": dial tcp 172.17.0.14:15021: connect: connection refused

```



#### 通过deployment来创建

```shell
$ vim deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-k8s-by-deployment
spec:
  replicas: 2
  # 用来查找相关的pod，所有标签都匹配才行
  selector:
    matchLabels:
      app: test-k8s-by-deployment
  # 定义pod相关数据
  template:
    metadata:
      labels:
        app: test-k8s-by-deployment
    spec:
      # 定义容器，可以多个
      containers:
        - name: test-k8s
          image: shyandsy/tiny_home
```



运行

```shell
# 部署
$ k apply -f deployment.yaml
deployment.apps/test-k8s-by-deployment created

$ k get deployment
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
test-k8s-by-deployment   2/2     2            2           3

$ k get pod

$ k get pod -o wide
NAME	READY   STATUS    RESTARTS   AGE    IP		NODE       NOMINATED NODE   REA                 DINESS GATES
test-k8s	2/2     Running   0          12m    172.17.0.14   minikube   <none>           <no                 ne>
test-k8s-by-deployment-79597458d6-chrps   2/2     Running   0          103s   172.17.0.18   minikube   <none>           <no                 ne>
test-k8s-by-deployment-79597458d6-s9mg6   2/2     Running   0          103s   172.17.0.17   minikube   <none>           <no                 ne>

# 进入pod内部可以访问
$ k exec -it test-k8s bash
$ curl 127.0.0.1
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta charset="UTF-8">
        <title>Dash</title>
        <link rel="icon" type="image/x-icon" href="/_favicon.ico?v=2.1.0">
        <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/bWLwgP.css">
    </head>
    <body>

<div id="react-entry-point">
    <div class="_dash-loading">
        Loading...
    </div>
</div>

        <footer>
            <script id="_dash-config" type="application/json">{"url_base_pathname":null,"requests_pathname_prefix":"/","ui":false,"props_check":false,"show_undo_redo":false,"suppress_callback_exceptions":false,"update_title":"Updating..."}</script>
            <script src="/_dash-component-suites/dash/deps/polyfill@7.v2_1_0m1644846186.12.1.min.js"></script>
<script src="/_dash-component-suites/dash/deps/react@16.v2_1_0m1644846186.14.0.min.js"></script>
<script src="/_dash-component-suites/dash/deps/react-dom@16.v2_1_0m1644846186.14.0.min.js"></script>
<script src="/_dash-component-suites/dash/deps/prop-types@15.v2_1_0m1644846186.7.2.min.js"></script>
<script src="/_dash-component-suites/dash/dash-renderer/build/dash_renderer.v2_1_0m1644846186.min.js"></script>
<script src="/_dash-component-suites/dash/dcc/dash_core_components.v2_1_0m1644846186.js"></script>
<script src="/_dash-component-suites/dash/dcc/dash_core_components-shared.v2_1_0m1644846186.js"></script>
<script src="/_dash-component-suites/dash/html/dash_html_components.v2_0_1m1644846186.min.js"></script>
<script src="/_dash-component-suites/dash/dash_table/bundle.v5_1_0m1644846186.js"></script>
            <script id="_dash-renderer" type="application/javascript">var renderer = new DashRenderer();</script>
        </footer>
    </body>
</html>r
```



关键：

- deployment通过label和pod关联，deployment通过



#### service

现在只能在pod内部访问应用，我们需要创建service

service.yaml

```shell
$ vim service.yaml
apiVersion: v1
kind: Service
metadata:
  name: test-k8s
spec:
  selector:
    app: test-k8s
  type: ClusterIP
  ports:
    - port: 8080        # 本 Service 的端口
      targetPort: 80  # 容器端口
      nodePort: 8080
```

运行

```shell
$ k apply -f service.yaml
service/test-k8s created

$ k get svc
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP    26h
test-k8s     ClusterIP   10.105.254.160   <none>        8080/TCP   6s
```





```shell
$ vim service.yaml
apiVersion: v1
kind: Service
metadata:
  name: test-k8s
spec:
  selector:
    app: test-k8s
  type: NodePort
  ports:
    - port: 8080        # 本 Service 的端口
      targetPort: 80  # 容器端口
      nodePort: 30030
      
      
apiVersion: v1
kind: Service
metadata:
  name: test-k8s
  selector:
    app: test-k8s
spec:
  selector:
    app: test-k8s
  type: NodePort
  ports:
    - port: 80        # 本 Service 的端口
      targetPort: 80  # 容器端口
      nodePort: 30000
      protocol: TCP
```

运行

```shell
$ k apply -f service.yaml
service/test-k8s created

# 还是不行
$ curl http://192.168.49.2:30030
curl: (7) Failed connect to 192.168.49.2:30030; Connection refused
$ curl http://192.168.49.2:8080
curl: (7) Failed connect to 192.168.49.2:8080; Connection refused
```



[shyandsy@localhost deployment]$ curl http://192.168.49.2:30030
curl: (7) Failed connect to 192.168.49.2:30030; Connection refused
[shyandsy@localhost deployment]$ curl http://192.168.49.2:8080
curl: (7) Failed connect to 192.168.49.2:8080; Connection refused



#### ClusterIp Service

- 原理
- 通过ClusterIp Service访问内部mysql pod



pod： ip会变，包含一组集群多个ip

pod之间服务发现，反向路由，负载均衡

pod集群内可以通过cluster ip去访问其他pod



#### NodePort Service

- service: selector
- pod: label



#### LoadBalance Service



