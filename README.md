# CompileService
接收上传一个py文件，把它用cython编译成.so文件，再传递给接收的程序。

可以用作python程序的加密上传。

## 设置
运行这个服务需要
* 自己生成证书（crt文件和key文件），放到dockerConfig.json中配置的路径下
* 安装sdk，以及必要的python包
* 安装supervisor，用来启动服务

也可以直接下载我们预先准备好的docker file:

1. 下载compile镜像

   wget http://updateapi.yunkuanke.com/download/dockerimages/CompileService.tar.gz

2. 导入镜像

   docker load -i CompileService.tar.gz

3. 启动compile service容器 (注：name表示容器名称，-p映射端口)

   docker run -d -p 8889:8889 --name=lzjf_compileservice -it compileservice_opensource:docker bash

4. 检查compile服务

   docker ps -a |grep lzjf_compileservice
   
## 使用

使用服务的时候，需要把客户端的配置文件CloudQuant.xml中的

\<entry key="Business.CompileServiceUrl" value="http://compile.yunkuanke.com/" /\>

改为您自己的compile service的地址，比如：

\<entry key="Business.CompileServiceUrl" value="http://192.168.1.111：8889/" /\>
