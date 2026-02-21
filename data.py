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

t3 = t4 = g = False

#flags
try:(lst,args) = getopt.getopt(sys.argv[1:],"a34g",["all =","t300 =","t400 =","garmin ="])
except:print("Error parsing flags")
for (opt,val) in lst:
    if opt in ['-a','--all']:
        t3 = t4 = g = True
        break
    if opt in ['-3','--t300']: t3 = True
    if opt in ['-4','--t400']: t4 = True
    if opt in ['-g','--garmin']: g= True

#Create empty JSON data
if t3: 
    with open('standings/T300.json', 'w') as file: json.dump({},file,indent=4)
if t4: 
    with open('standings/T400.json', 'w') as file: json.dump({},file,indent=4)
if  g: 
    with open('standings/Garmin.json', 'w') as file: json.dump({},file,indent=4) 

cur_year = date.today().year
days = date.today().timetuple().tm_yday

def partialMileage(dist,splits):
    #TODO: figure out the mess that is 100M and 50M
    #TODO: make sure all 100K and 50K splits are equal
    m=0
    if splits == 0: return 0
    elif '100K' in dist: m = (splits/4)*62.1
    elif '50K' in dist: m = (splits/2)*31.1
    return 0 if m < 26.2 else m

def updateT300():
    page1 = requests.get("http://edsresults.com/cr{}/index.php?search_type=race_results&event=100M&gender=&results_per_page=1000".format(str(cur_year-1)[-2:])).content
    table1 = pd.read_html(StringIO(str(bs(page1,features="lxml").find_all('table',{'id':'data'}))))[0]
    page2 = requests.get("http://edsresults.com/bandera{}/index.php?search_type=race_results&event=100K&gender=&results_per_page=1000".format(str(cur_year)[-2:])).content
    table2 = pd.read_html(StringIO(str(bs(page2,features="lxml").find_all('table',{'id':'data'}))))[0]
    page3 = requests.get("http://edsresults.com/{}rr100/index.php?search_type=race_results&event=100M&gender=&results_per_page=1000".format(str(cur_year))).content
    table3 = pd.read_html(StringIO(str(bs(page3,features="lxml").find_all('table',{'id':'data'}))))[0]
    page4 = requests.get("http://edsresults.com/{}rr100/index.php?search_type=race_results&event=100K&gender=&results_per_page=1000".format(str(cur_year))).content
    table4 = pd.read_html(StringIO(str(bs(page4,features="lxml").find_all('table',{'id':'data'}))))[0]
    tables = [[table1,'100M'],[table2,'100K'],[table3,'100M'],[table4,'100K']]
    for table,dist in tables:
        finishers = table.loc[table['Status']=='Complete']

        for index,table in list(finishers.iterrows()):
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
def updateT400(table,dist):
    #TODO: add partial distances
    finishers = table.loc[table['Status']=='Complete']

    for index,table in list(finishers.iterrows()):
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
def updateGarmin(table,dist):
    finishers = table.loc[table['Status']=='Complete']

    for index,table in list(finishers.iterrows()):
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
    if t4: updateT400(table,dist)
    if  g: updateGarmin(table,dist)
def getResultsRocky(event,dist):
    if not (t4 or g): return
    url = "http://edsresults.com/{}rr{}/index.php?search_type=race_results&event={}&gender=&results_per_page=1000".format(cur_year,event,dist)
    page = requests.get(url).content
    table = pd.read_html(StringIO(str(bs(page,features="lxml").find_all('table',{'id':'data'}))))[0]
    if t4: updateT400(table,dist)
    if  g: updateGarmin(table,dist)

if t3: updateT300()

#Get Bandera results
if days > 20:
    getResults("bandera","100K")
    getResults("bandera","50K")
    getResults("bandera","Saturday+50K")
    if g: getResults("bandera","25K")

#Get Rocky Raccoon results
if days > 50:
    getResultsRocky(100,'100M')
    getResultsRocky(100,'100K')
    getResultsRocky(50,'50M')
    getResultsRocky(50,'50K')
    if g: getResultsRocky(50,'13.1M')

#Get Great Springs Austin results
if days > 75: 
    getResults("austin",'50K')
    if g:
        getResults("austin",'26.2M')
        getResults("austin",'13.1M')
        getResults("austin",'10K')
        getResults("austin",'5K')

#Get Hippo results
if days > 90 and g:
    getResults("hippo","26.2M")
    getResults("hippo","13.1M")
    getResults("hippo","10K")
    getResults("hippo","5K")

#Get Hells Hills results
if days > 100:
    getResults("hh",'50M')
    getResults("hh",'50K')
    if g:
        getResults("hh",'25K')
        getResults("hh",'10K')

#Get Pandora results
if days > 120: 
    getResults("rox",'52.4M')
    if g:
        getResults("rox",'26.2M')
        getResults("rox",'13.1M')
        getResults("rox",'8M')
        getResults("rox",'4M')

#Get Dirt Fest results
if days > 135: 
    getResults("dirtfest",'50K')
    if g:
        getResults("dirtfest",'25K')
        getResults("dirtfest",'5M')

#Get River's Edge results
if days > 150: 
    getResults("edge",'50K')
    if g:
        getResults("edge",'25K')
        getResults("edge",'10M')
        getResults("edge",'5M')

#Get Great Springs Canyon Lake results
if days > 160: 
    getResults("canyonlake",'50K')
    if g:
        getResults("canyonlake",'25K')
        getResults("canyonlake",'10K')
        getResults("canyonlake",'5K')

#Get Mellow results
if days > 260 and g:
    getResults("mellow",'5K')
    getResults("mellow",'10K')
    getResults("mellow",'13.1M')
    getResults("mellow",'26.2M')

#Get Trailway results
if days > 290: 
    getResults("trailway",'50K')
    if g:
        getResults("trailway",'5K')
        getResults("trailway",'10K')
        getResults("trailway",'13.1M')
        getResults("trailway",'26.2M')

#Get Cactus Rose results
if days > 305:
    getResults("cr",'100M')
    getResults("cr",'50M')
    if g:
        getResults("cr",'25M')
        getResults("cr",'5M')

#Get Wild Hare results
if days > 325:
    getResults("wildhare",'50M')
    getResults("wildhare",'50K')
    if g:
        getResults("wildhare",'25K')
        getResults("wildhare",'10K')

#Get Mosaic results
if days > 345: 
    getResults("mosaic",'50K')
    if g:
        getResults("mosaic",'5K')
        getResults("mosaic",'10K')
        getResults("mosaic",'15K')
        getResults("mosaic",'13.1M')
        getResults("mosaic",'26.2M')
