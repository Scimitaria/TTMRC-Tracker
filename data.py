import sys
import json
import getopt
import requests # type: ignore
from io import StringIO
from datetime import date
import pandas as pd # type: ignore
from bs4 import BeautifulSoup as bs # type: ignore

# prevents pandas from cutting data
pd.set_option('display.max_rows',None)

cur_year = date.today().year
days = date.today().timetuple().tm_yday

t3 = t4 = g = False

#flags
try:(lst,args) = getopt.getopt(sys.argv[1:],"a34gr",["all =","t300 =","t400 =","garmin =","reset ="])
except:print("Error parsing flags")
for (opt,val) in lst:
    if opt in ['-a','--all']:
        t3 = t4 = g = True
        break
    if opt in ['-3','--t300']: t3 = True
    if opt in ['-4','--t400']: t4 = True
    if opt in ['-g','--garmin']: g= True
    if opt in ['-r','--reset']:
        with open('standings/T300.json', 'w') as file: json.dump({},file,indent=4)
        with open('standings/T400.json', 'w') as file: json.dump({},file,indent=4)
        with open('standings/Garmin.json', 'w') as file: json.dump({},file,indent=4)
        with open('log.txt', 'w') as f: f.write(str(cur_year))

#overwrite log if new year
with open('log.txt', 'r') as f: log=f.read()
if str(cur_year) not in log:
    with open('standings/T300.json', 'w') as file: json.dump({},file,indent=4)
    with open('standings/T400.json', 'w') as file: json.dump({},file,indent=4)
    with open('standings/Garmin.json', 'w') as file: json.dump({},file,indent=4)
    with open('log.txt', 'w') as f: f.write(str(cur_year))
    log=''

def partialMileage(dist,splits,event):
    if splits == 0: return 0
    match event:
        case "bandera":
            match splits:
                case 2: return 31.1
                case 3: return 52.3
                case 4: return 62.2
                case _: return 0
        case 100: #Rocky 100
            match dist,splits:
                case "100M",3: return 29.1
                case "100M",4: return 40
                case "100M",5: return 49.1
                case "100M",6: return 60
                case "100M",7: return 69.1
                case "100M",8: return 80
                case "100M",9: return 89.1
                case "100M",10: return 100
                case "100K",3: return 31.3
                case "100K",4: return 42.2
                case "100K",5: return 51.2
                case "100K",6: return 62.1
                case _: return 0
        case 50: #Rocky 50
            match dist,splits:
                case "50M",4: return 33.4
                case "50M",5: return 39
                case "50M",6: return 50.1
                case "50K",4: return 31.3
                case _: return 0
        case "hh": #Hells Hills 50M
            match splits:
                case 3: return 50
                case 2: return 33.7
                case _: return 0
        case "pandora":
            match splits:
                case 4: return 52.4
                case 3: return 39.3
                case 2: return 26.2
                case _: return 0
        case "cr": #Cactus Rose
            match splits:
                case 3: return 40.1
                case 4: return 50
                case 5: return 59.9
                case 6: return 75
                case 7: return 90.1
                case 8: return 100
                case _: return 0
        case "wildhare":
            match splits:
                case 6: return 50
                case 5: return 41.7
                case 4: return 33.3
                case _: return 0
        case "mosaic":
            match splits:
                case 9: return 28
                case 10: return 31.1
                case _: return 0
        #Events w/ all splits less than marathon
        case _: return 0

def updateT300():
    page1 = requests.get("http://edsresults.com/cr{}/index.php?search_type=race_results&event=100M&gender=&results_per_page=1000".format(str(cur_year-1)[-2:])).content
    table1 = pd.read_html(StringIO(str(bs(page1,features="lxml").find_all('table',{'id':'data'}))))[0]
    page2 = requests.get("http://edsresults.com/bandera{}/index.php?search_type=race_results&event=100K&gender=&results_per_page=1000".format(str(cur_year)[-2:])).content
    table2 = pd.read_html(StringIO(str(bs(page2,features="lxml").find_all('table',{'id':'data'}))))[0]
    page3 = requests.get("http://edsresults.com/{}rr100/index.php?search_type=race_results&event=100M&gender=&results_per_page=1000".format(str(cur_year))).content
    table3 = pd.read_html(StringIO(str(bs(page3,features="lxml").find_all('table',{'id':'data'}))))[0]
    page4 = requests.get("http://edsresults.com/{}rr100/index.php?search_type=race_results&event=100K&gender=&results_per_page=1000".format(str(cur_year))).content
    table4 = pd.read_html(StringIO(str(bs(page4,features="lxml").find_all('table',{'id':'data'}))))[0]
    tables = [table1,table2,table3,table4]
    for table in tables:
        finishers = table.loc[table['Status']=='Complete']

        for _,table in list(finishers.iterrows()):
            data=str(table).splitlines()[:-1]
            name = (str(data[4].split(" ")[-1])+" "+str(data[5].split(" ")[-1])).lower()

            with open('standings/T300.json', 'r+') as file:
                t300=json.load(file)
                #update mileages
                if name in t300: t300[name] += 1
                else: t300[name] = 1
                sorted_json=dict(sorted(t300.items(), key=lambda item: item[1], reverse=True))
                file.seek(0)
                file.truncate()
                json.dump(sorted_json, file, indent=4)
