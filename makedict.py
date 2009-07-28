import re, urllib, string
from BeautifulSoup import BeautifulSoup

q = "hhh/"

def scrape(url):
    f = urllib.urlopen(url)
    html = f.read()
    return BeautifulSoup(html)

def getStates(url):
    soup = scrape(url)
    result = {}
    match = re.findall('<a href="(http://geo.craigslist.org/iso/us/\w+)">([\w ]+)</a>', str(soup))
    for f in match:
        state = string.capwords(f[1])
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
    
    
        


