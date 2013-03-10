"""
result must be in this form:
{ "table_name" : [ [ [ "column_name" , "column_type" ] ]  , [ [ value ] ] ] }

example:
{"My Table":[[["Name","varchar(255)"],["Age","varchar(255)"]],[["'Ali'","'22'"],["'Hassan'","'23'"]]],

"Your Table":[[["City","varchar(255)"],["Population","int"],["Current Weather","varchar(255)"]],[["'Tehran'","8","'Sunny'"],["'Rasht'","1","'Rainy'"]]]} 

*text values must be in this form: "'value'"
*number values must be in this form: "value"
*varchar(t) is a text with maximum size of t

a Sample:
t = {"My Table":[[["Name","varchar(255)"],["Age","varchar(255)"]],[["'Ali'","'22'"],["'Hassan'","'23'"]]],"City Table":[[["City","varchar(255)"],["Population","int"],["Current Weather","varchar(255)"]],[["'Tehran'","8","'Sunny'"],["'Rasht'","1","'Rainy'"]]]} 
z = str(random.randint(1,1000))+".mdb"
print z
tomdb(t,z)

"""

import random
import pyodbc
import pypyodbc
import codecs
from bs4 import BeautifulSoup
def tomdb(result,dest):
    dest = dest.replace(" ","_")
    pypyodbc.win_create_mdb(dest)   #creating mdb file 
    MDB = dest; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = ''     #setting up some requirements
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))     #making a connection to mdb
    cur = con.cursor()      #making a cursor to connection
    for tblname in result:
         s = "CREATE TABLE `" + tblname + "` (`" 
         for cols in result[tblname][0]:
             s += str(cols[0])+"` " + str(cols[1]) +",`"
         s= s[:-2] + ");"
         cur.execute(s)
         con.commit()
         for row in result[tblname][1]: 
            s = "INSERT INTO `" + tblname + "` VALUES ("
            for field in row:
                f = field[1:-1]
                f = f.replace("'"," ")
                field = field[0]+f+field[-1]
                field = BeautifulSoup(field).prettify().strip()
                s += field + ","
            s = s[:-1] + ");"
            cur.execute(s)
            con.commit()
    cur.close()
    con.close()
          
    
