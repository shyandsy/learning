### helm总结



#### 安装



#### 三个核心概念

- chart： 一个helm package，包括了运行一个k8s cluster应用程序，工具，或者服务的所有所需的资源定义
- repository：存储，分享chart的地方
- release：chart运行在k8s集群上的一个实例，一个chart可以被多次安装在同一个cluster上，每次安装，都会创建一个新的release。



#### 核心命令

1. helm search，查找charts，可以在两种不通的来源上搜索

   ```shell
   # 1. helm search hub：在the artifact hub（https://artifacthub.io/）搜索
   $ helm search hub wordpress
   URL                                                     CHART VERSION   APP VERSION             DESCRIPTION
   https://artifacthub.io/packages/helm/kube-wordp...      0.1.0           1.1                     this is my wordpress package
   https://artifacthub.io/packages/helm/bitnami/wo...      13.0.11         5.9.0                   WordPress is the world's most popular blogging ...
   https://artifacthub.io/packages/helm/bitnami-ak...      13.0.7          5.8.3                   WordPress is the world's most popular blogging ...
   https://artifacthub.io/packages/helm/riftbit/wo...      12.1.16         5.8.1                   Web publishing platform for building blogs and ...
   
   
   
   # 2. helm search repo：在手动添加的repo中搜索，参考命令 helm repo add
   $ helm search repo
   Error: no repositories configured
   ```

   

2. helm install，安装部署一个chart

   helm install 名字 chart，这里release名wordpress，chart是bitnami/wordpress

   ```shell
   $ helm -n wordpress-release install wordpress bitnami/wordpress
   ```

   

3. helm status查看release的状态。helm install不会等待整个资源都运行起来，需要用status命令来跟踪部署状态

   ```shell
   $ helm -n wordpress-release status wordpress
   NAME: wordpress
   LAST DEPLOYED: Sun Feb 20 08:51:06 2022
   NAMESPACE: wordpress-release
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   CHART NAME: wordpress
   CHART VERSION: 13.0.11
   APP VERSION: 5.9.0
   
   ** Please be patient while the chart is being deployed **
   
   Your WordPress site can be accessed through the following DNS name from within your cluster:
   
       wordpress.wordpress-release.svc.cluster.local (port 80)
   
   To access your WordPress site from outside the cluster follow the steps below:
   
   1. Get the WordPress URL by running these commands:
   
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           Watch the status with: 'kubectl get svc --namespace wordpress-release -w wordpress'
   
      export SERVICE_IP=$(kubectl get svc --namespace wordpress-release wordpress --include "{{ range (index .status.loadBalancer.ingress 0) }}{{ . }}{{ end }}")
      echo "WordPress URL: http://$SERVICE_IP/"
      echo "WordPress Admin URL: http://$SERVICE_IP/admin"
   
   2. Open a browser and access WordPress using the obtained URL.
   
   3. Login with the following credentials below to see your blog:
   
     echo Username: user
     echo Password: $(kubectl get secret --namespace wordpress-release wordpress -o jsonpath="{.data.wordpress-password}" | base64 --decode)
   ```

   

4. helm show values命令，查看hub上的chart。我们可能会希望对开源的chart做一些定制

   ```shell
   $ helm show values bitnami/wordpress
   ## @section Global parameters
   ## Global Docker image parameters
   ## Please, note that this will override the image parameters, including dependencies, configured to use the global value
   ## Current available global Docker image parameters: imageRegistry, imagePullSecrets and storageClass
   
   ## @param global.imageRegistry Global Docker image registry
   ## @param global.imagePullSecrets Global Docker registry secret names as an array
   ## @param global.storageClass Global StorageClass for Persistent Volume(s)
   ##
   global:
     imageRegistry: ""
     ## E.g.
     ## imagePullSecrets:
     ##   - myRegistryKeySecretName
     ##
     imagePullSecrets: []
     storageClass: ""
   ...............................................................省略
   ```

   

5. 在hub中chart的基础上，增加定制内容

   ```shell
   $ echo '{mariadb.auth.database: user0db, mariadb.auth.username: user0}' > values.yaml
   
   $ helm install -f values.yaml bitnami/wordpress --generate-name
   ```

   定制database参数信息

   - 用户名 user0

   - 给新用户授权数据库 `user0db` 访问权限

     

6. helm install时候，有两个方法传递配置数据

   - `--value`   指定覆盖的yaml文件，可以指定多个，最右边的文件优先级最高

   - `--set`       命令行中直接覆盖。如果同时使用`--value`和`--set`，则所有数据会合并，--set优先级高于--value。--set中的参数会被持久化在ConfigMap中

     

