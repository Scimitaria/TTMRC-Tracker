import json
import requests # type: ignore
from io import StringIO
from datetime import date
import pandas as pd # type: ignore
from bs4 import BeautifulSoup as bs # type: ignore

# prevents pandas from cutting data
pd.set_option('display.max_rows',None)

#Create empty JSON data
with open('T400.json', 'w') as file: json.dump({},file,indent=4) 

cur_year = date.today().year
days = date.today().timetuple().tm_yday

def getResults(event,year,dist):
    url = "http://edsresults.com/{}{}/index.php?search_type=race_results&event={}&gender=&results_per_page=1000/".format(event,str(year)[-2:],dist)
    page = requests.get(url).content
    table = pd.read_html(StringIO(str(bs(page,features="lxml").find_all('table',{'id':'data'}))))[0]
    finishers = table.loc[table['Status']=='Complete']
    for index,table in list(finishers.iterrows()):
        data=str(table).splitlines()[:-1]
        name = (str(data[4].split(" ")[-1])+" "+str(data[5].split(" ")[-1])).lower()
        mileage=0
        if   "100M" in dist: mileage+=100
        elif "100K" in dist: mileage+=62.1
        elif "50M" in dist: mileage+=50
        elif "50K" in dist: mileage+=31.1

        with open('T400.json', 'r+') as file:
            t400=json.load(file)
            #update mileages
            if name in t400: t400[name] += mileage
            else: t400[name] = mileage
            sorted_json=dict(sorted(t400.items(), key=lambda item: item[1], reverse=True))
            file.seek(0)
            file.truncate()
            json.dump(sorted_json, file, indent=4)

def getResultsRocky(year,event,dist):
    url = "http://edsresults.com/{}rr{}/index.php?search_type=race_results&event={}&gender=&results_per_page=1000".format(year,event,dist)
    page = requests.get(url).content
    table = pd.read_html(StringIO(str(bs(page,features="lxml").find_all('table',{'id':'data'}))))[0]
    finishers = table.loc[table['Status']=='Complete']
    for index,table in list(finishers.iterrows()):
        data=str(table).splitlines()[:-1]
        name = (str(data[4].split(" ")[-1])+" "+str(data[5].split(" ")[-1])).lower()
        mileage=0
        if   "100M" in dist: mileage+=100
        elif "100K" in dist: mileage+=62.1
        elif "50M" in dist: mileage+=50
        elif "50K" in dist: mileage+=31.1

        with open('T400.json', 'r+') as file:
            t400=json.load(file)
            #update mileages
            if name in t400: t400[name] += mileage
            else: t400[name] = mileage
            sorted_json=dict(sorted(t400.items(), key=lambda item: item[1], reverse=True))
            file.seek(0)
            file.truncate()
            json.dump(sorted_json, file, indent=4)

#Get Bandera results
#b_y = str(cur_year if days > 20 else cur_year-1)[-2:]
if days > 20:
    getResults("bandera",cur_year,"100K")
    getResults("bandera",cur_year,"50K")
    getResults("bandera",cur_year,"Saturday+50K")

#Get Rocky Raccoon results
#rr_y = cur_year if days > 50 else cur_year-1
if days > 50:
    getResultsRocky(cur_year,100,'100M')
    getResultsRocky(cur_year,100,'100K')
    getResultsRocky(cur_year,50,'50M')
    getResultsRocky(cur_year,50,'50K')

#Get Great Springs Austin results
#gsa_y = str(cur_year if days > 75 else cur_year-1)[-2:]
if days > 75: getResults("austin",cur_year,'50K')

#Get Hells Hills results
#hh_y = str(cur_year if days > 100 else cur_year-1)[-2:]
if days > 100:
    getResults("hh",cur_year,'50M')
    getResults("hh",cur_year,'50K')

#Get Pandora results
#pb_y = str(cur_year if days > 120 else cur_year-1)[-2:]
if days > 120: getResults("rox",cur_year,'52.4M')

#Get Dirt Fest results
#df_y = str(cur_year if days > 135 else cur_year-1)[-2:]
if days > 135: getResults("dirtfest",cur_year,'50K')

#Get River's Edge results
#re_y = str(cur_year if days > 150 else cur_year-1)[-2:]
if days > 150: getResults("edge",cur_year,'50K')

#Get Great Springs Canyon Lake results
#gscl_y = str(cur_year if days > 160 else cur_year-1)[-2:]
if days > 160: getResults("canyonlake",cur_year,'50K')

#Get Trailway results
#tt_y = str(cur_year if days > 290 else cur_year-1)[-2:]
if days > 290: getResults("trailway",cur_year,'50K')


#Get Cactus Rose results
#cr_y = str(cur_year if days > 305 else cur_year-1)[-2:]
if days > 305:
    getResults("cr",cur_year,'100M')
    getResults("cr",cur_year,'50M')

#Get Wild Hare results
#wh_y = str(cur_year if days > 325 else cur_year-1)[-2:]
if days > 325:
    getResults("wildhare",cur_year,'50M')
    getResults("wildhare",cur_year,'50K')

#Get Mosaic results
#m_y = str(cur_year if days > 345 else cur_year-1)[-2:]
if days > 345: getResults("mosaic",cur_year,'50K')
