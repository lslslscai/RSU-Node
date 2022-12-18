from django.http import HttpRequest, HttpResponse
from serverAPI import models
from serverAPI.bc_plugin import bc_plugin
from server.settings import SELF_INFO
import requests
import time
from serverAPI.api.node import declareNodeCheck
from serverAPI.api.car import declarePosCheck
from serverAPI.api.data import getDataFromDB
from django.utils import timezone
import pymysql


def initialize(req: HttpRequest) -> HttpResponse:

    if not len(models.SelfInfo.objects.filter(address=SELF_INFO.get("address"))) == 0:
        return HttpResponse("server: already initialized!")

    handler = bc_plugin(SELF_INFO.get("private_key"),
                        "127.0.0.1:"+str(SELF_INFO.get("bc_port")))

    chain_id = handler.aelfChain.get_chain_id()
    api = "http://"+SELF_INFO.get("server")+"/node/nodeRegister"
    data = {
        "address": SELF_INFO.get("address"),
        "private_key": SELF_INFO.get("private_key"),
        "loc_x": SELF_INFO.get("loc_x"),
        "loc_y": SELF_INFO.get("loc_y"),
        "chain_id": str(chain_id),
        "host": req.get_host()
    }

    registerReq = requests.post(api, data=data)

    if registerReq.text.find("serverException") >= 0:
        return HttpResponse("node("+SELF_INFO.get("address")+"): "+registerReq.text)

    currTime = registerReq.text.split("#")[1]
    serverSign = registerReq.text.split("#")[2]

    input = {
        "BasicInfo": {
            "RegTime": currTime,
            "ServerSign": serverSign,
            "Addr": SELF_INFO.get("address")
        },
        "AdjInfo": SELF_INFO.get("AdjList")
    }
    id = handler.Initialize(input)

    try:
        info = models.SelfInfo(
            reg_time=currTime,
            address=SELF_INFO.get("address"),
            private_key=SELF_INFO.get("private_key"),
            loc_x=SELF_INFO.get("loc_x"),
            loc_y=SELF_INFO.get("loc_y"),
            chain_id=chain_id,
            current_round=0,
            bc_port=SELF_INFO.get("bc_port"),
            last_updated=currTime,
            round_time=currTime,
            node_status=SELF_INFO.get("node_status"),
            data_status=SELF_INFO.get("data_status"),
        )
        info.save()

        for item in SELF_INFO.get("AdjList"):
            adjList = models.AdjInfo(
                selfAddr=SELF_INFO.get("address"),
                destAddr=item[0],
                nodeIP=item[1]
            )
            adjList.save()
        return HttpResponse("node("+SELF_INFO.get("address")+"): "+"OK")
    except Exception as e:
        return HttpResponse("node("+SELF_INFO.get("address")+"): "+"dbException!\n"+str(e))


def startRound(req: HttpRequest) -> HttpResponse:
    # 查询自身信息，更新轮数
    info = models.SelfInfo.objects.filter(address=SELF_INFO.get("address"))[0]
    info.current_round += 1
    info.round_time = timezone.now()
    prikey = info.private_key
    port = info.bc_port
    info.save()

    # 确认上回合的检查情况
    url = "http://"+SELF_INFO.get("server")+"/sys/getCheckResult"
    data = {
        "chain_id": info.chain_id,
        "address": info.address
    }
    result = requests.post(url, data)
    print("lastTurn:"+result.text)
    if int(result.text) == 1:
        print("passed!")
        info.last_updated = timezone.now()
        checkpt = models.CheckPoint.objects.filter(
            owner=info.address,
            round=info.current_round-1
        )[0]
        checkpt.result = 1
        checkpt.save()

    # 更新即时缓存
    if info.data_status == 0:
        getDataFromDB(info)

    # 访问区块链，获取检查列表
    handler = bc_plugin(prikey, "127.0.0.1:"+str(port))
    time.sleep(4)
    checkList = handler.GetCheckResult(info.current_round)

    # 根据不同情况，选择需要进行的操作
    if "NodeCheckList" in checkList.keys() and\
            info.address in checkList["NodeCheckList"].keys():
        declareNodeCheck(handler, req.get_host())
    if "CarPosCheckList" in checkList.keys() and\
            info.address in checkList["CarPosCheckList"].keys():
        declarePosCheck()
    info.save()
    return HttpResponse("ok")


def manualStart(req: HttpRequest) -> HttpResponse:
    info = models.SelfInfo.objects.filter(address=SELF_INFO.get("address"))[0]
    prikey = info.private_key
    port = info.bc_port
    info.save()

    handler = bc_plugin(prikey, "127.0.0.1:"+port)
    checkList = handler.GetCheckResult(info.current_round)

    # 根据不同情况，选择需要进行的操作
    if "NodeCheckList" in checkList.keys() and\
            info.address in checkList["NodeCheckList"].keys():
        declareNodeCheck(handler, req.get_host())
    if "CarPosCheckList" in checkList.keys() and\
            info.address in checkList["CarPosCheckList"].keys():
        declarePosCheck()
    return HttpResponse("ok")


def changeStatus(req: HttpRequest) -> HttpResponse:
    selfInfo = models.SelfInfo.objects.filter(
        address=SELF_INFO.get("address")
    )[0]
    selfInfo.node_status = int(req.POST.get("node_status"))
    selfInfo.data_status = int(req.POST.get("data_status"))
    if int(req.POST.get("data_status")) >= 1:
        localData = models.ShortTermCache.objects.filter(
            owner=SELF_INFO.get("address")
        )
        for data in localData:
            data.content = "-1"
            data.save()
    if int(req.POST.get("data_status")) >= 2:
        cloudData = models.LongTermCache.objects.filter(
            owner=SELF_INFO.get("address")
        )
        for data in cloudData:
            data.content = "-1"
            data.save()
    selfInfo.save()
    return HttpResponse("ok")


def repairLongTermCache(info):
    dataSet = models.LongTermCache.objects.filter(
        owner = SELF_INFO.get("address")
    )
    db = pymysql.connect(host="bj-cdb-0tslvdym.sql.tencentcdb.com",
                         port=59568, user="root", password="tjubc12345", database="clouddb")
    cursor = db.cursor()
    for i in dataSet:
        sql = """
            select content from data where
            loc_x = {} and
            loc_y = {} and
            type = {} and
            create_round = {};
        """.format(
            i.loc_x,
            i.loc_y,
            i.type,
            i.create_round
        )
        cursor.execute(sql)
        res = cursor.fetchone()
        i.content = res[0]
        i.save()

def repair(req: HttpRequest) -> HttpResponse:
    selfInfo = models.SelfInfo.objects.filter(
        address=SELF_INFO.get("address")
    )[0]
    selfInfo.node_status = 0
    selfInfo.data_status = 0
    getDataFromDB(selfInfo)
    
    repairLongTermCache(selfInfo)
    return HttpResponse("ok")
