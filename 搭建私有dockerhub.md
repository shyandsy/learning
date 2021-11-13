### 搭建私有docker hub



#### 安装

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
$ docker run -d -p 5000:5000 --restart=always -v /Users/yshi3/docker/data/registry:/var/lib/registry registry:latest
dcfaa1c3b1459c7e4c3c5d152aecf9c43863ede6b957e642e9633eb9bb430e31

$ docker ps
CONTAINER ID   IMAGE                                                         COMMAND                  CREATED          STATUS          PORTS                                                                                                                                  NAMES
dcfaa1c3b145   registry:latest                       "/entrypoint.sh /etc…"   24 seconds ago   Up 24 seconds   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp                                                                                              adoring_mahavira

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

1. 查看本地有哪些镜像

   ```shell
   $ docker images
   REPOSITORY                                                   TAG          IMAGE ID       CREATED        SIZE
   jenkins/jenkins                                              lts          2219cea3096b   7 days ago     441MB
   registry                                                     latest       b2cb11db9d3d   2 months ago   26.2MB
   mos-docker.arf.tesla.cn/tesla/app/mos-db-for-test            2021082511   b6c0041dd68c   2 months ago   2.13GB
   artifactory.teslamotors.com:2002/tesla/app/mos-db-gf3-dev0   latest       33b9c8aa3fa2   2 months ago   2.88GB
   bitnami/redis                                                6.2          c93ea1a8147d   3 months ago   95.4MB
   redis                                                        alpine       eb705d309426   3 months ago   32.3MB
   releases-docker.jfrog.io/jfrog/jfrog-cli-full-v2             latest       23eab2aa238f   3 months ago   4.08GB
   quay.io/derailed/k9s                                         latest       dbc4c0b42c3e   4 months ago   122MB
   gcr.io/k8s-minikube/kicbase                                  v0.0.25      8768eddc4356   4 months ago   1.1GB
   confluentinc/cp-kafka                                        latest       ca0dbcd0244c   4 months ago   771MB
   confluentinc/cp-schema-registry                              latest       e560c8baba46   4 months ago   1.52GB
   confluentinc/cp-kafka-rest                                   latest       4d52dd719050   4 months ago   1.47GB
   confluentinc/cp-zookeeper                                    latest       04999d93068f   4 months ago   771MB
   mos-docker.arf.tesla.cn/tesla/app/mos-db-by-jeremy           20210329     47ed61e142a7   7 months ago   6.66GB
   ```

   

2. 我们安装一个jenkins作为测试对象

   ```shell
   $ docker run -d -p 80:8080 -p 50000:50000 -v jenkins:/var/jenkins_home -v /etc/localtime:/etc/localtime --name jenkins jenkins/jenkins
   
   $ registry docker ps
   CONTAINER ID   IMAGE                                 COMMAND                  CREATED          STATUS          PORTS                                                                                                                                  NAMES
   1a52a898bea9   jenkins/jenkins                       "/sbin/tini -- /usr/…"   5 minutes ago    Up 5 minutes    0.0.0.0:50000->50000/tcp, :::50000->50000/tcp, 0.0.0.0:80->8080/tcp, :::80->8080/tcp                                                   jenkins
   3eb912684830   registry                              "/entrypoint.sh /etc…"   26 minutes ago   Up 26 minutes   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp                                                                                              nifty_colden
   ```

   

3. 基于jenkins创建customize jenkins

   ```
   jenkins                                                      customize    220f3c3059b7   32 seconds ago   445MB
   ```

   

4. 选择jenkins镜像，加上tag

   ```
   命令: docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
   ```

   ```shell
   $ docker commit -m "cusotmize jenkins" -a "shyandsy" 1a52a898bea9 jenkins:customize
   sha256:220f3c3059b7a9f3d0b14a42062a28ad42d02586c6860490917d0c3264867a0f
   
   $ docker images
   REPOSITORY                                                   TAG          IMAGE ID       CREATED          SIZE
   jenkins                                                      customize    220f3c3059b7   32 seconds ago   445MB
   jenkins/jenkins                                              latest       05fe72a4142c   2 days ago       442MB
   jenkins/jenkins                                              lts          2219cea3096b   7 days ago       441MB
   registry                                                     latest       b2cb11db9d3d   2 months ago     26.2MB
   mos-docker.arf.tesla.cn/tesla/app/mos-db-by-jeremy           20210329     47ed61e142a7   7 months ago     6.66GB
   
   
   $ docker tag jenkins:customize 127.0.0.1:5000/customize_jenkins
   
    docker images
   REPOSITORY                                                   TAG          IMAGE ID       CREATED        SIZE
   127.0.0.1:5000/customize_jenkins                             latest       220f3c3059b7   5 hours ago    445MB
   ```

   可以看到生成 了docker image： 127.0.0.1:5000/customize_jenkins

   

5. 上传到自己的docker hub

   ```shell
   $ docker push 127.0.0.1:5000/customize_jenkins
   Using default tag: latest
   The push refers to repository [127.0.0.1:5000/customize_jenkins]
   4200a0d20b50: Pushed 
   3154953a06c3: Pushed 
   50f5da5ebdcc: Pushed 
   87a865ee5394: Pushed 
   565281cb77e5: Pushed 
   584df43dd75c: Pushed 
   e5f52b41a3ee: Pushed 
   342ad7707104: Pushed 
   7c01aed20ed5: Pushed 
   12f0509c672f: Pushed 
   7d1a934998be: Pushed 
   adf46c5bb797: Pushed 
   d72174d13c01: Pushed 
   96dc41f99ac0: Pushed 
   dbbb267503ba: Pushed 
   5f0ee19bb898: Pushed 
   2b1a9a8ec011: Pushed 
   62a747bf1719: Pushed 
   latest: digest: sha256:39e64703d126443a6dbf0d142bd8fbfc3374199379b7652adc1bd0c90400505d size: 4087
   ```

   

6. 
