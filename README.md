# taiga 容器部署

# taiga 组件介绍

## Taiga-front

由angularjs和coffeescript搭建的一个前端，可以运行在nginx中的静态网站。[taiga/taiga-front](https://github.com/taigaio/taiga-front.git)

[taiga/taiga-front-dist](https://github.com/taigaio/taiga-front-dist) 是taiga-front编译完版本，如果只是部署，可以使用这个版本。

## Taiga-back 

由django和python3编写的一个后台APIs服务。[taiga/taiga-back](https://github.com/taigaio/taiga-back.git)

# Taiga-docker 部署步骤

准备一个有docker环境的机器，具体安装参见官方[Docker Install](https://docs.docker.com/engine/installation/)  

## 克隆该项目到本地

码云的项目地址[https://gitee.com/tableExchange/taiga-docker.git](https://gitee.com/tableExchange/taiga-docker.git)
Github的分支地址[https://github.com/jussker/taiga-docker.git](https://github.com/jussker/taiga-docker.git)
原项目是GitHub上的ipedrazas维护的，地址[https://github.com/ipedrazas/taiga-docker/](https://github.com/ipedrazas/taiga-docker/)
因为用原项目教程没部署起来，所以分支重新修改了一下。最近原项目更新了，有兴趣的可以尝试下，增加了k8s的部署脚本。

```
git clone -b master --single-branch https://gitee.com/tableExchange/taiga-docker.git ~/taiga-docker
cd ~/taiga-docker
```

## 编译docker镜像

```
cd ~/taiga-docker/backend
./build.sh jussker-dev/taiga-back:dev
```
其中将`jussker-dev/taiga-back:dev`换成自己的镜像名称

```
cd ~/taiga-docker/frontend
./build.sh jussker-dev/taiga-front:dev
```
其中将`jussker-dev/taiga-front:dev`换成自己的镜像名称

## 修改`docker-compose.yml` 

将镜像改为自己的镜像名称,修改修改的地方如下所示：

`docker-compose.yml`

```
...
  taigabackend:
    image: jussker-dev/taiga-back:dev
...
  taigafrontend:
    image: jussker-dev/taiga-front:dev
...
```

## 启动服务

如果环境中已经有容器编排工具，则将docker-compose.yml提交给编排工具进行部署。

如果环境中还没有，则可以安装docker-compose,安装步骤参考官方的[Install Docker Compose](https://docs.docker.com/compose/install/#install-compose).这里演示使用docker-compose.

如果是部署在服务器上，则将`docker-compose`文件中的`localhost`替换为实际ip,如果文件中的端口已经被占用，则修改为新端口。`8000`后端api服务端口,`8080`前端服务端口。

```
cd ~/taiga-docker
docker-compose create
docker-compose start
```

## 进行初始化
初始化过程需要进入taigabackend容器中

```
docker ps 
```

找到`taigabackend`的容器id

```
CONTAINER ID        IMAGE                                                                                         COMMAND                  CREATED             STATUS              PORTS                    NAMES
ef5f0541b8e0        jussker-dev/taiga-front:dev                                                                   "/taiga/run.sh"          2 minutes ago       Up 52 seconds       0.0.0.0:8080->80/tcp     taigadocker_taigafrontend_1
8a58837b1201        jussker-dev/taiga-back:dev                                                                    "python manage.py ..."   2 minutes ago       Up 52 seconds       0.0.0.0:8000->8000/tcp   taigadocker_taigabackend_1
92b4f7a956cc        postgres                                                                                      "docker-entrypoint..."   2 minutes ago       Up 52 seconds       5432/tcp                 taigadocker_postgresdb_1
```

```
#进入容器
docker exec -it 8a58837b1201 /bin/bash
```

这样我们进入到容器中

初始化过程需要两步，初始化数据库和初始化静态文件,如下命令在taigabackend的容器中执行

```
#初始化数据库
chmod u+x ./regenerate.sh
./regenerate.sh

#初始化静态文件
python manage.py collectstatic

```

```
#退出容器
exit
```

## 查看界面

登陆taiga的地址[http://localhost:8080/](http://localhost:8080/)即可查看。管理员账户`admin`,密码`123123`

Django的管理界面[http://localhost:8080/admin/](http://localhost:8080/)可以查看数据库元数据。管理员账户`admin`,密码`123123`

## 特殊情况
如果需要将taiga的服务部署在不同的机器或者网段中，则需要注意将如下环境变量配置称为实际的地址

- `"MEDIA_URL=http://taiga-front:port/media/"` 
- `"STATIC_URL=http://taiga-front:port/static/"` 

将后端存储用户文件的uri或url 配置成实际提供文件服务的地址。如果有必要，也是要修改前端nginx代理。

需要了解的是，Taiga中文件或资源地址是由后端生成好后，发送给前端服务的，地址就是由`MEDIA_URL`和`STATIC_URL`决定其前缀。
如`MEDIA_URL=/media/`,则实际的地址为`http://taiga-backend:8001/media/`
如`MEDIA_URL=http//192.168.1.101:8001/media/`，则实际地址还是`http//192.168.1.101:8001/media/`

## docker-compose中环境变量说明

**Postgres的配置**

- `"POSTGRES_HOST=postgresdb"` 数据地址
- `"POSTGRES_DB=taiga"` 数据库名
- `"POSTGRES_USER=taiga"` 数据库登陆用户名
- `"POSTGRES_PASSWORD=taiga"` 数据库登陆密码

**Taiga-backend的配置**

- `"API_BASE_PROTOCOL=http"` 后端api使用的协议类型
- `"API_BASE_DOMAIN=taigabackend"` 后端api对外的域名或者ip
- `"API_BASE_PORT=8000"` 后端api的端口
- `"FRONT_BASE_PROTOCOL=http"` 前端服务的协议类型
- `"FRONT_BASE_DOMAIN=taigafrontend"` 前端服务的域名或者ip
- `"FRONT_BASE_PORT=80"` 前端服务的端口
- `"MEDIA_URL=/media/"` 后端存储用户文件的uri或url
- `"STATIC_URL=/static/"` 后端网页静态资源的uri或url
- `"EMAIL_HOST=smtp.domain.com"` 后端邮件功能所使用的服务地址
- `"EMAIL_PORT=25"` 后端邮件功能所使用的服务端口
- `"EMAIL_HOST_USER=yourmail@domain.com"` 邮箱账号
- `"EMAIL_HOST_PASSWORD=yourpassword"` 邮箱密码
- `"DEFAULT_FROM_EMAIL=yourmail@domain.com"` 默认的发件人
- `"EMAIL_SUBJECT_PREFIX=taiga-noreplay"` 邮件主题前缀
- `"EMAIL_USE_TLS=False"` ssl功能是否开启，因为多数邮箱服务的ssl功能开启复杂，这里只做测试，所以这里选择了False。

**Taiga-frontend的配置**

- `"BASE_DOMAIN=taigabackend:8000"` 后端api的地址
- `"BASE_PROTOCOL=http"` 后端api使用的协议类型

## 其他配置文件
这些变量均是从taiga的配置文件中得到的，这里为了方便部署所以单独领出来。更多配置可以参考源代码中的如下配置文件
**taiga-backend**
- `taiga-back/settings/common.py` 系统默认配置
- `taiga-back/settings/local.py` 用户自定义配置，如果修改默认配置，在这里重新定义即可

**taiga-frontend**
- `taiga-front/conf/conf.json` 如果修改默认配置，在这里重新定义即可，记得备份。

**其他**
taiga-docker的前端是部署在nginx上的，可以配置nginx的配置。


## 进行初始化
初始化过程需要进入taigabackend容器中

```
docker ps 
```
找到`taigabackend`的容器id

```
docker exec -it /bin/bash
```

这样我们进入到容器中

初始化过程需要两步，初始化数据库和初始化静态文件,如下命令在taigabackend的容器中执行

```
#初始化数据库
sh regenerate.sh

#初始化静态文件
python manage.py collectstatic
```

## 查看界面

登陆taiga的地址[http://localhost:8080/](http://localhost:8080/)即可查看。管理员账户`admin`,密码`123123`

Django的管理界面[http://localhost:8080/admin/](http://localhost:8080/)可以查看数据库元数据。管理员账户`admin`,密码`123123`

## 特殊情况
如果需要将taiga的服务部署在不同的机器或者网段中，则需要注意将如下环境变量配置称为实际的地址

- `"MEDIA_URL=http://taiga-front:port/media/"` 
- `"STATIC_URL=http://taiga-front:port/static/"` 

将后端存储用户文件的uri或url 配置成实际提供文件服务的地址。如果有必要，也是要修改前端nginx代理。

需要了解的是，Taiga中文件或资源地址是由后端生成好后，发送给前端服务的，地址就是由`MEDIA_URL`和`STATIC_URL`决定其前缀。
如`MEDIA_URL=/media/`,则实际的地址为`http://taiga-backend:8001/media/`
如`MEDIA_URL=http//192.168.1.101:8001/media/`，则实际地址还是`http//192.168.1.101:8001/media/`

## docker-compose中环境变量说明

**Postgres的配置**

- `"POSTGRES_HOST=postgresdb"` 数据地址
- `"POSTGRES_DB=taiga"` 数据库名
- `"POSTGRES_USER=taiga"` 数据库登陆用户名
- `"POSTGRES_PASSWORD=taiga"` 数据库登陆密码

**Taiga-backend的配置**

- `"API_BASE_PROTOCOL=http"` 后端api使用的协议类型
- `"API_BASE_DOMAIN=taigabackend"` 后端api对外的域名或者ip
- `"API_BASE_PORT=8000"` 后端api的端口
- `"FRONT_BASE_PROTOCOL=http"` 前端服务的协议类型
- `"FRONT_BASE_DOMAIN=taigafrontend"` 前端服务的域名或者ip
- `"FRONT_BASE_PORT=80"` 前端服务的端口
- `"MEDIA_URL=/media/"` 后端存储用户文件的uri或url
- `"STATIC_URL=/static/"` 后端网页静态资源的uri或url
- `"EMAIL_HOST=smtp.domain.com"` 后端邮件功能所使用的服务地址
- `"EMAIL_PORT=25"` 后端邮件功能所使用的服务端口
- `"EMAIL_HOST_USER=yourmail@domain.com"` 邮箱账号
- `"EMAIL_HOST_PASSWORD=yourpassword"` 邮箱密码
- `"DEFAULT_FROM_EMAIL=yourmail@domain.com"` 默认的发件人
- `"EMAIL_SUBJECT_PREFIX=taiga-noreplay"` 邮件主题前缀
- `"EMAIL_USE_TLS=False"` ssl功能是否开启，因为多数邮箱服务的ssl功能开启复杂，这里只做测试，所以这里选择了False。

**Taiga-frontend的配置**

- `"BASE_DOMAIN=taigabackend:8000"` 后端api的地址
- `"BASE_PROTOCOL=http"` 后端api使用的协议类型

## 其他配置文件
这些变量均是从taiga的配置文件中得到的，这里为了方便部署所以单独领出来。更多配置可以参考源代码中的如下配置文件
**taiga-backend**
- `taiga-back/settings/common.py` 系统默认配置
- `taiga-back/settings/local.py` 用户自定义配置，如果修改默认配置，在这里重新定义即可

**taiga-frontend**
- `taiga-front/conf/conf.json` 如果修改默认配置，在这里重新定义即可，记得备份。

**其他**
taiga-docker的前端是部署在nginx上的，可以通过配置nginx的配置来改变前端的规则。