def updateT400(t,dist,event):
    finishers = t.loc[t['Status']=='Complete']
    for _,table in list(finishers.iterrows()):
        data=str(table).splitlines()[:-1]
        name = (str(data[4].split(" ")[-1])+" "+str(data[5].split(" ")[-1])).lower()
        mileage=0
        if   "100M" in dist: mileage+=100
        elif "100K" in dist: mileage+=62.1
        elif "50M" in dist: mileage+=50
        elif "50K" in dist: mileage+=31.1

        with open('standings/T400.json', 'r+') as file:
            t400=json.load(file)
            #update mileages
            if name in t400: t400[name] += mileage
            else: t400[name] = mileage
            sorted_json=dict(sorted(t400.items(), key=lambda item: item[1], reverse=True))
            file.seek(0)
            file.truncate()
            json.dump(sorted_json, file, indent=4)

    incomplete = t.loc[t['Status']=='DNF']
    for _,table in list(incomplete.iterrows()):
        data=str(table).splitlines()[:-1]
        name = (str(data[4].split(" ")[-1])+" "+str(data[5].split(" ")[-1])).lower()
        i = 12 if event in [100,50] else 10
        mileage=partialMileage(dist,int(data[i].split(" ")[-1]),event)
        if mileage > 0:
            with open('standings/T400.json', 'r+') as file:
                t400=json.load(file)
                #update mileages
                if name in t400: t400[name] += mileage
                else: t400[name] = mileage
                sorted_json=dict(sorted(t400.items(), key=lambda item: item[1], reverse=True))
                file.seek(0)
                file.truncate()
                json.dump(sorted_json, file, indent=4)
def updateGarmin(table,dist):
    finishers = table.loc[table['Status']=='Complete']

    for _,table in list(finishers.iterrows()):
        data=str(table).splitlines()[:-1]
        name = (str(data[4].split(" ")[-1])+" "+str(data[5].split(" ")[-1])).lower()
        points=0
        if any(word in dist for word in ['100','52.4M','50M']): points+=4
        elif any(word in dist for word in ['50K','25M','20M','25K','13.1M','10M']): points+=3
        elif any(word in dist for word in ['15K','8M','10K','5M']): points+=2
        else: points += 1

        with open('standings/Garmin.json', 'r+') as file:
            garmin=json.load(file)
            #update mileages
            if name in garmin: garmin[name] += points
            else: garmin[name] = points
            sorted_json=dict(sorted(garmin.items(), key=lambda item: item[1], reverse=True))
            file.seek(0)
            file.truncate()
            json.dump(sorted_json, file, indent=4)

def getResults(event,dist):
    if not (t4 or g): return
    url = "http://edsresults.com/{}{}/index.php?search_type=race_results&event={}&gender=&results_per_page=1000/".format(event,str(cur_year)[-2:],dist)
    page = requests.get(url).content
    table = pd.read_html(StringIO(str(bs(page,features="lxml").find_all('table',{'id':'data'}))))[0]
    if t4 and event not in ["hippo","mellow"]: updateT400(table,dist,event)
    if  g: updateGarmin(table,dist)
def getResultsRocky(event,dist):
    if not (t4 or g): return
    url = "http://edsresults.com/{}rr{}/index.php?search_type=race_results&event={}&gender=&results_per_page=1000".format(cur_year,event,dist)
    page = requests.get(url).content
    table = pd.read_html(StringIO(str(bs(page,features="lxml").find_all('table',{'id':'data'}))))[0]
    if t4: updateT400(table,dist,event)
    if  g: updateGarmin(table,dist)

if t3: updateT300()

#Get Bandera results
if days > 20:
    if not 'bandera' in log:
        getResults("bandera","100K")
        getResults("bandera","50K")
        getResults("bandera","Saturday+50K")
        with open('log.txt', 'a') as f: f.write('bandera')
    if g and not 'banderag' in log: 
        getResults("bandera","25K")
        with open('log.txt', 'a') as f: f.write('banderag')

#Get Rocky Raccoon results
if days > 50:
    if not 'rocky' in log:
        getResultsRocky(100,'100M')
        getResultsRocky(100,'100K')
        getResultsRocky(50,'50M')
        getResultsRocky(50,'50K')
        with open('log.txt', 'a') as f: f.write('rocky')
    if g and not 'rockyg' in log:
        getResultsRocky(50,'13.1M')
        with open('log.txt', 'a') as f: f.write('rockyg')

