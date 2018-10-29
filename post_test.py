import requests
import urllib

url = "http://www.bamosz.hu/web/guest/alapoldal"

querystring = {"_bamoszpublicalapoldal_WAR_bamoszpublicalapoldalportlet_INSTANCE_N4Uk__facesViewId":"/view.xhtml","p_p_col_count":"1","p_p_col_id":"column-1","p_p_id":"bamoszpublicalapoldal_WAR_bamoszpublicalapoldalportlet_INSTANCE_N4Uk","p_p_lifecycle":"2","p_p_mode":"view","p_p_state":"normal"}

payload = 'A3225%3Aj_idt7=A3225%3Aj_idt7&javax.faces.encodedURL=http%#3A%2F%2Fwww.bamosz.hu%2Fweb%2Fguest%2Falapoldal%3F_bamoszpublicalapoldal_WAR_bamoszpublicalapoldalportlet_INSTANCE_N4Uk__facesViewId%3D%252Fview.xhtml%26p_p_col_count%3D1%26p_p_col_id%3Dcolumn-1%26p_p_id%3Dbamoszpublicalapoldal_WAR_bamoszpublicalapoldalportlet_INSTANCE_N4Uk%26p_p_lifecycle%3D2%26p_p_mode%3Dview%26p_p_state%3Dnormal&A3225%3Aj_idt7%3Aj_idt8=&A3225%3Aj_idt7%3AstartDate_input=2017.03.10&A3225%3Aj_idt7%3AendDate_input=2018.03.10&A3225%3Aj_idt7%3AchartDataCaption=%C3%81rfolyam&A3225%3Aj_idt7%3chartType=arfolyam&A3225%3Aj_idt7%3Aj_idt267_input=vesszo&javax.faces.ViewState=-220517059891699428%3A-5300933957931377133&javax.faces.partial.ajax=true&javax.faces.source=A3225:j_idt7:j_idt232&javax.faces.partial.execute=@all&javax.faces.partial.render=A3225:j_idt7:grafikon A3225:j_idt7:fundDataTable A3225:j_idt7:startDate&A3225:j_idt7:j_idt232=A3225:j_idt7:j_idt232&interval=10Y'

headers = {
    'origin': "http://www.bamosz.hu",
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded",
    'accept': "application/xml, text/xml, */*; q=0.01",
    'faces-request': "partial/ajax",
    'x-devtools-emulate-network-conditions-client-id': "(7DA15FA3F5708CF2C49731792D975E3B)",
    'x-requested-with': "XMLHttpRequest",
    'referer': "http://www.bamosz.hu/alapoldal?isin=HU0000711015",
    'accept-encoding': "gzip, deflate",
    'accept-language': "en-US,en;q=0.9,hu;q=0.8",
    'cookie': "COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=hu_HU; __utmc=253912987; __utmz=253912987.1520621149.9.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); JSESSIONID=B0135F4B356F65D300B0FC3D50B97E83; __utma=253912987.58143300.1512671141.1520635846.1520702315.13; __utmb=253912987.2.9.1520702315; csfcfc=121245Xfn_; COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=hu_HU; __utmc=253912987; __utmz=253912987.1520621149.9.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); JSESSIONID=B0135F4B356F65D300B0FC3D50B97E83; __utma=253912987.58143300.1512671141.1520635846.1520702315.13; __utmb=253912987.2.9.1520702315",
    'cache-control': "no-cache",
    'postman-token': "6a1c8c5c-54cf-73a8-7527-d3c10464dedf"
    }

response = requests.request("POST", url, data=urllib.urlencode(payload), headers=headers, params=querystring)

print(size(response.text))
