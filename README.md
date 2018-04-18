# CompileService
接收上传一个py文件，把它用cython编译成.so文件。可以传递给接收的程序，或是返回编译后的so文件以供下载。

由于编译后不可反推出原python代码，可以用作python程序的加密用途。

为了使用户明白我们加密的过程，我们在GitHub内开放了源代码。如不需要看源代码展示，可直接使用服务，以下为使用的步骤：

## 安装docker环境
* 如果使用的系统是win8/win10 x64 专业版（带hyper-v支持），请下载win10环境下的docker安装文件： http://updateapi.yunkuanke.com/download/dockerimages/win10-docker.zip （366M）。然后按照压缩包内的安装说明文档（win10docker安装.docx）进行安装。
* 如果使用的是win8/win10 x64 的非专业版、以及win7 x64等不支持hyper-v的64位系统，请下载win7环境下的docker安装文件： http://updateapi.yunkuanke.com/download/dockerimages/win7-docker.zip （256M）。然后按照压缩包内的安装说明文档（win7环境下安装docker安装.docx）进行安装。
* 32位windows系统不支持安装docker环境。
* 64位linux系统可自行安装docker环境。

## 下载docker镜像并使用
    可以从 http://updateapi.yunkuanke.com/download/dockerimages/CompileService.tar.gz （约1.3G）下载最新的docker镜像并解压，然后按照说明文档（Docker CompileSvc使用文档.docx）进行配置和使用。