#Get Great Springs Austin results
if days > 75:
    if not 'austin' in log: 
        getResults("austin",'50K')
        with open('log.txt', 'a') as f: f.write('austin')
    if g and not 'austing' in log:
        getResults("austin",'26.2M')
        getResults("austin",'13.1M')
        getResults("austin",'10K')
        getResults("austin",'5K')
        with open('log.txt', 'a') as f: f.write('austing')

#Get Hippo results
if days > 90 and g and not 'hippo' in log:
    getResults("hippo","26.2M")
    getResults("hippo","13.1M")
    getResults("hippo","10K")
    getResults("hippo","5K")
    with open('log.txt', 'a') as f: f.write('hippo')

#Get Hells Hills results
if days > 100:
    if not 'hellshills' in log:
        getResults("hh",'50M')
        getResults("hh",'50K')
        with open('log.txt', 'a') as f: f.write('hellshills')
    if g and not 'hellshillsg' in log:
        getResults("hh",'25K')
        getResults("hh",'10K')
        with open('log.txt', 'a') as f: f.write('hellshillsg')

#Get Pandora results
if days > 120:
    if not 'pandora' in log:
        getResults("rox",'52.4M')
        with open('log.txt', 'a') as f: f.write('pandora')
    if g and not 'pandorag' in log:
        getResults("rox",'26.2M')
        getResults("rox",'13.1M')
        getResults("rox",'8M')
        getResults("rox",'4M')
        with open('log.txt', 'a') as f: f.write('pandorag')

#Get Dirt Fest results
if days > 135: 
    if not 'dirtfest' in log:
        getResults("dirtfest",'50K')
        with open('log.txt', 'a') as f: f.write('dirtfest')
    if g and not 'dirtfestg' in log:
        getResults("dirtfest",'25K')
        getResults("dirtfest",'5M')
        with open('log.txt', 'a') as f: f.write('dirtfestg')

#Get River's Edge results
if days > 150: 
    if not 'edge' in log:
        getResults("edge",'50K')
        with open('log.txt', 'a') as f: f.write('edge')
    if g and not 'edgeg' in log:
        getResults("edge",'25K')
        getResults("edge",'10M')
        getResults("edge",'5M')
        with open('log.txt', 'a') as f: f.write('edgeg')

#Get Great Springs Canyon Lake results
if days > 160: 
    if not 'canyon' in log:
        getResults("canyonlake",'50K')
        with open('log.txt', 'a') as f: f.write('canyon')
    if g and not 'canyong' in log:
        getResults("canyonlake",'25K')
        getResults("canyonlake",'10K')
        getResults("canyonlake",'5K')
        with open('log.txt', 'a') as f: f.write('canyong')

#Get Mellow results
if days > 260 and g and not 'mellow' in log:
    getResults("mellow",'5K')
    getResults("mellow",'10K')
    getResults("mellow",'13.1M')
    getResults("mellow",'26.2M')
    with open('log.txt', 'a') as f: f.write('mellow')

#Get Trailway results
if days > 290: 
    if not 'trailway' in log:
        getResults("trailway",'50K')
        with open('log.txt', 'a') as f: f.write('trailway')
    if g and not 'trailwayg' in log:
        getResults("trailway",'5K')
        getResults("trailway",'10K')
        getResults("trailway",'13.1M')
        getResults("trailway",'26.2M')
        with open('log.txt', 'a') as f: f.write('trailwayg')

#Get Cactus Rose results
if days > 305:
    if not 'cactus' in log:
        getResults("cr",'100M')
        getResults("cr",'50M')
        with open('log.txt', 'a') as f: f.write('cactus')
    if g and not 'cactusg' in log:
        getResults("cr",'25M')
        getResults("cr",'5M')
        with open('log.txt', 'a') as f: f.write('cactusg')

#Get Wild Hare results
if days > 325:
    if not 'wildhare' in log:
        getResults("wildhare",'50M')
        getResults("wildhare",'50K')
        with open('log.txt', 'a') as f: f.write('wildhare')
    if g and not 'wildhareg' in log:
        getResults("wildhare",'25K')
        getResults("wildhare",'10K')
        with open('log.txt', 'a') as f: f.write('hellshillsg')

#Get Mosaic results
if days > 345: 
    if not 'mosaic' in log:
        getResults("mosaic",'50K')
        with open('log.txt', 'a') as f: f.write('mosaic')
    if g and not 'mosaicg' in log:
        getResults("mosaic",'5K')
        getResults("mosaic",'10K')
        getResults("mosaic",'15K')
        getResults("mosaic",'13.1M')
        getResults("mosaic",'26.2M')
        with open('log.txt', 'a') as f: f.write('mosaicg')
