from remoteDBconnector import dbconn
from configparser import ConfigParser
import pandas


config = ConfigParser()
config.read('myconfexample_mongo.cfg')
mytunnel=dbconn('myconfexample_mongo.cfg')
# a=pandas.read_sql('SHOW databases;',mytunnel.conn)

for coll in mytunnel.conn.list_databases():
    print(coll)
    
    
mytunnel.closeAll()