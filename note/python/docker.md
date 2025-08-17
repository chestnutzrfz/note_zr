# 使用

### docker

开启vpn

docker desktop   sign in      登录  否则会有问题

https://hub.docker.com  在这个网站搜索 需要的项目  如mysql

docker run -d --name mysql -p 3306:3306 mysql:latest      即可下载并运行mysql容器

```
docker run -d ：创建并运行一个容器，-d则是让容器以后台进程运行

--name mysql : 给容器起个名字叫mysql，你可以叫别的

-p 3306:3306 : 设置端口映射。

容器是隔离环境，外界不可访问。但是可以将宿主机端口映射容器内到端口，当访问宿主机指定端口时，就是在访问容器内的端口了。

容器内端口往往是由容器内的进程决定，例如MySQL进程默认端口是3306，因此容器内端口一定是3306；而宿主机端口则可以任意指定，一般与容器内保持一致。

格式： -p 宿主机端口:容器内端口，示例中就是将宿主机的3306映射到容器内的3306端口

-e TZ=Asia/Shanghai : 配置容器内进程运行时的一些参数

格式：-e KEY=VALUE，KEY和VALUE都由容器内进程决定

案例中，TZ=Asia/Shanghai是设置时区；MYSQL_ROOT_PASSWORD=123是设置MySQL默认密码

mysql : 设置镜像名称，Docker会根据这个名字搜索并下载镜像

格式：REPOSITORY:TAG，例如mysql:8.0，其中REPOSITORY可以理解为镜像名，TAG是版本号

在未指定TAG的情况下，默认是最新版本，也就是mysql:latest

```

| **命令**      | ** 说明**                      |
| ------------- | ------------------------------ |
| docker images | 查看本地镜像                   |
| docker rmi    | 删除本地镜像                   |
| docker run    | 创建并运行容器（不能重复创建） |
| docker ps     | 查看容器                       |
| docker exec   | 进入容器                       |



### 阿里镜像

复制登录   密码为:zr445244

```
docker login --username=ali_zrzr crpi-gr7z0rnhy33wrmeb.cn-hangzhou.personal.cr.aliyuncs.com
```



### dockerfile

在制作镜像的文件夹目录中创建dockerfile文件

```
# 使用官方 Python 基础镜像
FROM python:3.12

# 如果出现错误，换国内源-阿里云即可解决
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量（生产环境应关闭 debug）
ENV FLASK_DEBUG=0

# 暴露端口（Flask 默认 5000）
EXPOSE 5000

# 启动命令（生产环境建议使用 Gunicorn）
CMD ["flask", "run", "--host", "0.0.0.0"]

```



### requirements.txt



```
Flask==2.0.3
Werkzeug==2.0.3  # 最后一个包含 url_quote 的版本

```



### 构建镜像

```
# 进入镜像目录
cd /root/demo
# 开始构建
docker build -t docker-demo:1.0 .
```

docker build : 就是构建一个docker镜像

-t docker-demo:1.0 ：-t参数是指定镜像的名称（repository和tag）

. : 最后的点是指构建时Dockerfile所在路径，由于我们进入了demo目录，所以指定的是.代表当前目录，也可以直接指定Dockerfile目录：

docker build -t docker-demo:1.0 /root/demo