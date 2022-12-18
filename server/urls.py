"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from serverAPI.api import car, cloud, node, sys, data
urlpatterns = [
    # 系统相关
    path('sys/initialize', sys.initialize),  # 完成系统初始化
    path('sys/getData', data.updateCache),  # 获取数据列表
    path('sys/manualStart', sys.manualStart), # 手动开始检查
    path('sys/startRound', sys.startRound),  # 接收服务器通知，开始回合

    # 数据相关API
    path('data/uploadLongTermData',data.uploadLongTermData),
    path('data/uploadToCloud',data.uploadToCloud),
    
    # 汽车相关API
    path('car/getDataFromNode', data.getDataOrHash),  # 从节点获取数据

    # 节点相关API
    path('node/declareNodeCheck', node.reqCheckDataFromNode),  # 接受节点发起的检查请求
    path('node/reqCheckDataFromNode', node.sendNodeCheckData),  # 为节点检查提供数据
    path('node/sendNodeCheckData', node.check),  # 接受节点数据，进行检查


    # 云端相关API
    path('cloud/reqCloudCheck', cloud.sendCloudCheckData),  # 接受服务器发起的云端检查请求
    
]
