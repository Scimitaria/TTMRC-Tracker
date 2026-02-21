import requests # type: ignore
from datetime import date
from bs4 import BeautifulSoup as bs # type: ignore

cur_year = date.today().year
days = date.today().timetuple().tm_yday

#Get Bandera results
b_y = str(cur_year if days > 20 else cur_year-1)[-2:]
#bandera100 = requests.get("http://edsresults.com/bandera{}/index.php?search_type=race_results&event=100K&gender=&results_per_page=400/".format(b_y)
#bandera50  = requests.get("http://edsresults.com/bandera{}/index.php?search_type=race_results&event=50K&gender=&results_per_page=400/".format(b_y)
#bandera50S = requests.get("http://edsresults.com/bandera{}/index.php?search_type=race_results&event=Saturday+50K&gender=&results_per_page=400/".format(b_y)

#Get Rocky Raccoon results
rr_y = cur_year if days > 50 else cur_year-1
#rocky100M = requests.get("http://edsresults.com/{}rr100/index.php?search_type=race_results&event=100M&gender=&results_per_page=400".format(rr_y))
#rocky100K = requests.get("http://edsresults.com/{}rr100/index.php?search_type=race_results&event=100K&gender=&results_per_page=400".format(rr_y))
#rocky50M  = requests.get("http://edsresults.com/{}rr50/index.php?search_type=race_results&event=50M&gender=&results_per_page=400".format(rr_y))
#rocky50K  = requests.get("http://edsresults.com/{}rr50/index.php?search_type=race_results&event=50K&gender=&results_per_page=400".format(rr_y))

#Get Great Springs Austin results
gsa_y = str(cur_year if days > 75 else cur_year-1)[-2:]
#gsa50k = requests.get("http://edsresults.com/austin{}/index.php?search_type=race_results&event=50K&gender=&results_per_page=400".format(gs_y))
#gsaMar = requests.get("http://edsresults.com/austin{}/index.php?search_type=race_results&event=26.2M&gender=&results_per_page=400".format(gs_y))

#Get Hippo results
h_y = cur_year if days > 90 else cur_year-1
#hippoMar = requests.get("http://edsresults.com/hippo{}/index.php?search_type=race_results&event=26.2M&gender=&results_per_page=400".format(str(h_y)[-2:]))

#Get Hells Hills results
hh_y = str(cur_year if days > 100 else cur_year-1)[-2:]
#hh50M = requests.get("http://edsresults.com/hh{}/index.php?search_type=race_results&event=50M&gender=&results_per_page=400".format(hh_y))
#hh50K = requests.get("http://edsresults.com/hh{}/index.php?search_type=race_results&event=50K&gender=&results_per_page=400".format(hh_y))

#Get Pandora results
pb_y = str(cur_year if days > 120 else cur_year-1)[-2:]
#pb_DMar = requests.get("http://edsresults.com/rox{}/index.php?search_type=race_results&event=52.4M&gender=&results_per_page=400".format(hh_y))
#pb_Mar  = requests.get("http://edsresults.com/rox{}/index.php?search_type=race_results&event=26.2M&gender=&results_per_page=400".format(hh_y))

#Get Dirt Fest results
df_y = str(cur_year if days > 135 else cur_year-1)[-2:]
#df_50K = requests.get("http://www.edsresults.com/dirtfest{}/index.php?search_type=race_results&event=50K&gender=&results_per_page=400".format(df_y))

#Get River's Edge results
re_y = str(cur_year if days > 150 else cur_year-1)[-2:]
#re50K = requests.get("http://edsresults.com/edge{}/index.php?search_type=race_results&event=50K&gender=&results_per_page=400".format(re_y))

#Get Great Springs Canyon Lake results
gscl_y = str(cur_year if days > 160 else cur_year-1)[-2:]
#gscl50K = requests.get("http://edsresults.com/canyonlake{}/index.php?search_type=race_results&event=50K&gender=&results_per_page=400".format(gscl_y))

#Get Mellow results
m_y = str(cur_year if days > 260 else cur_year-1)[-2:]
#mellowMar = requests.get("http://edsresults.com/mellow{}/index.php?search_type=race_results&event=26.2M&gender=&results_per_page=400".format(m_y))

#Get Trailway results
tt_y = str(cur_year if days > 290 else cur_year-1)[-2:]
#tt50K = requests.get("http://edsresults.com/trailway{}/index.php?search_type=race_results&event=50K&gender=&results_per_page=400".format(tt_y))
#ttMar = requests.get("http://edsresults.com/trailway{}/index.php?search_type=race_results&event=26.2M&gender=&results_per_page=400".format(tt_y))

#Get Cactus Rose results
cr_y = str(cur_year if days > 305 else cur_year-1)[-2:]
#cr100M = requests.get("http://edsresults.com/cr{}/index.php?search_type=race_results&event=100M&gender=&results_per_page=400".format(cr_y))
#cr50M  = requests.get("http://edsresults.com/cr{}/index.php?search_type=race_results&event=50M&gender=&results_per_page=400".format(cr_y))

#Get Wild Hare results
wh_y = str(cur_year if days > 325 else cur_year-1)[-2:]
#wh50M = requests.get("http://edsresults.com/wildhare{}/index.php?search_type=race_results&event=50M&gender=&results_per_page=400".format(cr_y))
#wh50K = requests.get("http://edsresults.com/wildhare{}/index.php?search_type=race_results&event=50K&gender=&results_per_page=400".format(cr_y))

#Get Mosaic results
m_y = str(cur_year if days > 345 else cur_year-1)[-2:]
#mosaic50K = requests.get("http://edsresults.com/mosaic{}/index.php?search_type=race_results&event=50K&gender=&results_per_page=400".format(m_y))
#mosaicMar = requests.get("http://edsresults.com/mosaic{}/index.php?search_type=race_results&event=26.2M&gender=&results_per_page=400".format(m_y))
