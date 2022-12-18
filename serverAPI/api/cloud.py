from django.http import HttpRequest, HttpResponse
from serverAPI import models
from serverAPI.bc_plugin import bc_plugin
from server.settings import SELF_INFO
import requests
import json

def sendCloudCheckData(req: HttpRequest) -> HttpResponse:
    print("sendCloudCheckData!")
    data = models.LongTermCache.objects.filter(
        owner = SELF_INFO.get("address")
    )
    selfInfo = models.SelfInfo.objects.filter(
        address = SELF_INFO.get("address")
    )[0]
    dataSet = []
    if len(data) == 0:
        print("no data to check!")
        return HttpResponse("no data to check!")
    
    for i in data:
        dataSet.append({
            "create_round": i.create_round,
            "loc_x": i.loc_x,
            "loc_y": i.loc_y,
            "type": i.type,
            "content": i.content,
            "data_hash": i.data_hash,
        })
    input = {
        "dataSet":json.dumps(dataSet),
        "address":SELF_INFO.get("address"),
        "chain_id":selfInfo.chain_id
    }
    url = "http://"+req.POST.get("host")+"/cloud/cloudCheck"
    requests.post(url, input)
    return HttpResponse("ok")