7. 查看--set的定制参数

   helm get values release名

   ```shell
   $ helm get values happy-panda
   mariadb:
     auth:
       username: user1
       
   # helm get 可用参数   
   Available Commands:
     all         download all information for a named release
     hooks       download all hooks for a named release
     manifest    download the manifest for a named release
     notes       download the notes for a named release
     values      download the values file for a named release
   ```

   

8. 删除helm install时候--set加入的参数

   ```shell
   $ helm upgrade with --reset-values
   ```

   

9. helm upgrade，有两个作用

   - 升级chart release
   - 修改release的配置

   upgrade会基于当前的release，根据upgrade参数提供的信息来升级。chart可以非常复杂和庞大，helm采用最小改动原则来提供性能能

   ```shell
   $ helm upgrade -f panda.yaml happy-panda bitnami/wordpress
   ```

   

10. helm rollback

    部署时候出现问题的时候，可以通过rollback回到上一个版本

    ```shell
    $ helm rollback [RELEASE] [REVISION]
    
    $ helm rollback happy-panda 1
    ```

    

11. 卸载 helm uninstall

    ```shell
    $ helm uninstall happy-panda
    ```

    

12. helm repo，管理repo

    ```shell
    $ helm repo list
    NAME            URL
    stable          https://charts.helm.sh/stable
    mumoshu         https://mumoshu.github.io/charts
    
    $ helm repo add dev https://example.com/dev-charts
    
    $ helm repo update
    
    $ helm repo remove
    ```

    

13. 创建自定义chart

    ```shell
    # 创建
    $ helm create deis-workflow
    Creating deis-workflow
    
    # 打包
    $ helm package deis-workflow
    deis-workflow-0.1.0.tgz
    
    # 安装
    $ helm install deis-workflow ./deis-workflow-0.1.0.tgz
    ```

    

14. 



#### 使用helm hub部署一个wordpress

