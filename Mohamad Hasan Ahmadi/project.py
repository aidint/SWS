from urllib2 import*
c = open('information.txt')
c = c.read()
b = open('information.txt','w')                 #in this file all the scraped informations are saved
s = raw_input("insert the subject : ")
a = urlopen('https://github.com/search?q='+s+'&ref=commandbar')
a = a.read()
d = open('processing data.txt','w')             #this file opened for saving the data of the current search
tag1 = '<span class="count">'
ta = '</a>'
d.write('the number of related projects with different languages :')
d.write('\n')
while a.find(tag1) != -1:                             #through this loop the name and the number of the projects
      projects_num = a[a.find(tag1)+len(tag1):        #written by different languages is taken
                       a[a.find(tag1):].find('</span>') + a.find(tag1)]
      project_name = a[a[a.find(tag1):].find('</span>')+a.find(tag1)+
                        len('</span>')+13:a[a.find(tag1):].find(ta)+a.find(tag1)]
      d.write(projects_num+'\t'+project_name)
      a = a[a[a.find(tag1):].find('</span>')+a.find(tag1):]
d.write('projects : ')
d.write('\n')
tag2 = '<span class="mega-icon mega-icon-public-repo"></span>'
ht = '">'
ft = '</a>'
itag = 'rel="author">'
ftag = '</a>]'
f = dict()
i = 0
while a.find(tag2) != -1:                 #through this loop the result of the first page of the search is taken
      p = a[a.find(tag2)+len(tag2):]
      p = p[p.find(ht)+len(ht):p.find(ft)]
      d.write(str(i+1) + '.' + p + '\n')
      a = a[a[a.find(tag2):].find('</span>')+a.find(tag2):]       #from here the name of people worked on thw project is taken
      """pr = urlopen('https://github.com/'+p)
      pr = pr.read()
      for k in range(2):
            pr = pr[pr.find(itag)+len(itag):]
      l = []
      while pr.find(itag) != -1 :
            n = pr[pr.find(itag)+len(itag):pr.find(ftag)]
            if n not in l:
                  l.append(n)
            pr = pr[pr.find(ftag)+len(ftag):]
      f[n] = l                     #a dictionary with the project names and the poeple who worked on it"""
      i += 1
q = raw_input("do you want more projects in this subject?(yes,no): ")
page = 2
while q == 'yes':       #through this loop if more projects are needed print yes to get more projects from next pages
      a = urlopen('https://github.com/search?p='+str(page)+'&q='+s+'&ref=commandbar')
      a = a.read()
      while a.find(tag2) != -1:
            p = a[a.find(tag2)+len(tag2):]
            p = p[p.find(ht)+len(ht):p.find(ft)]
            d.write(str(i+1) + '.' + p + '\n')
            a = a[a[a.find(tag2):].find('</span>')+a.find(tag2):]
            page += 1
            i += 1
      q = raw_input("do you want more projects in this subject?(yes,no): ")
d.close()
d = open('processing data.txt')
d = d.read()
b.write(c + d)                      #search results added to the information file
b.write('\n'+'---------------------------------'+'\n')
b.close()
b = open('information.txt')
b = b.read()
print b
