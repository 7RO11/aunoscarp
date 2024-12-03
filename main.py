from bs4 import BeautifulSoup
import requests
import json
import re

item = {
      "name": "",
      "min": 220,
      "max": 1,
      "type": "",
      "blurb": "",
      "stats": {
        "ql": {
          "value": "",
          "quality": "",
        },
        "dual": {
          "value": "",
          "quality": "",
        },
        "aSpeed": {
          "value": "",
          "quality": "",
        },
        "rSpeed": {
          "value": "",
          "quality": "",
        },
        "range": {
          "value": "",
          "quality": "",
        },
        "minDamage": {
          "value": "",
          "quality": "",
        },
        "maxDamage": {
          "value": "",
          "quality": "",
        },
        "critMod": {
          "value": "",
          "quality": "",
        },
        "attackCap": {
          "value": "",
          "quality": "",
        },
        "init": {
          "value": "",
          "quality": "",
        },
        "multi": {
          "value": "",
          "quality": "",
        },
        "specials": {
          "value": "",
          "quality": "",
        },
        "reqs": {
        },
        "mods": {
        },
        
      },
      "profs": []
    }


toScrape = "https://auno.org/ao/db.php?id=204750"
page = requests.get(toScrape)
item["auno"] = toScrape

soup = BeautifulSoup(page.content, "html.parser")

name = soup.find("legend").text
item["name"] = name

slots = soup.find("td", string="Slot").parent.text

if slots.find("Right hand") != -1 and slots.find("Left hand") != -1:
    item["stats"]["dual"]["value"] = "Yes"
else:
    item["stats"]["dual"]["value"] = "No"

aspeed = re.findall(r"\d\.?\d*s", soup.find("td", string="Attack time").parent.text)[0]
item["stats"]["aSpeed"]["value"] = aspeed
rspeed = re.findall(r"\d\.?\d*s", soup.find("td", string="Recharge time").parent.text)[0]
item["stats"]["rSpeed"]["value"] = rspeed
range = re.findall(r"\d* m", soup.find("td", string="Range").parent.text)[0]
item["stats"]["range"]["value"] = range
minD = re.findall(r"\d*-", soup.find("td", string="Damage").parent.text)[0]
item["stats"]["minDamage"]["value"] = minD[:-1]
maxD = re.findall(r"-\d*", soup.find("td", string="Damage").parent.text)[0]
item["stats"]["maxDamage"]["value"] = maxD[1:]
crit = re.findall(r"\(\d*\)", soup.find("td", string="Damage").parent.text)[0]
item["stats"]["critMod"]["value"] = crit[1:-1]
if soup.find("td", string="Attack rating cap"):
  mbs = re.findall(r"\d*$", soup.find("td", string="Attack rating cap").parent.text)[0]
  item["stats"]["attackCap"]["value"] = mbs
init = re.findall(r"\w*\sinit", soup.find("td", string="Initiative skill").parent.text)[0]
item["stats"]["init"]["value"] = init[:-5]

if soup.find("td", string="Multi ranged"):
    mulr = re.findall(r"\d*$", soup.find("td", string="Multi ranged").parent.text)[0]
    item["stats"]["multi"]["value"] = mulr

if soup.find("td", string="Multi melee"):
    mulr = re.findall(r"\d*$", soup.find("td", string="Multi melee").parent.text)[0]
    item["stats"]["multi"]["value"] = mulr

sps = soup.find("td", string="Can").parent.text
specials = []
if sps.find("Fast Attack") != -1:
    specials.append("Fast Attack")
if sps.find("Fling Shot") != -1:
    specials.append("Fling Shot")
if sps.find("Burst") != -1:
    specials.append("Burst")
if sps.find("Full Auto") != -1:
    specials.append("Full Auto")
if sps.find("Aimed Shot") != -1:
    specials.append("Aimed Shot")
if sps.find("Sneak Attack") != -1:
    specials.append("Sneak Attack")
if sps.find("Brawl") != -1:
    specials.append("Brawl")
if sps.find("Dimach") != -1:
    specials.append("Dimach")

item["stats"]["specials"]["value"] = (", ").join(specials)

reqs = soup.find("td", string="To Equip").parent.parent.text
numbhead = re.findall("User", reqs)

reqN = []
reqV = []

for index, bs in enumerate(numbhead):
  req = re.findall(r"User\n.*", reqs)[index][5:]
  reqN.append(req)

for index, bs in enumerate(numbhead):
  req = re.findall(r">=.*|==.*", reqs)[index][3:]
  reqV.append(req)

item["type"] = reqN[0]

for index, req in enumerate(reqN):
    item["stats"]["reqs"][req] = {"value": reqV[index], "quality": ""}


testmods = soup.find("td", string="On Equip")

if testmods:
  mods = soup.find("td", string="On Equip").parent.parent.text
  numbhead = re.findall("User", mods)

  reqN = []
  reqV = []

  for index, bs in enumerate(numbhead):
    req = re.findall(r"Modify\n.*", mods)[index][7:]
    reqN.append(req)
    
  for index, bs in enumerate(numbhead):
    req = re.findall(r"\d+", mods)[index]
    reqV.append(req)
    


  for index, req in enumerate(reqN):
      item["stats"]["mods"][req] = {"value": reqV[index], "quality": ""}

# class stereotypes
if item["type"] == "1h Blunt":
  item["profs"].append("Enforcer")
  item["profs"].append("Meta-Physicist")

if item["type"] == "2h Blunt":
  item["profs"].append("Enforcer")
  item["profs"].append("Meta-Physicist")

if item["type"] == "1h Edged":
  item["profs"].append("Enforcer")
  item["profs"].append("Adventurer")

if item["type"] == "2h Edged":
  item["profs"].append("Enforcer")
  item["profs"].append("Keeper")

if item["type"] == "2h Edged":
  item["profs"].append("Enforcer")
  item["profs"].append("Keeper")

if item["type"] == "Pistol":
  item["profs"].append("Adventurer")
  item["profs"].append("Bureaucrat")
  item["profs"].append("Doctor")
  item["profs"].append("Engineer")
  item["profs"].append("Meta-Physicist")
  item["profs"].append("Nano-technician")

if item["type"] == "Smg":
  item["profs"].append("Fixer")
  item["profs"].append("Soldier")

if item["type"] == "Assault rifle":
  item["profs"].append("Soldier")

if item["type"] == "Rifle":
  item["profs"].append("Agent")

if item["type"] == "Martial arts":
  item["profs"].append("Trader")
  item["profs"].append("Martial Artist")

if item["type"] == "Piercing":
  item["profs"].append("Shade")

if item["type"] == "Shotgun":
  item["profs"].append("Trader")


jsoneditem = json.dumps(item)
f = open("dump.json", "w")
f.write(jsoneditem)
f.close()