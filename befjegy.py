from bs4 import BeautifulSoup
import urllib2
import requests
import numpy as np
import datetime 
import time
import csv
import pickle
import os.path
import requests
import matplotlib.dates as mdates
import logging
import math
import numpy as np
import codecs
import pandas as pd
import sys
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnicodeDictReader( object ):
    def __init__( self, *args, **kw ):
        self.encoding= kw.pop('encoding', 'utf8')
        self.reader= csv.DictReader( *args, **kw )
    def __iter__( self ):
        decode= codecs.getdecoder( self.encoding )
        for row in self.reader:
            t= dict( (k,decode(row[k])[0]) for k in row )
            yield t

class befjegy:
    daily_rates={}
    base_url="http://www.bamosz.hu/alapoldal?isin="
    isin=[] 
    base_url2="http://www.bamosz.hu/legfrissebb-adatok"

    def __init__(self,list):  
        self.isin=list
        self.load_rates()

    @classmethod
    def from_file(cls,filename):
        befjegy=cls(cls.load_isin(filename))
        return befjegy

    @staticmethod
    def refresh_isin(isinlist=[]):
        isin=[]
        r=urllib2.urlopen(befjegy.base_url2).read()
        soup=BeautifulSoup(r,"html.parser")
        tables=soup.find_all("table",class_="dataTable2 alapokContainer specEvenOddTableGrey")
        for table in tables:
            rows=table.find_all("tr")
            for row in rows:
                if row.has_attr("class") and row["class"]==["dataContainer", "dataContainerTop"]:
                    category=row.find("td").get_text().strip()
                elif row.has_attr("class") and set(["dataContainer", "dataContainerTop", "nyitoEvenT"]).issubset(row["class"]):
                    data={}
                    data["name"]=row.find("a").get_text().strip()
                    data["category"]=category
                    data["isin"]= row.find("a")["onclick"][14:-4].split(",")[-1].split("'")[-2]
                elif row.has_attr("class") and set(["dataContainer", "borderRightDotted", "nyitoEvenT2"]).issubset(row["class"]):
                    cells=row.find_all("td")
                    data["currency"]=cells[1].get_text().strip()
                    data["startdate"]=cells[12].get_text().strip()
                    data["risk"]=cells[13].get_text().strip()
                    isin.append(data)

        keys=isin[0].keys()
        with open("isin.conf","wb" ) as fp:
            dict_writer = csv.DictWriter(fp, keys)
            dict_writer.writeheader()
            for i in isin:
                dict_writer.writerow({k:v.encode('utf8') for k,v in i.items()})
        fp.close()

    @staticmethod
    def load_isin(conf):
        isin=[]
        try:
            with codecs.open(conf,"rb") as fp:
                rdr= UnicodeDictReader( fp )
                for row in rdr:
                    isin.append(row)
            return isin
        except IOError:
            print("Cannot load config file:" + conf  +  " Check if file exists!")


    def download_data(self,isin):
        url=self.base_url+isin
        session = requests.session()
        r=session.get(url)
        soup=BeautifulSoup(r.content,"html.parser")
        vs=soup.select("input#javax.faces.ViewState")[0]["value"]
        cookie=""
        for k, v in requests.utils.dict_from_cookiejar(r.cookies).iteritems():
            cookie= cookie+ k +"="+ v+";"        
        
        url = "http://www.bamosz.hu/web/guest/alapoldal"
        querystring = {"_bamoszpublicalapoldal_WAR_bamoszpublicalapoldalportlet_INSTANCE_N4Uk__facesViewId":"/view.xhtml","p_p_col_count":"1","p_p_col_id":"column-1","p_p_id":"bamoszpublicalapoldal_WAR_bamoszpublicalapoldalportlet_INSTANCE_N4Uk","p_p_lifecycle":"2","p_p_mode":"view","p_p_state":"normal"}
        payload = (
            ('A3225%3Aj_idt7','A3225%3Aj_idt7'),
            ('javax.faces.encodedURL','http%3A%2F%2Fwww.bamosz.hu%2Fweb%2Fguest%2Falapoldal%3F_bamoszpublicalapoldal_WAR_bamoszpublicalapoldalportlet_INSTANCE_N4Uk__facesViewId%3D%252Fview.xhtml%26p_p_col_count%3D1%26p_p_col_id%3Dcolumn-1%26p_p_id%3Dbamoszpublicalapoldal_WAR_bamoszpublicalapoldalportlet_INSTANCE_N4Uk%26p_p_lifecycle%3D2%26p_p_mode%3Dview%26p_p_state%3Dnormal'),
            ('A3225%3Aj_idt7%3Aj_idt8',''),
            ('A3225%3Aj_idt7%3AstartDate_input','2017.03.12'),
            ('A3225%3Aj_idt7%3AendDate_input','2018.03.12'),
            ('A3225%3Aj_idt7%3AchartDataCaption','%C3%81rfolyam'),
            ('A3225%3Aj_idt7%3AchartType','arfolyam'),
            ('A3225%3Aj_idt7%3Aj_idt267_input','vesszo'),
            ('javax.faces.ViewState',vs),
            ('javax.faces.partial.ajax','true'),
            ('javax.faces.source','A3225:j_idt7:j_idt238'),
            ('javax.faces.partial.execute','@all'),
            ('javax.faces.partial.render','A3225:j_idt7:grafikon A3225:j_idt7:fundDataTable A3225:j_idt7:startDate'),
            ('A3225:j_idt7:j_idt238','A3225:j_idt7:j_idt238'),
            ('interval','10Y'),
        )
        p=''
        for t in payload:
            p=p+t[0]+"="+t[1]+"&"

        headers = {
            'origin': "http://www.bamosz.hu",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'accept': "application/xml, text/xml, */*; q=0.01",
            'faces-request': "partial/ajax",
            'x-devtools-emulate-network-conditions-client-id': "(7DA15FA3F5708CF2C49731792D975E3B)",
            'x-requested-with': "XMLHttpRequest",
            'referer': self.base_url+isin,
            'accept-encoding': "gzip, deflate",
            'accept-language': "en-US,en;q=0.9,hu;q=0.8",
            'cookie': cookie,
            'cache-control': "no-cache"
            }

        r = session.request("POST", url, data=p, headers=headers, params=querystring)
        start_index=r.text.find('<div id="A3225:j_idt7:fundDataTable"')
        end_index=r.text.find("'A3225:j_idt7:fundDataTable', {visible:true});</script>")

