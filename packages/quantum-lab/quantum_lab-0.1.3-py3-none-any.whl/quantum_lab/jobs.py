import requests
import json

def create( 
        userID, 
        uploadType, 
        shot, 
        resourceId, 
        filePath, 
        volumeName, 
        resourceName
    ):
    url = "http://sdt-api.qcc.svc.cluster.local"
    url_path = f"{url}/qcc/job/notebook"

    headers = {
        "Content-Type": "application/json",
        "email": userID,
    }

    data = json.dumps({
        "uploadType": uploadType,
        "shot": shot,
        "resourceId": resourceId,
        "filePath": filePath,
        "volumeName": volumeName,
        "resourceName": resourceName
    })

    response = requests.post(f"{url_path}", headers=headers, data=data) 

    print("[Info] Created job / ",response.text, flush=True)

    return response.text

def getList():
    url = "http://sdt-api.qcc.svc.cluster.local"
    url_path = f"{url}/qcc/jobs"

    # params = {
    #     "volumeName": volumeName,
    #     "hostPath": hostPath
    # }

    response = requests.get(f"{url_path}") # , params=params)

    print("[Job LIST] ", response.text, flush=True)

    return response.text

# def getJob():
# def delete():