1. helm install，安装chart。我们安装一个wordpress。https://artifacthub.io/packages/helm/bitnami/wordpress

   ```SHELL
   $ helm repo add bitnami https://charts.bitnami.com/bitnami
   
   $ kubectl create namespace wordpress-release
   
   $ helm -n wordpress-release install wordpress bitnami/wordpress
   NAME: my-release
   LAST DEPLOYED: Sun Feb 20 05:20:32 2022
   NAMESPACE: default
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   CHART NAME: wordpress
   CHART VERSION: 13.0.11
   APP VERSION: 5.9.0
   
   ** Please be patient while the chart is being deployed **
   
   Your WordPress site can be accessed through the following DNS name from within your cluster:
   
       my-release-wordpress.default.svc.cluster.local (port 80)
   
   To access your WordPress site from outside the cluster follow the steps below:
   
   1. Get the WordPress URL by running these commands:
   
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           Watch the status with: 'kubectl get svc --namespace default -w my-release-wordpress'
   
      export SERVICE_IP=$(kubectl get svc --namespace default my-release-wordpress --include "{{ range (index .status.loadBalancer.ingress 0) }}{{ . }}{{ end }}")
      echo "WordPress URL: http://$SERVICE_IP/"
      echo "WordPress Admin URL: http://$SERVICE_IP/admin"
   
   2. Open a browser and access WordPress using the obtained URL.
   
   3. Login with the following credentials below to see your blog:
   
     echo Username: user
     echo Password: $(kubectl get secret --namespace default my-release-wordpress -o jsonpath="{.data.wordpress-password}" | base64 --decode)
     
     
   $ helm list 
   NAME            NAMESPACE       REVISION        UPDATED			STATUS          CHART                   APP VERSION
   my-release      default         1               2022-02-200		 deployed        wordpress-13.0.11       5.9.0
   
   # 检查pod状态
   $ kubectl -n wordpress-release get pods
   NAME                        READY   STATUS             RESTARTS   AGE
   wordpress-fdbd54b87-5rlgb   0/1     ImagePullBackOff   0          3m20s
   wordpress-mariadb-0         0/1     ImagePullBackOff   0          3m19s
   
   # 检查pod详细
   $ kubectl -n  wordpress-release describe pod  wordpress-fdbd54b87-5rlgb
   Name:         wordpress-fdbd54b87-5rlgb
   Namespace:    wordpress-release
   Priority:     0
   Node:         minikube/192.168.49.2
   Start Time:   Sun, 20 Feb 2022 06:01:23 -0500
   Labels:       app.kubernetes.io/instance=wordpress
                 app.kubernetes.io/managed-by=Helm
                 app.kubernetes.io/name=wordpress
                 helm.sh/chart=wordpress-13.0.11
                 pod-template-hash=fdbd54b87
   Annotations:  <none>
   Status:       Pending
   IP:           172.17.0.5
   IPs:
     IP:           172.17.0.5
   Controlled By:  ReplicaSet/wordpress-fdbd54b87
   Containers:
     wordpress:
       Container ID:
       Image:          docker.io/bitnami/wordpress:5.9.0-debian-10-r9
       Image ID:
       Ports:          8080/TCP, 8443/TCP
       Host Ports:     0/TCP, 0/TCP
       State:          Waiting
         Reason:       ImagePullBackOff
       Ready:          False
       Restart Count:  0
       Requests:
         cpu:      300m
         memory:   512Mi
       Liveness:   http-get http://:http/wp-admin/install.php delay=120s timeout=5s period=10s #success=1 #failure=6
       Readiness:  http-get http://:http/wp-login.php delay=30s timeout=5s period=10s #success=1 #failure=6
       Environment:
         BITNAMI_DEBUG:                          false
         ALLOW_EMPTY_PASSWORD:                   yes
         MARIADB_HOST:                           wordpress-mariadb
         MARIADB_PORT_NUMBER:                    3306
         WORDPRESS_DATABASE_NAME:                bitnami_wordpress
         WORDPRESS_DATABASE_USER:                bn_wordpress
         WORDPRESS_DATABASE_PASSWORD:            <set to the key 'mariadb-password' in secret 'wordpress-mariadb'>  Optional: false
         WORDPRESS_USERNAME:                     user
         WORDPRESS_PASSWORD:                     <set to the key 'wordpress-password' in secret 'wordpress'>  Optional: false
         WORDPRESS_EMAIL:                        user@example.com
         WORDPRESS_FIRST_NAME:                   FirstName
         WORDPRESS_LAST_NAME:                    LastName
         WORDPRESS_HTACCESS_OVERRIDE_NONE:       no
         WORDPRESS_ENABLE_HTACCESS_PERSISTENCE:  no
         WORDPRESS_BLOG_NAME:                    User's Blog!
         WORDPRESS_SKIP_BOOTSTRAP:               no
         WORDPRESS_TABLE_PREFIX:                 wp_
         WORDPRESS_SCHEME:                       http
         WORDPRESS_EXTRA_WP_CONFIG_CONTENT:
         WORDPRESS_AUTO_UPDATE_LEVEL:            none
         WORDPRESS_PLUGINS:                      none
         APACHE_HTTP_PORT_NUMBER:                8080
         APACHE_HTTPS_PORT_NUMBER:               8443
       Mounts:
         /bitnami/wordpress from wordpress-data (rw,path="wordpress")
         /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-9r72k (ro)
   Conditions:
     Type              Status
     Initialized       True
     Ready             False
     ContainersReady   False
     PodScheduled      True
   Volumes:
     wordpress-data:
       Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
       ClaimName:  wordpress
       ReadOnly:   false
     kube-api-access-9r72k:
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
     Type     Reason     Age                  From               Message
     ----     ------     ----                 ----               -------
     Normal   Scheduled  2m34s                default-scheduler  Successfully assigned wordpress-release/wordpress-fdbd54b87-5rlgb to minikube
     Warning  Failed     67s                  kubelet            Failed to pull image "docker.io/bitnami/wordpress:5.9.0-debian-10-r9": rpc error: code = Unknown desc = Error response from daemon: Get "https://registry-1.docker.io/v2/": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
     Normal   BackOff    27s (x5 over 2m18s)  kubelet            Back-off pulling image "docker.io/bitnami/wordpress:5.9.0-debian-10-r9"
     Warning  Failed     27s (x5 over 2m18s)  kubelet            Error: ImagePullBackOff
     Normal   Pulling    15s (x4 over 2m33s)  kubelet            Pulling image "docker.io/bitnami/wordpress:5.9.0-debian-10-r9"
     Warning  Failed     0s (x3 over 2m18s)   kubelet            Failed to pull image "docker.io/bitnami/wordpress:5.9.0-debian-10-r9": rpc error: code = Unknown desc = Error response from daemon: Get "https://registry-1.docker.io/v2/": net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
     Warning  Failed     0s (x4 over 2m18s)   kubelet            Error: ErrImagePull
   ```

   

   <font color="red">解决办法</font>：这是docker registry无法访问导致的，改用镜像地址即可

   ```shell
   $ sudo vim /etc/docker/daemon.json
   {
     "registry-mirrors":["https://ixoaalsa.mirror.aliyuncs.com","https://docker.mirrors.ustc.edu.cn"]
   }
   
   # 重启docker
   $ systemctl daemon-reload
   $ systemctl restart docker
   
   # 重启pod
   $ kubectl scale deployment XXXX --replicas=0 -n wordpress-release
   $ kubectl scale deployment XXXX --replicas=1 -n wordpress-release
   
   # 检查，创建成功了
   $ k -n wordpress-release get pod
   NAME                        READY   STATUS              RESTARTS   AGE
   wordpress-fdbd54b87-rmnjt   0/1     ContainerCreating   0          24s
   wordpress-mariadb-0         0/1     ContainerCreating   0          23s
   
   # 查看pod情况
   $ k -n wordpress-release describe pod wordpress-fdbd54b87-rmnjt
   Name:         wordpress-fdbd54b87-rmnjt
   Namespace:    wordpress-release
   Priority:     0
   Node:         minikube/192.168.49.2
   Start Time:   Sun, 20 Feb 2022 08:51:07 -0500
   Labels:       app.kubernetes.io/instance=wordpress
                 app.kubernetes.io/managed-by=Helm
                 app.kubernetes.io/name=wordpress
                 helm.sh/chart=wordpress-13.0.11
                 pod-template-hash=fdbd54b87
   Annotations:  <none>
   Status:       Running
   IP:           172.17.0.5
   IPs:
     IP:           172.17.0.5
   Controlled By:  ReplicaSet/wordpress-fdbd54b87
   Containers:
     wordpress:
       Container ID:   docker://45e7b1392cb0af652dadfbfc0d64c716bde4f92c085d1b64a6829f8e3bb539a8
       Image:          docker.io/bitnami/wordpress:5.9.0-debian-10-r9
       Image ID:       docker-pullable://bitnami/wordpress@sha256:5ee13e7d3eff27f75eef823a10015fee8cbf6dadcf79cd2e831ca21db38c1cdb
       Ports:          8080/TCP, 8443/TCP
       Host Ports:     0/TCP, 0/TCP
       State:          Running
         Started:      Sun, 20 Feb 2022 08:52:01 -0500
       Ready:          True
       Restart Count:  0
       Requests:
         cpu:      300m
         memory:   512Mi
       Liveness:   http-get http://:http/wp-admin/install.php delay=120s timeout=5s period=10s #success=1 #failure=6
       Readiness:  http-get http://:http/wp-login.php delay=30s timeout=5s period=10s #success=1 #failure=6
       Environment:
         BITNAMI_DEBUG:                          false
         ALLOW_EMPTY_PASSWORD:                   yes
         MARIADB_HOST:                           wordpress-mariadb
         MARIADB_PORT_NUMBER:                    3306
         WORDPRESS_DATABASE_NAME:                bitnami_wordpress
         WORDPRESS_DATABASE_USER:                bn_wordpress
         WORDPRESS_DATABASE_PASSWORD:            <set to the key 'mariadb-password' in secret 'wordpress-mariadb'>  Optional: false
         WORDPRESS_USERNAME:                     user
         WORDPRESS_PASSWORD:                     <set to the key 'wordpress-password' in secret 'wordpress'>  Optional: false
         WORDPRESS_EMAIL:                        user@example.com
         WORDPRESS_FIRST_NAME:                   FirstName
         WORDPRESS_LAST_NAME:                    LastName
         WORDPRESS_HTACCESS_OVERRIDE_NONE:       no
         WORDPRESS_ENABLE_HTACCESS_PERSISTENCE:  no
         WORDPRESS_BLOG_NAME:                    User's Blog!
         WORDPRESS_SKIP_BOOTSTRAP:               no
         WORDPRESS_TABLE_PREFIX:                 wp_
         WORDPRESS_SCHEME:                       http
         WORDPRESS_EXTRA_WP_CONFIG_CONTENT:
         WORDPRESS_AUTO_UPDATE_LEVEL:            none
         WORDPRESS_PLUGINS:                      none
         APACHE_HTTP_PORT_NUMBER:                8080
         APACHE_HTTPS_PORT_NUMBER:               8443
       Mounts:
         /bitnami/wordpress from wordpress-data (rw,path="wordpress")
         /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-p8wts (ro)
   Conditions:
     Type              Status
     Initialized       True
     Ready             True
     ContainersReady   True
     PodScheduled      True
   Volumes:
     wordpress-data:
       Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
       ClaimName:  wordpress
       ReadOnly:   false
     kube-api-access-p8wts:
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
     Normal   Scheduled  13m                default-scheduler  Successfully assigned wordpress-release/wordpress-fdbd54b87-rmnjt to minikube
     Normal   Pulling    13m                kubelet            Pulling image "docker.io/bitnami/wordpress:5.9.0-debian-10-r9"
     Normal   Pulled     12m                kubelet            Successfully pulled image "docker.io/bitnami/wordpress:5.9.0-debian-10-r9" in 53.781746559s
     Normal   Created    12m                kubelet            Created container wordpress
     Normal   Started    12m                kubelet            Started container wordpress
     Warning  Unhealthy  11m (x4 over 11m)  kubelet            Readiness probe failed: Get "http://172.17.0.5:8080/wp-login.php": dial tcp 172.17.0.5:8080: connect: connection refused
   ```

   

