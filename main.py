import json
import time
import requests

USER = ""
COOKIE = input("SSID Cookie: ")

pbSess = requests.session()
solSess = requests.session()

pbSess.cookies.set("SSID", COOKIE)

# -- TODO Nu merge, tot da parola invalida
#
#def authPbinfo(user, password):
#  URL = "https://www.pbinfo.ro/ajx-module/php-login.php"
#
#  data = {
#    "user": user,
#    "parola": password
#  }
#  req = pbSess.post(URL, data=data)
#  j = req.json()
#  if req.json()["stare"] == "warning":
#    data["form_token"] = j["form_token"]
#    data["local_ip"] = "1f1cf68e-3f4a-4134-8211-1bc9bbeb8cce.local 2c602033-2d1e-4942-a667-ca90111a95db.local"
#    print(data)
#    req = pbSess.post(URL, data=data)
#
#  print(req.json())

def getPbinfoSolved(user):
  URL = "https://www.pbinfo.ro/ajx-module/profil/json-jurnal.php"

  return len(pbSess.post(URL, params={"user": user}).json()["content"])

def getSolinfoPb():
  return json.loads(open("probleme.json").read())

def getSolinfoSource(name):
  URL_PB = "https://api.solinfo.ro/v2.0/endpoint/page/problema"
  URL_SOL = "https://api.solinfo.ro/v2.0/endpoint/page/problema-solutie"

  pb = solSess.post(URL_PB, data=json.dumps({"name": name}))
  solID = pb.json()["solutions"][0]["id"]
  sol = solSess.post(URL_SOL, data=json.dumps({"solutionId": solID}))

  return sol.json()["content"]

def sendPbinfo(id, source):
  URL = "https://www.pbinfo.ro/ajx-module/php-solutie-incarcare.php"
  
  data = {
    "id": id,
    "pagina": "probleme",
    "limbaj_de_programare": "cpp",
    "sursa": source
  }

  return pbSess.post(URL, data=data).json()

def solveProblem(id, name):
  print(sendPbinfo(id, getSolinfoSource(name)))

probleme = getSolinfoPb()
solved = getPbinfoSolved(USER)
num = int(input("Cate probleme?: "))
for i in range(solved, solved+num):
  solveProblem(probleme[i]["id"], probleme[i]["name"])
  print(i)