#        pattern=re.compile('<!\[CDATA\[(.*?)\]\]>')
#        for m in re.findall(pattern,r.text):
#            if 'dataTable2' in m:
#        soup=BeautifulSoup(r.text[start_index:end_index],'lxml')
#        rows=soup.find_all("table",class_="dataTable2")[1].find_all("tr")
        line_pattern = re.compile('<tr>(.*?)</tr>',re.S)
        cell_pattern= re.compile('<td>(.*?)</td>',re.S)
        rows=re.findall(line_pattern,r.text[start_index:end_index])
        lst=[]
        try:
            for row in rows:
                try:
                    data={}
                    cells=re.findall(cell_pattern,row)
                    data["date"]= time.mktime(datetime.datetime.strptime(cells[0].strip(), "%Y.%m.%d.").timetuple())
                    data["rate"]=float(cells[1].replace(',','.').replace(u'\xa0','').strip()) if cells[1].replace(',','.').replace(u'\xa0','').strip() else 0
                    data["netassetvalue"]=float(cells[2].replace(u'\xa0', u' ').replace(" ","").strip()) if cells[2].replace(u'\xa0', u' ').replace(" ","").strip() else 0
                    data["paidyield"]=float(cells[3].replace(" ","").strip()) if cells[3].replace(" ","").strip() else 0
                    data["trade"]=float(cells[4].strip()) if cells[4].replace(" ","").strip() else 0
                    data["tradepercent"]=float(cells[5].replace(",",".").replace("%","").strip())/100 if cells[5].strip() else 0
                    data["3myield"]=float(cells[6].replace(",",".").replace("%","").strip())/100 if cells[6].strip() else '' 
                    data["6myield"]=float(cells[7].replace(",",".").replace("%","").strip())/100 if cells[7].strip() else ''
                    data["1yyield"]=float(cells[8].replace(",",".").replace("%","").strip())/100 if cells[8].strip() else ''
                    data["3yyield"]=float(cells[9].replace(",",".").replace("%","").strip())/100 if cells[9].strip() else ''
                    data["5yyield"]=float(cells[10].replace(",",".").replace("%","").strip())/100 if cells[10].strip() else ''
                    data["10yyield"]=float(cells[11].replace(",",".").replace("%","").strip())/100 if cells[11].strip() else ''
                    lst.append(data)
                except Exception as inst:
                    logger.error("isin:%s date:%s",isin, cells[0].strip())
                    logger.error(inst)
                    continue

        except Exception as inst:
            logger.error("isin:%s date:%s",isin, cells[0].strip())
            logger.error(inst)

        with open(isin + '.dat', 'wb') as f:
            pickle.dump(lst, f, pickle.HIGHEST_PROTOCOL)
            f.close()

    def load_rates(self):
        for idx,isin in enumerate(self.isin):
            try:
                if not os.path.isfile(isin["isin"]+".dat"):
                    self.download_data(isin["isin"])
                with open(isin["isin"] + '.dat', 'rb') as f:
                    self.daily_rates[isin["isin"]]= pickle.load(f)
                logger.info("%i. %s loaded ok.",idx, isin["isin"])
            except :
                logger.error("%i Loading %s failed.",idx, isin["isin"])
                e = sys.exc_info()[0]
                print "Error: %s" % e 
                continue

    def get_rates(self,normalized=True):
        result=dict()
        for isin in self.isin:
            try:
                if normalized:
                    n=self.daily_rates[isin["isin"]][0]["rate"]
                    rates= [x["rate"]/n for x in self.daily_rates[isin["isin"]]]
                else:
                    rates= [x["rate"] for x in self.daily_rates[isin["isin"]]]
                dates= mdates.epoch2num([x["date"] for x in self.daily_rates[isin["isin"]]])
            except:
                continue
            result[isin["isin"]]=(dates,rates)
        return result
    
    def get_trades(self):
        result=dict()
        for isin in self.isin:
            try:
                trades = [sum([d["trade"] for d in self.daily_rates[isin["isin"]]][i:len(self.daily_rates[isin["isin"]])]) for i in range(len(self.daily_rates[isin["isin"]]))]
                dates= mdates.epoch2num([x["date"] for x in self.daily_rates[isin["isin"]]])
            except:
                continue
            result[isin["isin"]]=(dates,trades)
        return result
    
    def get_asset_value(self):
        result=dict()
        for isin in self.isin:
            result[isin["isin"]]=self.daily_rates[isin["isin"]][0]["netassetvalue"]
        return result

    def get_yields(self,duration):
        result=dict()
        for isin in self.isin:
            try:
                yields=[d[duration] for d in self.daily_rates[isin["isin"]]]
                result[isin["isin"]]=yields
            except:
                logger.error("Creating timeseries for %s failed.",isin["isin"])
                continue

        return result

    def get_yields_stat(self,duration):
        result=dict()

    def get_overview(self,duration):
        result={}
        with open('overview.csv', 'w') as csvfile:
            fieldnames = ['Isin', 'Name','Mean','StdDev']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for isin in self.isin:
                yields=[d[duration] for d in self.daily_rates[isin["isin"]]]
                if len(yields)>0:
                    mn=sum(yields) / len(yields) # Mean value
                    std = math.sqrt(sum([(e-mn)**2 for e in yields]) / len(yields))
                    result[isin["name"] + "(" + isin["isin"] + ")"]=[mn,std]
                    writer.writerow({"Isin":isin["isin"].encode('utf8'),
                                     "Name":isin["name"].encode('utf8'),
                                     "Mean":mn,
                                     "StdDev":std})
        return result

    def get_yields_array(self,duration):
        result={}
        for isin in self.isin:
            yields=[d[duration] for d in self.daily_rates[isin["isin"]]]
            if len(yields)>0:
                result[isin["name"]+"("+isin["isin"]+")"]=np.asarray(yields)
        return result

    def convert_timeseries(self,ts_type):
        data = {}
        for isin in self.isin:
            try:
                d = data.setdefault(isin["isin"], {})
                n=self.daily_rates[isin["isin"]][0][ts_type]
                for x in self.daily_rates[isin["isin"]]:
                    d[x["date"]] = x[ts_type]
            except:
                logger.error("Creating timeseries for %s %s failed.",ts_type,isin["isin"])
                continue
        df = pd.DataFrame.from_dict(data)
        return df

    def get_correlation(self):
        df = self.convert_timeseries("rate")
        df = df.corr()
        df.to_csv("correlation.csv")
        return df

    def get_overview(self):
        df=pd.DataFrame.from_dict(self.isin).set_index("isin")
        df['6m_dev']=self.convert_timeseries("6myield").std()
        df['6m_mean']=self.convert_timeseries("6myield").mean()
        df['1y_dev']=self.convert_timeseries("1yyield").std()
        df['1y_mean']=self.convert_timeseries("1yyield").mean()
        df['3y_dev']=self.convert_timeseries("3yyield").std()
        df['3y_mean']=self.convert_timeseries("3yyield").mean()
        df.to_csv("get_overview.csv",encoding='utf8')
        return df

