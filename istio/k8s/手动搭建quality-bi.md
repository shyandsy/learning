### 手动搭建quality-bi



- 镜像准备
  - 创建docker image
  - 推送到registry
- k8s配置文件，手动安装
  - deployment
  - service
  - ingress 
- helm chart安装



#### 创建doker image推送到registry

新建空文件app/__init__.py

新建requirements.txt

```python
dash
gunicorn
pandas
plotly
```



新建app\app.py

```python
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://[your-ip-or-domain-name]:8080/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

# base url
prefix = '/dash/'

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname=prefix)
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
    #app.run_server(debug=True)  # <== THIS MAY NOT DEPLOY
    #USE DIFFERENT ARGUMENTS FOR run_server METHOD
    app.run_server(debug=True, host='0.0.0.0', port=8080)
```

启动后，访问127.0.0.1:8080/dash即可看到



Dockerfile

```dockerfile
FROM china-devops-docker-local.arf.tesla.cn/base-images/python:3.8
#FROM china-dots-system-docker-local.arf.tesla.cn/share/dots:builder as compiler

COPY requirements.txt ./requirements.txt

#COPY . ./
RUN GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/shyandsy/dash-sample dash-sample
WORKDIR dash-sample

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD gunicorn -b 0.0.0.0:80 app.app:server
```



打包镜像

```shell
$ docker build -t dots/api/quality-bi .
$ docker tag dots/api/quality-bi:latest china-devops-docker-local.arf.tesla.cn/dots/api/quality-bi:latest
$ docker push china-devops-docker-local.arf.tesla.cn/dots/api/quality-bi:latest
```



#### k8s配置，手动安装

deployment.yaml

```yaml
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



service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test-k8s-service
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



ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-k8s-ingress
  annotations:
# nginx.ingress.kubernetes.io/rewrite-target: /$1
spec:
  rules:
    - host: "shyandsy.com"
      http:
        paths:
        - path: /_dash-component-suites
          pathType: Prefix
          backend:
            service:
              name: test-k8s-service
              port:
                number: 80
        - path: /_dash-dependencies
          pathType: Prefix
          backend:
            service:
              name: test-k8s-service
              port:
                number: 80
        - path: /_dash-layout
          pathType: Prefix
          backend:
            service:
              name: test-k8s-service
              port:
                number: 80
        - path: /dash
          pathType: ImplementationSpecific
          backend:
            service:
              name: test-k8s-service
              port:
                number: 80
```



安装

```shell
$ k apply -f deployment.yaml
deployment.apps/test-k8s-deployment created
$ k apply -f service.yaml
service/test-k8s-service created
$ k apply -f ingress.yaml
ingress.networking.k8s.io/test-k8s-ingress created
```

