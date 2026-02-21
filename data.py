import requests # type: ignore
from io import StringIO
from datetime import date
import pandas as pd # type: ignore
from bs4 import BeautifulSoup as bs # type: ignore

# prevents pandas from cutting data
pd.set_option('display.max_rows',None)

cur_year = date.today().year
days = date.today().timetuple().tm_yday

def getResults(event,year,dist):
    url = "http://edsresults.com/{}{}/index.php?search_type=race_results&event={}&gender=&results_per_page=1000/".format(event,year,dist)
    page = requests.get(url).content
    table = pd.read_html(StringIO(str(bs(page,features="lxml").find_all('table',{'id':'data'}))))[0]
    finishers = table.loc[table['Status']=='Complete']
    for index,table in list(finishers.iterrows()):
        data=str(table).splitlines()[:-1]
        name = (str(data[4].split(" ")[-1])+" "+str(data[5].split(" ")[-1])).lower()
        m=0
        if   "100M" in dist: m+=100
        elif "100K" in dist: m+=62.1
        elif "50M" in dist: m+=50
        elif "50K" in dist: m+=31.1

def getResultsRocky(year,event,dist):
    url = "http://edsresults.com/{}rr{}/index.php?search_type=race_results&event={}&gender=&results_per_page=1000".format(year,event,dist)
    page = requests.get(url).content
    table = pd.read_html(StringIO(str(bs(page,features="lxml").find_all('table',{'id':'data'}))))[0]
    finishers = table.loc[table['Status']=='Complete']
    for index,table in list(finishers.iterrows()):
        data=str(table).splitlines()[:-1]
        print(str(data[4].split(" ")[-1]),str(data[5].split(" ")[-1]))

#Get Bandera results
b_y = str(cur_year if days > 20 else cur_year-1)[-2:]
#getResults("bandera",b_y,"100K")
#getResults("bandera",b_y,"50K")
#getResults("bandera",b_y,"Saturday+50K")

#Get Rocky Raccoon results
rr_y = cur_year if days > 50 else cur_year-1
#getResultsRocky(rr_y,100,'100M')
#getResultsRocky(rr_y,100,'100K')
#getResultsRocky(rr_y,50,'50M')
#getResultsRocky(rr_y,50,'50K')

#Get Great Springs Austin results
gsa_y = str(cur_year if days > 75 else cur_year-1)[-2:]
#getResults("austin",gsa_y,'50K')

#Get Hells Hills results
hh_y = str(cur_year if days > 100 else cur_year-1)[-2:]
#getResults("hh",hh_y,'50M')
#getResults("hh",hh_y,'50K')

#Get Pandora results
pb_y = str(cur_year if days > 120 else cur_year-1)[-2:]
#getResults("rox",pb_y,'52.4M')

#Get Dirt Fest results
df_y = str(cur_year if days > 135 else cur_year-1)[-2:]
#getResults("dirtfest",df_y,'50K')

#Get River's Edge results
re_y = str(cur_year if days > 150 else cur_year-1)[-2:]
#getResults("edge",re_y,'50K')

#Get Great Springs Canyon Lake results
gscl_y = str(cur_year if days > 160 else cur_year-1)[-2:]
#getResults("canyonlake",gscl_y,'50K')

#Get Trailway results
tt_y = str(cur_year if days > 290 else cur_year-1)[-2:]
#getResults("trailway",tt_y,'50K')


#Get Cactus Rose results
cr_y = str(cur_year if days > 305 else cur_year-1)[-2:]
#getResults("cr",cr_y,'100M')
#getResults("cr",cr_y,'50M')

#Get Wild Hare results
wh_y = str(cur_year if days > 325 else cur_year-1)[-2:]
#getResults("wildhare",wh_y,'50M')
#getResults("wildhare",wh_y,'50K')

#Get Mosaic results
m_y = str(cur_year if days > 345 else cur_year-1)[-2:]
#getResults("mosaic",m_y,'50K')


# Deprecated due to being short #
#Get Hippo results
#h_y = str(cur_year if days > 90 else cur_year-1)[-2:]
#Get Mellow results
#m_y = str(cur_year if days > 260 else cur_year-1)[-2:]
#mellowMar = requests.get("http://edsresults.com/mellow{}/index.php?search_type=race_results&event=26.2M&gender=&results_per_page=400".format(m_y))