2. 获取访问url，现在虚拟机内部通过地址

   ```shell
   $ minikube -n wordpress-release service wordpress --url
   http://192.168.49.2:31628
   http://192.168.49.2:31941
   ```

   现在虚拟机内部访问http://192.168.49.2:31628 即可打开网页

   

3. 如何让虚拟机对外提供服务呢?



#### 创建自己的dash chart

1. 创建chart

   ```shell
   $ helm create test
   Creating test
   
   $ tree ./test
   .
   ├── charts
   ├── 
   ├── templates
   │   ├── deployment.yaml
   │   ├── _helpers.tpl
   │   ├── hpa.yaml
   │   ├── ingress.yaml
   │   ├── NOTES.txt
   │   ├── serviceaccount.yaml
   │   ├── service.yaml
   │   └── tests
   │       └── test-connection.yaml
   └── values.yaml
   
   $cat 
   
   ```

   

   Chart.yaml内容

   ```shell
   apiVersion: v2
   name: test
   description: A Helm chart for Kubernetes
   
   # A chart can be either an 'application' or a 'library' chart.
   #
   # Application charts are a collection of templates that can be packaged into versioned archives
   # to be deployed.
   #
   # Library charts provide useful utilities or functions for the chart developer. They're included as
   # a dependency of application charts to inject those utilities and functions into the rendering
   # pipeline. Library charts do not define any templates and therefore cannot be deployed.
   type: application
   
   # This is the chart version. This version number should be incremented each time you make changes
   # to the chart and its templates, including the app version.
   # Versions are expected to follow Semantic Versioning (https://semver.org/)
   version: 0.1.0
   
   # This is the version number of the application being deployed. This version number should be
   # incremented each time you make changes to the application. Versions are not expected to
   # follow Semantic Versioning. They should reflect the version the application is using.
   # It is recommended to use it with quotes.
   appVersion: "1.16.0"
   ```

   

   查看templates/deployment.yaml

   ```shell
   $ cat templates/deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: {{ include "test.fullname" . }}
     labels:
       {{- include "test.labels" . | nindent 4 }}
   spec:
     {{- if not .Values.autoscaling.enabled }}
     replicas: {{ .Values.replicaCount }}
     {{- end }}
     selector:
       matchLabels:
         {{- include "test.selectorLabels" . | nindent 6 }}
     template:
       metadata:
         {{- with .Values.podAnnotations }}
         annotations:
           {{- toYaml . | nindent 8 }}
         {{- end }}
         labels:
           {{- include "test.selectorLabels" . | nindent 8 }}
       spec:
         {{- with .Values.imagePullSecrets }}
         imagePullSecrets:
           {{- toYaml . | nindent 8 }}
         {{- end }}
         serviceAccountName: {{ include "test.serviceAccountName" . }}
         securityContext:
           {{- toYaml .Values.podSecurityContext | nindent 8 }}
         containers:
           - name: {{ .Chart.Name }}
             securityContext:
               {{- toYaml .Values.securityContext | nindent 12 }}
             image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
             imagePullPolicy: {{ .Values.image.pullPolicy }}
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
               {{- toYaml .Values.resources | nindent 12 }}
         {{- with .Values.nodeSelector }}
         nodeSelector:
           {{- toYaml . | nindent 8 }}
         {{- end }}
         {{- with .Values.affinity }}
         affinity:
           {{- toYaml . | nindent 8 }}
         {{- end }}
         {{- with .Values.tolerations }}
         tolerations:
           {{- toYaml . | nindent 8 }}
         {{- end }}
   ```

   

2. 打包

3. 上传



#### 分析上面wordpress的chart

https://github.com/bitnami/charts/tree/master/bitnami/wordpress







#### 2022.02.23 python deployment

- docker镜像
  - from ： china-devops-docker-local.arf.tesla.cn/base-images/python:3.8
- helm部署，install
- k8s配置
