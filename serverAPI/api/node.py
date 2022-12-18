from django.http import HttpRequest, HttpResponse
from serverAPI import models
from serverAPI.bc_plugin import bc_plugin
from server.settings import SELF_INFO
import hashlib
import json
import requests
import time
from datetime import datetime


def declareNodeCheck(handler, host) -> HttpResponse:
    print("declareNodeCheck!")
    selfInfo = models.SelfInfo.objects.filter(
        address=SELF_INFO.get("address"))[0]
    AdjList = models.AdjInfo.objects.filter(selfAddr=SELF_INFO.get("address"))

    # addr = "http://127.0.0.1:8002/node/declareNodeCheck"
    data = {
        "loc_x": selfInfo.loc_x,
        "loc_y": selfInfo.loc_y,
        "host": host
    }
    info = models.SelfInfo.objects.filter(address=SELF_INFO.get("address"))[0]
    prikey = info.private_key
    port = info.bc_port
    handler = bc_plugin(prikey, "127.0.0.1:"+port)
    dataSet = models.ShortTermCache.objects.filter(
        owner=SELF_INFO.get("address"),
        loc_x__gte=float(selfInfo.loc_x)*2,
        loc_x__lte=float(selfInfo.loc_x)*2+2,
        loc_y__gte=float(selfInfo.loc_y)*2,
        loc_y__lte=float(selfInfo.loc_y)*2+2,
    ).order_by("-acc_count")
    string = ""
    for i in dataSet:
        print(i.content, i.acc_count)
        string += i.content
    input = hashlib.sha256(string.encode()).hexdigest()
    checkpt = models.CheckPoint(
        owner=selfInfo.address,
        round=selfInfo.current_round,
        data_hash=input,
        result=0
    )
    checkpt.save()
    handler.DeclareNodeCheck(input)

    # res = requests.post(addr, data)
    for node in AdjList:
        addr = "http://"+node.nodeIP+"/node/declareNodeCheck"
        res = requests.post(addr, data)

    return HttpResponse("ok")


def reqCheckDataFromNode(req: HttpRequest) -> HttpResponse:
    print("reqCheckDataFromNode!")
    dest_loc = (req.POST.get("loc_x"), req.POST.get("loc_y"))
    print(dest_loc)
    selfData = models.ShortTermCache.objects.filter(
        owner=SELF_INFO.get("address"),
        loc_x__gte=float(dest_loc[0])*2,
        loc_x__lte=float(dest_loc[0])*2+2,
        loc_y__gte=float(dest_loc[0])*2,
        loc_y__lte=float(dest_loc[0])*2+2,
    ).values_list("loc_x", "loc_y").distinct()
    dataLoc = []
    for i in selfData:
        dataLoc.append((i[0], i[1]))
    data = {
        "dataLoc": json.dumps(dataLoc),
        "host": req.get_host()
    }
    print(data)
    url = "http://"+req.POST.get("host")+"/node/reqCheckDataFromNode"
    ret = requests.post(url, data)
    return HttpResponse("ok")


def check(req: HttpRequest) -> HttpResponse:
    print("check!")
    dataSet = json.loads(req.POST.get("content"))
    result = True
    for data in dataSet:
        localData = models.ShortTermCache.objects.filter(
            owner=SELF_INFO.get("address"),
            loc_x=data["loc_x"],
            loc_y=data["loc_y"],
            type=data["type"],
            content=data["content"],
            create_time__gte=datetime.strptime(
                data["create_time"], "%Y-%m-%d %H:%M:%S")
        )
        if len(localData) == 0:
            result = False
            break

    info = models.SelfInfo.objects.filter(address=SELF_INFO.get("address"))[0]
    prikey = info.private_key
    port = info.bc_port
    handler = bc_plugin(prikey, "127.0.0.1:"+port)
    addr = models.AdjInfo.objects.filter(
        nodeIP=req.POST.get("host"))[0].destAddr
    print(addr)
    input = {
        "To": addr,
        "Result": result,
        "Round": info.current_round
    }
    time.sleep(4)
    handler.ReciteNode(input)

    url = "http://"+SELF_INFO.get("server")+"/node/recite"
    data = {
        "chain_id": info.chain_id,
        "checker_address": info.address,
        "checked_address": addr
    }

    res = requests.post(url, data)
    return HttpResponse("ok")


def sendNodeCheckData(req: HttpRequest) -> HttpResponse:
    reqData = json.loads(req.POST.get("dataLoc"))
    print("sendNodeCheckData!")
    content = []
    for point in reqData:
        print("point"+str(point))
        dataSet = models.ShortTermCache.objects.filter(
            owner=SELF_INFO.get("address"), loc_x=point[0], loc_y=point[1]
        )
        for data in dataSet:
            content.append({
                "loc_x": data.loc_x,
                "loc_y": data.loc_y,
                "type": data.type,
                "content": data.content,
                "create_time": data.create_time.strftime("%Y-%m-%d %H:%M:%S")
            })
    data = {
        "content": json.dumps(content),
        "host": req.get_host()
    }
    url = req.POST.get("host")
    res = requests.post("http://"+url+"/node/sendNodeCheckData", data)
    return HttpResponse("ok")
