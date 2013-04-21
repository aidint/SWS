from urllib2 import*
from tagrem import*
from WSdb import*

s = raw_input("insert the subject : ")
a = urlopen('https://github.com/search?q='+s+'&ref=commandbar')
a = a.read()
z = dict()
y = dict()
z["languages"] = [[["languge name","varchar(20)"],["projects numbers","varchar(10)"]],[]]
tag1 = '<span class="count">'
ta = '</a>'
while a.find(tag1) != -1:                             #through this loop the name and the number of the projects
      projects_num = a[a.find(tag1)+len(tag1):        #written by different languages is taken
                       a[a.find(tag1):].find('</span>') + a.find(tag1)]
      project_name = a[a[a.find(tag1):].find('</span>')+a.find(tag1)+
                        len('</span>')+13:a[a.find(tag1):].find(ta)+a.find(tag1)-1]
      s = "'"+'"' + project_name+'"' + "'"
      t = "'"+'"' + str(projects_num)+'"' + "'"
      w = [s,t]
      z["languages"][1].append(w)
      a = a[a[a.find(tag1):].find('</span>')+a.find(tag1):]
tag2 = '<span class="mega-icon mega-icon-public-repo"></span>'
ht = '">'
ft = '</a>'
itag = 'rel="author">'
ftag = '>]'
f = dict()
i = 0
while a.find(tag2) != -1:                 #through this loop the result of the first page of the search and the name of people who worked on it them taken 
      p = a[a.find(tag2)+len(tag2):]      
      p = p[p.find(ht)+len(ht):p.find(ft)]      #p is the name of the project
      p = tagrem(p)
      a = a[a[a.find(tag2):].find('</span>')+a.find(tag2):]       
      pr = urlopen('https://github.com/' + p)
      pr = pr.read()
      for k in range(2):
            pr = pr[pr.find(itag)+len(itag):]         #pr is the name of each person of the project's member
      l = []
      while pr.find(itag) != -1 :
            n = pr[pr.find(itag)+len(itag):pr.find(ftag)]
            n = tagrem(n,0)
            n = "'"+'"' + n +'"' + "'"
            if n not in l:
                  l.append([n])             #l is a list of the members of the project
            pr = pr[pr.find(itag)+pr.find(ftag)+len(ftag):]
      y[p] = [[["people","varchar(20)"]],l]
      i += 1

q = raw_input("do you want more projects in this subject?(yes,no): ")
page = 2
while q == 'yes':       #through this loop if more projects are needed print yes to get more projects from next pages
      a = urlopen('https://github.com/search?p='+str(page)+'&q='+s+'&ref=commandbar')
      a = a.read()
      while a.find(tag2) != -1:
            p = a[a.find(tag2)+len(tag2):]
            p = p[p.find(ht)+len(ht):p.find(ft)]
            p = tagrem(p)
            a = a[a[a.find(tag2):].find('</span>')+a.find(tag2):]
            pr = urlopen('https://github.com/' + p)
            pr = pr.read()
            for k in range(2):
                  pr = pr[pr.find(itag)+len(itag):]
            l = []
            while pr.find(itag) != -1 :
                  n = pr[pr.find(itag)+len(itag):pr.find(ftag)]
                  n = tagrem(n,0)
                  s = ''
                  if n not in l:
                        n += s
                        l.append(n)             
                  pr = pr[pr.find(itag)+pr.find(ftag)+len(ftag):]
            w = [p,l]
            y[p] = [[["people","varchar(20)"]],l]
            page += 1
            i += 1
      q = raw_input("do you want more projects in this subject?(yes,no): ")
print z;print y
tomdb(z,'languages.mdb')
tomdb(y,'projects.mdb')

