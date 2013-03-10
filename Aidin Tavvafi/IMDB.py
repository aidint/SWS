"""
Coded By: Aidin Tavvafi
Project:  Simple Web Scraping(SWS)

IMDB_fc returns a dictionary containing full credits of a movie, defined by it's name, and saves the scraped data into a database(.mdb) 

simple sample:
z = IMDB_fc(raw_input("name of the movie: "))
for i in z:#stepping in the result dictionary
    print;print
    print i
    print
    for j in z[i]:#stepping in the categories
        p = BeautifulSoup(j[0])
        p = p.prettify().strip()
        s = p 
        p = BeautifulSoup(j[1])
        p = p.prettify().strip()
        s += "      "+ u" role:" 
        s += p
        print s
"""
from bs4 import *
from urllib2 import *
from tagrem import *  
import codecs  
import WSdb
#def output(string,filename,mode):
#    k = codecs.open(filename,mode,"UTF-8")
#    k.write(string)
#    k.close()
def IMDB_fc(name,valid=1):
    isdet = False
    result = dict()
    name2 = name #name2 is a backup for name of the movie
    name = name.replace(" ","+") #for searching we need to remove spaces and put
    #"+" instead
    f = urlopen("http://www.imdb.com/find?q="+name+"&s=tt")
    name = name2
    s = f.read()
    #finding the movie url:
    s = s[s.find('<td class="result_text">')+len('<td class="result_text">'):]
    s = s[s.find("href") + 6:s.find('" >')]
    s = s.split("/")
    s = s[2]
    if s[:2] != "tt":
        print "Movie Not Found"
        return None
    f = urlopen("http://www.imdb.com/title/"+s+"/fullcredits")
    s2 = s
    s = f.read()
    #seeing if the movie found is the movie that the user is searching for:
    t = s[s.find('<a class="main"')+1:]
    t = t[t.find(">")+1:t.find("<")]
    if valid:
        if t != name.title():
            if (raw_input(t + "\t"+"is this the movie you are searching for?(no if not)\t")
                == "no"):
                print "Movie not found"
                return None
    soup = BeautifulSoup(s)
    j = soup.prettify()
    a = list()
    categorylist = list()
    for i in soup.findAll("a"):
        try:
            x = i["class"]
        except:
            continue
        if x[0] == 'glossary':
            k = BeautifulSoup(i.__str__())
            k = k.prettify()
            u = tagrem(k,2)
            categorylist.append(u)
            k = k[:k.find(">")]
            a.append(k)
    result = dict()
    for po in categorylist:
        result[po] = [[["Name","varchar(255)"],["Role","varchar(255)"]]]
    for i in range(len(a)):
        
        categoryinside = list()
        try:
            t = j[j.find(a[i])+len(a[i]):]
            t = t[:t.find(a[i+1])]
        except:
            t = j[j.find(a[i])+len(a[i]):]
            t = t[:t.find("</table>")]  
        p = BeautifulSoup(t)
        
        for k in p.findAll("tr"):
            
            z = tagrem(k.__str__(),2)
            while z.find("  ") != -1:
                z = z.replace("  ","")
                z = z.replace("\n","")
            if len(z) != 0:
                credit = list()
                if z.find("...") != -1:
                    this = z.split("...")
                    delchar = "."
                else:
                    this = z.split("(")
                    delchar = ")"
                if len(this) == 1:
                    credit.append("'"+this[0].strip()+"'")
                    credit.append("''")
                elif len(this) == 2:
                    credit.append("'"+this[0].strip()+"'"); credit.append("'"+this[1].strip(delchar).strip()+"'")
                categoryinside.append(credit)
                
        result[categorylist[i]].append(categoryinside)
    WSdb.tomdb(result,name+".mdb")
    return result



        

    
