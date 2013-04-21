import urllib2
from bs4 import*
import re
from tagrem import *
import WSdb
import random

collist = []
jlist = []
last = dict()

f = urllib2.urlopen("http://www.irexpert.ir/Webforms/Default/Search.aspx?OnlineOnly=1")

print "Connected"

s = f.read()

pattern=r"\?\d{6}"

nums=re.findall(pattern,s)

num=[]

for item in nums:
    num.append(item[1:])
    
info=[]

for i in range(len(num)):
    info.append({})
    
result = dict()

for person in range(len(num)):
    f = urllib2.urlopen("http://www.irexpert.ir/Webforms/UserHome/Expert.aspx?EID="+num[person])
    print person
    s = f.read()
    t = BeautifulSoup(s)
    y = t.prettify()
    a = list()
    
    for i in t.findAll("td"):
        try:
            x = i["class"]
        except:
            continue
        if x[0] == 'InfoTitle':
            k = BeautifulSoup(i.__str__())
            k = k.prettify()
            k = k[:k.find(">")+1]
            a.append(k)
            
    if person == 0:
        for j in range(12):
            flist = []
            searchquery = a[j]
            u = y[y.find(searchquery)+len(searchquery):]
            u = u[:u.find("</tr>")]
            y = y[y.find(u)+len(u):]
            u = tagrem(u,2)
            u = BeautifulSoup(u).prettify().strip()
            flist.append(u.split(":",1)[0].strip())
            flist.append("varchar(255)")
            collist.append(flist)
        flist = []
        searchquery = a[j+1]
        u = y[y.find(searchquery)+len(searchquery):]
        u = u[:u.find("</tr>")]
        y = y[y.find(u)+len(u):]
        u = tagrem(u,2)
        u = BeautifulSoup(u).prettify().strip()
        flist.append(u.split(":",1)[0].strip())
        flist.append("varchar(255)")
        collist.append(flist)
    last["Online"] = [collist]
    y = t.prettify()
    
        
    y = t.prettify()
    flist = []
    for j in range(12):
        searchquery = a[j]
        u = y[y.find(searchquery)+len(searchquery):]
        u = u[:u.find("</tr>")]
        y = y[y.find(u)+len(u):]
        u = tagrem(u,2)
        u = BeautifulSoup(u).prettify().strip()
        u = BeautifulSoup("'" + u.split(":",1)[1].strip() + "'").prettify().strip()
        flist.append(u)
        
    searchquery = a[j+1]
    u = y[y.find(searchquery)+len(searchquery):]
    u = u[:u.find("</textarea>")]
    s = y[y.find(u)+len(u):]
    u = tagrem(u,2)
    u = BeautifulSoup(u).prettify().strip()
    u = BeautifulSoup("'" + u.split(":",1)[1].strip() + "'").prettify().strip()
    flist.append(u)
    jlist.append(flist)
last["Online"].append(jlist)

z = str(random.randint(1,1000))

        
print z
WSdb.tomdb(last,z+".mdb")
