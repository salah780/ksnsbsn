import requests
import time
url = "https://freedl.ink/api/upload/url"
params = {
    "key": "107702nbd8y3tgn5c4nds",
    "url": "http://154.194.55.233:8080/series/Atta-Khattab/QMdeaW2OiVmoEx/320638.mp4?token=cbfdzU.aazyH.X.X.ydcbHHyfad.X.y.EG.mp4.25f5cdc647d4912ef4d6fa0fce16ec3420a2757575cc96c0bafc5dc9a003e1a8.8452.VGVsZWNvbSBFZ3lwdA==.",
    "fld_id": 0
}
response = requests.get(url, params=params)
data = response.json()

if "result" in data and "filecode" in data["result"]:
    file_code = data["result"]["filecode"]
    download_link = f"https://frdl.is/{file_code}"
else:
    print("Error:", data)
url = "https://freedl.ink/api/file/rename"
params = {
    "file_code": {file_code},
    "name": "madah episode 94897.mp4",
    "key": "107702nbd8y3tgn5c4nds"
}
time.sleep(15)
response = requests.get(url, params=params)
print(download_link)