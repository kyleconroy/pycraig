import re, urllib, string
from BeautifulSoup import BeautifulSoup



def scrape(url):
    f = urllib.urlopen(url)
    html = f.read()
    return BeautifulSoup(html)

def getSections():
    url = "http://sfbay.craigslist.org/"
    categories = {"Community" : {"url": "ccc"},
                  "Housing" : {"url": "hhh"},
                  "Jobs": {"url": "jjj"},
                  "For Sale": {"url": "sss"},
                  "Gigs": {"url": "ggg"},
                  "Services":{"url": "bbb"},
                  "Personals":{"url": "ppp"},
                  "Resumes":{"url": "res"}}
    soup = scrape(url)
    for k,v in categories.items():
        s = str(soup.findAll(id=v['url']))
        match = re.findall('<a href="/cgi-bin/personals.cgi\?category=(\w+)">([\w ]+)</a>', s)
        if not match:
            match = re.findall('<a href="(\w+)/">([\w /]+)<\/a>', s)
        if match:
            result = {}
            for f in match:
                result[string.capwords(f[1])] = f[0]
            v["sections"] = result
    return categories
            
            
            
        

def getStates(url):
    rename = {"dc" : "washington dc",
              "mass" : "massachusetts",
              "n carolina": "north carolina",
              "n hampshire": "new hampshire",
              "s carolina": "south carolina"}
    soup = scrape(url)
    result = {}
    match = re.findall('<a href="(http://geo.craigslist.org/iso/us/\w+)">([\w ]+)</a>', str(soup))
    for f in match:
        state = f[1]
        if state in rename.keys():
            state = rename[state]
        state = string.capwords(state)
        result[state] = getCities(f[0])
    return result


def getCities(url):
    soup = scrape(url)
    s = str(soup.findAll(id="list"))
    result = {}
    match = re.findall('<a href="(http://\w+.craigslist.org/)">([\w ]+)</a>', s)
    for f in match:
        city = string.capwords(f[1])
        url = f[0]
        result[city] = url
    match = re.findall('<a href="(http://\w+.craigslist.org/)"><b>([\w ]+)</b></a>', s)
    for f in match:
        city = string.capwords(f[1])
        url = f[0]
        result[city] = getAreas(url)
    match = re.findall('<a href="(http://\w+.craigslist.org/)">([\w ]+)\W*[/-]+\W*([\w ]+)</a>', s)
    for f in match:
        city1 = string.capwords(f[1])
        city2 = string.capwords(f[1])
        url = f[0]
        result[city1] = url
        result[city2] = url
    if result:
        return result 
    else:
        f = urllib.urlopen(url)
        return f.geturl()

def getAreas(url):
    soup = scrape(url)
    s = soup.findAll("span",{"class":"for"})
    match = re.findall('<a href="/(\w+)/" title="([\w ]+)">', str(s))
    result = {}
    for f in match:
        area = string.capwords(f[1])
        aurl = url + f[0] + "/"
        result[area] = getNeighborhoods(aurl)
    if result:
        result["all"] = url
        return result
    else:
        return url

def getNeighborhoods(url):
    q = "hhh/"
    if url == "http://newyork.craigslist.org/mnh/":
        return url
    if not re.match("sfbay", url):
        return url
    nurl = url + q
    soup = scrape(nurl)
    s = soup.findAll("select", {"name":"neighborhood"})
    result = {}
    match = re.findall('<option value="(\d+)">([\w /-]+)', str(s))
    for f in match:
        value = f[0]
        n = f[1].split(' / ')
        for place in n:
            result[string.capwords(place)] = value 
    result["all"] = url
    return result
    
        


