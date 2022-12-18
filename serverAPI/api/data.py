from django.http import HttpRequest, HttpResponse
from serverAPI import models
from serverAPI.bc_plugin import bc_plugin
from server.settings import SELF_INFO
from django.utils import timezone
import hashlib
import time
import pymysql

def uploadToCloud(dataHash, round):
    db = pymysql.connect(host="bj-cdb-0tslvdym.sql.tencentcdb.com",port=59568, user="root",password="tjubc12345",database="clouddb")
    
    selfInfo = models.SelfInfo.objects.filter(address=SELF_INFO.get("address"))[0]
    data = models.ShortTermCache.objects.filter(
        owner=SELF_INFO.get("address"),
        create_round__lte = round
    )
    cursor = db.cursor()
    for item in data:
        upload_time = timezone.now()
        create_round = item.create_round
        upload_round = selfInfo.current_round
        loc_x = item.loc_x
        loc_y = item.loc_y
        type = item.type
        data_hash = dataHash
        content = item.content
        
        sql = """
            insert into data
            (upload_time, upload_round, data_hash, content, type, create_round, loc_x, loc_y)
            values
            ("{}" , {}, "{}", "{}", {}, {}, {}, {})
        """.format(
            upload_time,
            upload_round,
            data_hash,
            content,
            type,
            create_round,
            loc_x,
            loc_y
        )

        cursor.execute(sql)
        item.delete()
    db.commit()
    cursor.close()
    db.close()


def getDataFromDB(info):
    for i in range(info.loc_x*2, info.loc_x*2+3):
        for j in range(info.loc_y*2, info.loc_y*2+3):
            raw = models.dataPoint.objects.using('dataDB').filter(
                loc_x=i,
                loc_y=j
            )
            currTime = timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            for item in raw:
                cache = models.ShortTermCache(
                    owner=SELF_INFO.get("address"),
                    create_round = info.current_round,
                    create_time=currTime[0],
                    loc_x=i,
                    loc_y=j,
                    type=item.type,
                    content=item.content,
                    acc_count = item.popularity
                )
                cache.save()


def updateCache(req: HttpRequest) -> HttpResponse:
    info = models.SelfInfo.objects.filter(address=SELF_INFO.get("address"))[0]
    getDataFromDB(info)
    return HttpResponse("ok")


def uploadLongTermData(req: HttpRequest) -> HttpResponse:
    selfInfo = models.SelfInfo.objects.filter(
        address=SELF_INFO.get("address"))[0]
    lastCheckedList = models.CheckPoint.objects.filter(
        owner=selfInfo.address,
        result=1
    ).order_by("-round")
    if len(lastCheckedList) == 0:
        return HttpResponse("no data to upload")
    lastChecked = lastCheckedList[0]
    print("last checked!" + str(lastChecked.round))
    expiredData = models.ShortTermCache.objects.filter(
        owner=selfInfo.address,
        create_round__lte=lastChecked.round
    ).order_by("-acc_count")
    string = ""

    for i in expiredData:
        string += i.content
    input = hashlib.sha256(string.encode()).hexdigest()

    handler = bc_plugin(selfInfo.private_key, "127.0.0.1:"+selfInfo.bc_port)
    while True:
        dataHash = handler.getDataHash(int(lastChecked.round))
        if dataHash["value"] == input:
            break
        time.sleep(1)

    handler.UpdateLongTermCache(input)
    for i in range(0, SELF_INFO.get("CacheRemained")):
        longCache = models.LongTermCache(
            owner=expiredData[i].owner,
            create_time=expiredData[i].create_time,
            create_round=expiredData[i].create_round,
            upload_round=selfInfo.current_round+1,
            loc_x=expiredData[i].loc_x,
            loc_y=expiredData[i].loc_y,
            type=expiredData[i].type,
            data_hash = input,
            content=expiredData[i].content
        )
        longCache.save()

    uploadToCloud(input, lastChecked.round)

    return HttpResponse("ok")


def getDataOrHash(req: HttpRequest) -> HttpResponse:
    info = models.SelfInfo.objects.filter(address=SELF_INFO.get("address"))[0]
    last_update = info.last_updated
    prikey = info.private_key
    port = info.bc_port

    querySet = req.body.get()
    dataSet = []

    for item in querySet:
        start_time = max(item["start_time"], last_update)
        data = models.ShortTermCache.objects.filter(
            type=item["type"],
            loc_x=item["loc_x"],
            loc_y=item["loc_y"],
            create_time__in=[start_time, item["end_time"]]
        )
        for elem in data:
            dataSet.append(elem)

        if item["start_time"] < last_update:
            handler = bc_plugin(prikey, "127.0.0.1"+port)
            dataHashSet = bc_plugin.getDataHash(
                item["start_time"], last_update)
            for elem in dataHashSet:
                dataSet.append(elem)
    return HttpResponse(dataSet)
